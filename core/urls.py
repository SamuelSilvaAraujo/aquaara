from django.urls import path, include
from core.views import *

urlpatterns = [
    path('', Index.as_view(), name="index"),
    path('propriedades/', PropertyListView.as_view(), name="propriedade_list"),
    path('novapropriedade/', PropertyCreateView.as_view(), name="propriedade_create"),
    path('<slug:slug_property>/', include([
        path('viveiros/', PropertyPondsView.as_view(), name="propriedade_ponds"),
        path('novoviveiro/', PondCreateView.as_view(), name="pond_create"),
        path('viveiro/<slug:slug_pond>/', PondDetailView.as_view(), name="pond_detail"),
        path('viveiro/<slug:slug_pond>/atualizar/',  PondUpdateView.as_view(), name="pond_update"),
        path('viveiro/<slug:slug_pond>/excluir/',  PondDeleteView.as_view(), name="pond_delete"),
    ])),
]