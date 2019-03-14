from django.contrib.auth.views import LoginView
from django.views.generic import  CreateView
from django.urls import reverse_lazy

from .forms import LoginForm, RegisterForm

class ViewLogin(LoginView):
    template_name = 'registration/login.html'
    form_class = LoginForm

class ViewRegister(CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')
