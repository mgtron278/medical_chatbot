# chat/forms.py
from django import forms

class MessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, label='Your Message')
