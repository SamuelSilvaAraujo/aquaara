from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Propriedade

class Index(TemplateView):
    template_name = 'index.html'

class PropriedadesView(LoginRequiredMixin, ListView):
    model = Propriedade
    template_name = 'propriedades.html'

    def get_queryset(self):
        return Propriedade.objects.filter(user=self.request.user)


class PropriedadeView(LoginRequiredMixin, DetailView):
    template_name = 'propriedade.html'
    model = Propriedade
    slug_field = 'slug'