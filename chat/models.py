from django.db import models

# Create your models here.
# chat/models.py


class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    medical_condition = models.TextField()
    medication_regimen = models.TextField()
    last_appointment = models.DateField()
    next_appointment = models.DateField()
    doctor_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
# chat/models.py
class Conversation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    message_by_user = models.BooleanField(default=True)

    def __str__(self):
        sender = "User" if self.message_by_user else "AI"
        return f"{sender}: {self.message}"


