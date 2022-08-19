from dataclasses import field, fields
import email
from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth import get_user_model 



class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = get_user_model()
        fields = ("email",)

class CustomUserUpdate(forms.ModelForm):
    
    email = forms.EmailField(disabled=True)
    phone_number = PhoneNumberField()
    phone_number.error_messages['invalid'] = 'یک شماره تماس معتبر (مانند 0991 991 9999) یا یک شماره با پیشوند کشور مورد نظر وارد نمایید.'
    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email", "profile_picture", "phone_number")
        
               