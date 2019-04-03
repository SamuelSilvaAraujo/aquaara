from django.urls import path, include
from core.views import *

urlpatterns = [
    path('', Index.as_view(), name="index"),
    path('propriedades/', PropertyListView.as_view(), name="property_list"),
    path('propriedade/', include([
        path('cadastro/', PropertyCreateView.as_view(), name="property_create"),
        path('<int:pk>/editar/', PropertyUpdateView.as_view(), name="property_update")
    ])),
    path('<int:pk_property>/', include([
        path('viveiros/', PropertyPondsView.as_view(), name="property_ponds"),
        path('viveiro/', include([
            path('cadastro/', PondCreateView.as_view(), name="pond_create"),
            path('<int:pk_pond>/', include([
                path('', PondDetailView.as_view(), name="pond_detail"),
                path('editar/', PondUpdateView.as_view(), name="pond_update"),
                path('excluir/', PondDeleteView.as_view(), name="pond_delete"),
                path('novo/ciclo/', CycleCreateView.as_view(), name="cycle_init"),
                path('ciclo/<int:pk_cycle>/', CycleDetailView.as_view(), name="cycle_detail"),
                path('povoamento/', PopulationCreateView.as_view(), name="population"),
                path('mortalidade/', MortalityCreateView.as_view(), name="mortality"),
                path('biometria/', BiometriaCreateView.as_view(), name="biometria"),
                path('despesca/', DespescaCreateView.as_view(), name="despesca"),
            ]))
        ])),
    ])),
]