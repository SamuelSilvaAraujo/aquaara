from django.urls import path
from core.views import *

urlpatterns = [
    path('', Index.as_view(), name="index"),
    path('propriedade/list/', PropertyListView.as_view(), name="propriedade_list"),
    path('propriedade/detail/<slug:slug>/', PropertyDetailView.as_view(), name="propriedade_detail"),
    path('propriedade/create/', PropertyCreateView.as_view(), name="propriedade_create"),
]