from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'form-control', 'placeholder': 'username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class':'form-control', 'placeholder':'password'}))

class UserRegisterForm(UserCreationForm):
    # adds an email field on top of the fields in UserCreationForm
    email = forms.EmailField() # default required=True
    
    # defines which model this form is linked to
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
