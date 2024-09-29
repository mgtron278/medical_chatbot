import os
import django

# Step 1: Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical_chatbot.settings')  # Replace with your actual project name
django.setup()

# Step 2: Import your Patient model
from chat.models import Patient

# Step 3: Define the patient data
patient_data = {
    'first_name': 'John',
    'last_name': 'Doe',
    'medical_condition': 'Hypertension',
    'medication_regimen': 'Lisinopril 10mg once daily',
    'last_appointment': '2023-09-01',
    'next_appointment': '2023-10-01',
    'doctor_name': 'Dr. Smith'
}

# Step 4: Create the patient in the database
try:
    patient = Patient.objects.create(**patient_data)
    print(f"Patient {patient.first_name} {patient.last_name} created successfully!")
except Exception as e:
    print(f"An error occurred: {e}")