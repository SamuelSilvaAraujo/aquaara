from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *

class Index(TemplateView):
    template_name = 'index.html'

class PropertyListView(LoginRequiredMixin, ListView):
    model = Property
    template_name = 'property_list.html'

    def get_queryset(self):
        return self.request.user.property_set.all()

    def get_context_data(self, **kwargs):
        context = super(PropertyListView, self).get_context_data(**kwargs)
        context["propertys_page"] = "active"
        return context

class PropertyPondsView(LoginRequiredMixin, DetailView):
    template_name = 'property_ponds.html'
    model = Property
    pk_url_kwarg = 'pk_property'

    def get_context_data(self, **kwargs):
        context = super(PropertyPondsView, self).get_context_data(**kwargs)
        context["pk_property"] = self.kwargs["pk_property"]
        context["pond_page"] = "active"
        return context

class PropertyCreateView(LoginRequiredMixin, CreateView):
    model = Property
    template_name = 'property_create.html'
    form_class = PropertyForm
    second_form_class = AddressForm

    def get_context_data(self, **kwargs):
        context = super(PropertyCreateView, self).get_context_data(**kwargs)
        context["address_form"] = AddressForm
        context["propertys_page"] = "active"
        return context

    def form_valid(self, form):
        address_obj = self.second_form_class(self.request.POST).save()
        obj = form.save(commit=False)
        obj.address = address_obj
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect(reverse_lazy('property_ponds', kwargs={'pk_property': obj.id}))

class PropertyUpdateView(LoginRequiredMixin, UpdateView):
    model = Property
    form_class = PropertyForm
    second_form_class = AddressForm
    template_name = 'property_update.html'

    def form_valid(self, form):
        address_obj = self.second_form_class(self.request.POST).save()
        property_obj = form.save(commit=False)
        property_obj.address = address_obj
        property_obj.save()
        return HttpResponseRedirect(reverse_lazy("property_list"))

    def get_context_data(self, **kwargs):
        context = super(PropertyUpdateView, self).get_context_data(**kwargs)
        context["address_form"] = self.second_form_class(instance=self.object.address)
        return context

class PropertyDeleteView(LoginRequiredMixin, DeleteView):
    model = Property
    template_name = 'property_delete.html'

    def get_success_url(self):
        return reverse('property_list')

class PondCreateView(LoginRequiredMixin, CreateView):
    form_class = PondForm
    template_name = 'pond_create.html'

    def get_context_data(self, **kwargs):
        context = super(PondCreateView, self).get_context_data(**kwargs)
        context["property"] = Property.objects.get(pk=self.kwargs["pk_property"])
        context["pond_page"] = "active"
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
        context["property"] = Property.objects.get(pk=self.kwargs["pk_property"])
        context["pond_page"] = "active"
        return context

class PondUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'pond_update.html'
    model = Pond
    form_class = PondForm
    pk_url_kwarg = 'pk_pond'

    def get_success_url(self):
        pk_property = self.kwargs["pk_property"]
        pk_pond = self.kwargs["pk_pond"]
        return reverse_lazy('pond_detail', kwargs={"pk_property": pk_property, "pk_pond": pk_pond})

    def get_context_data(self, **kwargs):
        context = super(PondUpdateView, self).get_context_data(**kwargs)
        context["property"] = Property.objects.get(pk=self.kwargs["pk_property"])
        context["pond"] = Pond.objects.get(pk=self.kwargs["pk_pond"])
        context["pond_page"] = "active"
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
        context["property"] = Property.objects.get(pk=self.kwargs["pk_property"])
        context["pond_page"] = "active"
        return context

class CycleCreateView(LoginRequiredMixin, CreateView):
    model = Cycle
    template_name = 'cycle_create.html'
    form_class = CycleForm

    def form_valid(self, form):
        pk_pond = self.kwargs["pk_pond"]
        pk_property = self.kwargs["pk_property"]
        obj = form.save(commit=False)
        if obj.system == 'IN' and not obj.type_intensive:
            return super().form_invalid(form)
        obj.pond = Pond.objects.get(pk=pk_pond)
        obj.save()
        return HttpResponseRedirect(reverse_lazy('pond_detail', kwargs={'pk_property': pk_property, 'pk_pond': pk_pond}))

    def get_context_data(self, **kwargs):
        context = super(CycleCreateView, self).get_context_data(**kwargs)
        context["property"] = Property.objects.get(pk=self.kwargs["pk_property"])
        context["pond"] = Pond.objects.get(pk=self.kwargs["pk_pond"])
        context["pond_page"] = "active"
        return context

