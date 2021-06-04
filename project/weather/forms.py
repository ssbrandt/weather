from django.forms import ModelForm, TextInput
from .models import City
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name': TextInput(attrs={'class': 'input', 'placeholder': 'City Name'})}

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=200)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name',)
