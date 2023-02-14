# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    username = forms.CharField(max_length=30, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
