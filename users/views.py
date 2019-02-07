from django.contrib.auth.views import LoginView
from django.views.generic import  CreateView
from .forms import LoginForm, RegisterForm
from django.urls import reverse_lazy

class ViewLogin(LoginView):
    template_name = 'registration/login.html'
    form_class = LoginForm

class ViewRegister(CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')
