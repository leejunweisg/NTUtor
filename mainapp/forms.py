from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'form-control', 'placeholder': 'username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class':'form-control', 'placeholder':'password'}))

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "username", "class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder" : "email", "class": "form-control"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder" : "password","class": "form-control"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder" : "repeat password",  "class": "form-control"}))

    def clean(self):
        # code ensures that any validation logic in parent classes is maintained
        cleaned_data = super().clean()
        email = cleaned_data.get("email")

        # check if email already exists, raise error
        if User.objects.filter(email=cleaned_data.get('email')).exists():
            raise ValidationError("This email address already exists.")

    # defines which model this form is linked to
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
