from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF', 'data-mask': '999.999.999-99', 'id': 'cpf'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class RegisterForm(UserCreationForm):
    cpf = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'CPF', 'class': 'form-control', 'data-mask': '999.999.999-99', 'id': 'cpf'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nome', 'class': 'form-control', 'id': 'nome'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Senha', 'class': 'form-control', 'id': 'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Corfimar Senha', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ("cpf", "name", "password1", "password2")