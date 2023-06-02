# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ClimateChange

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True,)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')

class ClimateChangeForm(forms.ModelForm):
  class Meta:
    model = ClimateChange
    fields = ['date', 'temperature', 'precipitation']