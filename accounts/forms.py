from dataclasses import field, fields
import email
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = get_user_model()
        fields = ("email",)

class CustomUserUpdate(forms.ModelForm):
    
    email = forms.EmailField(disabled=True)
    
    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email", "profile_picture")
        
               