class PopulationCreateView(LoginRequiredMixin, CreateView):
    model = Population
    form_class = PopulationForm
    template_name = 'population_create.html'

    def form_valid(self, form):
        pk_pond = self.kwargs["pk_pond"]
        pk_property = self.kwargs["pk_property"]
        pond_obj = Pond.objects.get(pk=pk_pond)
        cycle = pond_obj.cycle()
        population_obj = form.save()
        cycle.population = population_obj
        cycle.save()
        return HttpResponseRedirect(reverse_lazy('pond_detail', kwargs={'pk_property': pk_property, 'pk_pond': pk_pond}))

    def get_context_data(self, **kwargs):
        context = super(PopulationCreateView, self).get_context_data(**kwargs)
        context["property"] = Property.objects.get(pk=self.kwargs["pk_property"])
        context["pond"] = Pond.objects.get(pk=self.kwargs["pk_pond"])
        context["pond_page"] = "active"
        return context

class MortalityCreateView(LoginRequiredMixin, CreateView):
    model = Mortality
    form_class = MortalityForm
    template_name = 'mortality.html'

    def form_valid(self, form):
        pk_pond = self.kwargs["pk_pond"]
        pk_property = self.kwargs["pk_property"]
        pond_obj = Pond.objects.get(pk=pk_pond)
        obj = form.save(commit=False)
        obj.cycle = pond_obj.cycle()
        obj.save()
        return HttpResponseRedirect(reverse_lazy('pond_detail', kwargs={'pk_property': pk_property, 'pk_pond': pk_pond}))

    def get_context_data(self, **kwargs):
        context = super(MortalityCreateView, self).get_context_data(**kwargs)
        context["property"] = Property.objects.get(pk=self.kwargs["pk_property"])
        context["pond"] = Pond.objects.get(pk=self.kwargs["pk_pond"])
        context["pond_page"] = "active"
        return context

class BiometriaCreateView(LoginRequiredMixin, CreateView):
    model = Biometria
    form_class = BiometriaForm
    template_name = 'biometria.html'

    def form_valid(self, form):
        pk_pond = self.kwargs["pk_pond"]
        pk_property = self.kwargs["pk_property"]
        pond_obj = Pond.objects.get(pk=pk_pond)
        obj = form.save(commit=False)
        obj.cycle = pond_obj.cycle()
        obj.save()
        return HttpResponseRedirect(reverse_lazy('pond_detail', kwargs={'pk_property': pk_property, 'pk_pond': pk_pond}))

    def get_context_data(self, **kwargs):
        context = super(BiometriaCreateView, self).get_context_data(**kwargs)
        context["property"] = Property.objects.get(pk=self.kwargs["pk_property"])
        context["pond"] = Pond.objects.get(pk=self.kwargs["pk_pond"])
        context["pond_page"] = "active"
        return context

class DespescaCreateView(LoginRequiredMixin, CreateView):
    model = Despesca
    form_class = DespescaForm
    template_name = 'despesca.html'

    def form_valid(self, form):
        pk_pond = self.kwargs["pk_pond"]
        pk_property = self.kwargs["pk_property"]
        pond_obj = Pond.objects.get(pk=pk_pond)
        despesca_obj = form.save()
        cycle = pond_obj.cycle()
        cycle.despesca = despesca_obj
        cycle.save()
        return HttpResponseRedirect(reverse_lazy('pond_detail', kwargs={'pk_property': pk_property, 'pk_pond': pk_pond}))

    def get_context_data(self, **kwargs):
        context = super(DespescaCreateView, self).get_context_data(**kwargs)
        context["property"] = Property.objects.get(pk=self.kwargs["pk_property"])
        context["pond"] = Pond.objects.get(pk=self.kwargs["pk_pond"])
        context["pond_page"] = "active"
        return context