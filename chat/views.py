from django.shortcuts import render, redirect
from .models import Patient, Conversation
from .forms import MessageForm
from django.http import HttpResponse
from dotenv import load_dotenv
import os
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from .extractor import extract_entities_with_gpt
from .graph import store_entities_in_knowledge_graph
from .graph import retrieve_information_from_knowledge_graph
from .intent import recognize_nature_with_gpt
from .summary import summarize_conversation

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')


def home_view(request):
    return HttpResponse("<h1>Welcome to the Medical Chatbot</h1><p><a href='/chat/1/'>Start Chat</a></p>")

memory = ConversationBufferMemory(input_key="user_message", memory_key="history", return_messages=True)
# chat/views.py
def chat_view(request, patient_id):
    retrieved_info = ''
    patient = Patient.objects.get(id=patient_id)
    
    patient_info = f"""
    Patient Medical Information:
    - Medical Condition: {patient.medical_condition}
    - Medication Regimen: {patient.medication_regimen}
    - Last Appointment: {patient.last_appointment}
    - Next Appointment: {patient.next_appointment}
    - Doctor's Name: {patient.doctor_name}
    """

    # Define a LangChain prompt template with placeholders
    prompt_template = PromptTemplate(
        input_variables=["patient_info","retrieved_info", "user_message", "history"],
        template="""
        You are a medical assistant chatbot. Never speak in third person. Give brief but precise responses. Here is the patient information:
        {patient_info}
        If appointment change is requested, inform patient the information is conveyed to doctor and waiting response.
        Information from previous conversations :{retrieved_info}
        you have access to last message: {history}
        "DO NOT GREET USER AND DO NOT INTRODUCE YOURSELF AS CHATBOT"
        Do not ask any questions. Please respond to the following user message in a clear, compassionate, and professional way.
        User: {user_message}
        """,
    )
    llm = ChatOpenAI(openai_api_key=openai_api_key, model_name="gpt-3.5-turbo", temperature=0.2)
        
    conversations = Conversation.objects.filter(patient=patient).order_by('timestamp')
    
    conversations2 = Conversation.objects.filter(patient=patient).order_by('-timestamp')[:4]

    # Reverse the order to maintain chronological flow in the prompt
    last_two_conversations = reversed(conversations2)
    chat_chain = LLMChain(llm=llm, prompt=prompt_template, memory=memory)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        
        if 'reset_summary' in request.POST:  # Check if reset button was clicked
            request.session['current_summary'] = ''  # Clear the summary
            return redirect('chat', patient_id=patient.id)
        
        if form.is_valid():
            user_message = form.cleaned_data['message']
            
            Conversation.objects.create(patient=patient, message=user_message, message_by_user=True)

            
            if  recognize_nature_with_gpt(user_message) == 'question':
                retrieved_info = retrieve_information_from_knowledge_graph(patient, user_message)

            else:
                extracted_entities = extract_entities_with_gpt(user_message)
                
                if extracted_entities:
                        store_entities_in_knowledge_graph(patient, extracted_entities)

                
            if not retrieved_info:
                retrieved_info = ''
            
            formatted_history = []
            for message in last_two_conversations:
                if message.message_by_user:
                    formatted_history.append(f"user: {message.message}")
                else:
                    formatted_history.append(f"AI: {message.message}")

            formatted_history_output = "\n".join(formatted_history)
            
            print("Type of 'formatted_history_output':", type(formatted_history_output))

            ai_response = chat_chain.run({
                "patient_info": patient_info,
                "retrieved_info": str(retrieved_info),
                "user_message": user_message,
                "history": formatted_history_output if formatted_history_output else "No prior conversation."
            })
                
                
            Conversation.objects.create(patient=patient, message=ai_response, message_by_user=False)
            
            if 'current_summary' not in request.session:
                request.session['current_summary'] = ''

            # Include the new interaction to be summarized
            new_interaction = f"User: {user_message}\nAI: {ai_response}"
            
            # Combine previous summary with the new interaction for summarization
            updated_summary = summarize_conversation(request.session['current_summary'] + "\n" + new_interaction)
            
            # Update the session to keep the latest summary
            request.session['current_summary'] = updated_summary            
            return redirect('chat', patient_id=patient.id)
    else:
        form = MessageForm()

     
        if not Conversation.objects.filter(patient=patient).exists():
            greeting = f"Hello {patient.first_name}, how can I assist you today?"
            Conversation.objects.create(patient=patient, message=greeting, message_by_user=False)

    
    conversations = Conversation.objects.filter(patient=patient).order_by('timestamp')

    return render(request, 'chat/chat.html', {'form': form, 'conversations': conversations, 'patient': patient, 'current_summary': request.session.get('current_summary', '')})


