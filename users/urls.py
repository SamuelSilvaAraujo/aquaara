from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import *

urlpatterns = [
    path('login/', ViewLogin.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('cadastro/', ViewRegister.as_view(), name="register"),
]