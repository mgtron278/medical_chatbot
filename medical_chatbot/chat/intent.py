import openai
import os
from dotenv import load_dotenv
load_dotenv()


openai.api_key = os.getenv('OPENAI_API_KEY')

def recognize_intent_with_gpt(user_message):
    prompt = f"""
    Determine the user's intent from the following message and categorize it into one of the following intents:
    - Medication
    - Appointment
    - Dosage
    - Frequency
    - Labreports
    - Diet
    - Symptoms
    - Doctor notes
    - Treatment
    - realted topics.

    
    Provide the intent as a single word. If you dont find anything related, just output unknown.

    User's message: "{user_message}"
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    intent = response['choices'][0]['message']['content'].strip().lower()
    
    return intent


#print(recognize_intent_with_gpt(' what did i take for my diet'))
def recognize_nature_with_gpt(user_message):
    prompt = f"""
    u have to analyze user message and output "question" in word format if its a question. 

    User's message: "{user_message}"
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    nature = response['choices'][0]['message']['content'].strip().lower()
    
    return nature

