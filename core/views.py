from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Property, Adress
from .forms import PropertyForm, AdressForm

class Index(TemplateView):
    template_name = 'index.html'

class PropertyListView(LoginRequiredMixin, ListView):
    model = Property
    template_name = 'property_list.html'

    def get_queryset(self):
        return Property.objects.filter(user=self.request.user)

class PropertyDetailView(LoginRequiredMixin, DetailView):
    template_name = 'property_detail.html'
    model = Property
    slug_field = 'slug'

class PropertyCreateView(LoginRequiredMixin, CreateView):
    model = Property
    template_name = 'property_create.html'
    form_class = PropertyForm
    second_form_class = AdressForm

    def get_context_data(self, **kwargs):
        context = super(PropertyCreateView, self).get_context_data(**kwargs)
        context["adress_form"] = AdressForm
        return context

    def form_valid(self, form):
        adress_obj = self.second_form_class(self.request.POST).save()
        obj = form.save(commit=False)
        obj.adress = adress_obj
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect(reverse_lazy('propriedade_list'))