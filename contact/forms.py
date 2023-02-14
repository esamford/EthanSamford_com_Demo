from django import forms
from django.forms import ModelForm
from .models import Message


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ('first_name', 'last_name', 'email', 'message')
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'First name',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Last name',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your email',
                }
            ),
            'message': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'What would you like to say?',
                }
            )
        }



