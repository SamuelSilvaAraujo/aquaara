from django.urls import path
from core.views import *

urlpatterns = [
    path('', Index.as_view(), name="index"),
    path('propriedade/list/', PropertyListView.as_view(), name="propriedade_list"),
    path('propriedade/detail/<slug:slug>/', PropertyDetailView.as_view(), name="propriedade_detail"),
    path('propriedade/create/', PropertyCreateView.as_view(), name="propriedade_create"),
    path('propriedade/<slug:slug>/viveiro/create/', PondCreateView.as_view(), name="viveiro_create"),
    path('propriedade/<slug:property_slug>/viveiro/<slug:slug>/', PondDetailView.as_view(), name="viveiro_detail")
]