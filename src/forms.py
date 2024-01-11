# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ClimateChange, City


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
    )
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = "__all__"
