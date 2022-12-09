from django import forms
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'nameinput form-style', 'placeholder': 'Your Username', 'autocomplete': 'off'}), max_length=32)
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-style', 'placeholder': 'Your Password', 'autocomplete': 'off'}), max_length=32)
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-style', 'placeholder': 'Confirm Password', 'autocomplete': 'off'}), max_length=32)
