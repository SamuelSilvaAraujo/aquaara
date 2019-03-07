from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Property, Pond, Cycle
from .forms import PondForm, PropertyForm, AdressForm, CycleForm

class Index(TemplateView):
    template_name = 'index.html'

class PropertyListView(LoginRequiredMixin, ListView):
    model = Property
    template_name = 'property_list.html'

    def get_queryset(self):
        return self.request.user.property_set.all()

class PropertyPondsView(LoginRequiredMixin, DetailView):
    template_name = 'property_ponds.html'
    model = Property
    pk_url_kwarg = 'pk_property'

    def get_context_data(self, **kwargs):
        context = super(PropertyPondsView, self).get_context_data(**kwargs)
        context["pk_property"] = self.kwargs["pk_property"]
        context["active_page"] = "active"
        return context

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
        return HttpResponseRedirect(reverse_lazy('property_ponds', kwargs={'pk_property': obj.id}))

class PondCreateView(LoginRequiredMixin, CreateView):
    form_class = PondForm
    template_name = 'pond_create.html'
    pk_url_kwarg = 'pk_property'

    def get_context_data(self, **kwargs):
        context = super(PondCreateView, self).get_context_data(**kwargs)
        context["pk_property"] = self.kwargs["pk_property"]
        return context

    def form_valid(self, form):
        pk_property = self.kwargs["pk_property"]
        obj = form.save(commit=False)
        obj.property = Property.objects.get(pk=pk_property)
        obj.save()
        return HttpResponseRedirect(reverse_lazy('pond_detail', kwargs={"pk_property": pk_property, "pk_pond": obj.id}))

class PondDetailView(LoginRequiredMixin, DetailView):
    template_name = 'pond_detail.html'
    model = Pond
    pk_url_kwarg = "pk_pond"

    def get_context_data(self, **kwargs):
        context = super(PondDetailView, self).get_context_data(**kwargs)
        context["pk_property"] = self.kwargs["pk_property"]
        return context

class PondUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'pond_update.html'
    model = Pond
    form_class = PondForm
    pk_url_kwarg = 'pk_pond'

    def get_success_url(self):
        pk_property = self.kwargs["pk_property"]
        pk_pond = self.kwargs["pk_pond"]
        return  reverse_lazy('pond_detail', kwargs={"pk_property": pk_property, "pk_pond": pk_pond})

    def get_context_data(self, **kwargs):
        context = super(PondUpdateView, self).get_context_data(**kwargs)
        context["pk_property"] = self.kwargs["pk_property"]
        context["pk_pond"] = self.kwargs["pk_pond"]
        return context

class PondDeleteView(LoginRequiredMixin, DeleteView):
    model = Pond
    template_name = 'pond_delete.html'
    pk_url_kwarg = 'pk_pond'

    def get_success_url(self):
        pk_property = self.kwargs["pk_property"]
        return  reverse('property_ponds', kwargs={"pk_property": pk_property})

    def get_context_data(self, **kwargs):
        context = super(PondDeleteView, self).get_context_data(**kwargs)
        context["pk_property"] = self.kwargs["pk_property"]
        return context

class CycleInitView(LoginRequiredMixin, CreateView):
    model = Cycle
    template_name = 'cycle_init.html'
    form_class = CycleForm
    pk_url_kwarg = 'pk_pond'

    def form_valid(self, form):
        pk_pond = self.kwargs["pk_pond"]
        pk_property = self.kwargs["pk_property"]
        obj = form.save(commit=False)
        obj.pond = Pond.objects.get(pk=pk_pond)
        obj.save()
        return HttpResponseRedirect(reverse_lazy('pond_detail', kwargs={'pk_property': pk_property, 'pk_pond': pk_pond}))
    
    def get_context_data(self, **kwargs):
        context = super(CycleInitView, self).get_context_data(**kwargs)
        context["pk_property"] = self.kwargs["pk_property"]
        context["pk_pond"] = self.kwargs["pk_pond"]
        return context