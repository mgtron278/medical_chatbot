import openai
import json
import os
from dotenv import load_dotenv
load_dotenv()


openai.api_key = os.getenv('OPENAI_API_KEY')

def summarize_conversation(convo):
    # Structure the messages for the API call
    messages = [
        {"role": "system", "content": "You are a helpful assistant that summarizes medical chatbot conversations into paragraph."},
        {"role": "user", "content": convo}
    ]

    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=700,  # Adjust the max tokens for your desired summary length
        temperature=0.2  # Adjust the temperature for less or more creative summaries
    )

    # Extract and return the summary
    summary = response['choices'][0]['message']['content']
    return summary


