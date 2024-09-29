# chat/urls.py
from django.urls import path
from .views import chat_view

urlpatterns = [
    path('<int:patient_id>/', chat_view, name='chat'),
]
