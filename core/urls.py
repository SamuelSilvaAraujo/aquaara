from django.urls import path
from core.views import *

urlpatterns = [
    path('', Index.as_view(), name="index"),
    path('propriedades/', PropriedadesView.as_view(), name="propriedades"),
    path('propriedade/<slug:slug>/', PropriedadeView.as_view(), name="propriedade")
]