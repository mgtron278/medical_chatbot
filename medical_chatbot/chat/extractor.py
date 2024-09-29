import openai
import json
import os
from dotenv import load_dotenv
load_dotenv()


openai.api_key = os.getenv('OPENAI_API_KEY')
def extract_entities_with_gpt(user_message):
    prompt = f"""
    Extract the following entities from the user's message, if availabe:
    - Medication
    - Appointment
    - Dosage
    - Frequency
    - lab_reports
    - Diet
    - Symptoms
    - doctor_notes
    - Treatment
    - Any other health-related, body-related, hospital-related information
    if nothing is found, do no mention the key-value pair.
    Provide the output in JSON format with keys as entity types.

    User's message: "{user_message}"
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    try:
        entities = json.loads(response.choices[0].message['content'].strip())
    except json.JSONDecodeError:
        entities = {}
    return entities