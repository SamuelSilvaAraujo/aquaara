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

class PropertyCreateView(LoginRequiredMixin, CreateView):
    model = Property
    template_name = 'property_form.html'
    form_class = PropertyForm

    def get_context_data(self, **kwargs):
        context = super(PropertyCreateView, self).get_context_data(**kwargs)
        context["propertys_page"] = "active"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('ponds_list', kwargs={'pk_property': self.object.pk})

class PropertyUpdateView(LoginRequiredMixin, UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = 'property_form.html'

    def get_success_url(self):
        return reverse('property_list')

    def get_context_data(self, **kwargs):
        context = super(PropertyUpdateView, self).get_context_data(**kwargs)
        context["propertys_page"] = "active"
        return context

class PropertyDeleteView(LoginRequiredMixin, DeleteView):
    model = Property
    template_name = 'property_delete.html'

    def get_success_url(self):
        return reverse('property_list')

    def get_context_data(self, **kwargs):
        context = super(PropertyDeleteView, self).get_context_data(**kwargs)
        context["propertys_page"] = "active"
        return context

class PondListView(LoginRequiredMixin, ListView):
    template_name = 'pond_list.html'
    model = Pond
    pk_url_kwarg = 'pk_property'

    def get_queryset(self):
        property = Property.objects.get(id=self.kwargs["pk_property"])
        return property.pond_set.all()

    def get_context_data(self, **kwargs):
        context = super(PondListView, self).get_context_data(**kwargs)
        property = Property.objects.get(id=self.kwargs["pk_property"])
        context["property"] = property
        context["pond_page"] = "active"
        return context

class PondCreateView(LoginRequiredMixin, CreateView):
    form_class = PondForm
    template_name = 'pond_form.html'

    def get_context_data(self, **kwargs):
        context = super(PondCreateView, self).get_context_data(**kwargs)
        context["property"] = Property.objects.get(pk=self.kwargs["pk_property"])
        context["pond_page"] = "active"
        return context

    def form_valid(self, form):
        pk_property = self.kwargs["pk_property"]
        form = form.save(commit=False)
        form.property = Property.objects.get(pk=pk_property)
        form.save()
        return HttpResponseRedirect(reverse_lazy('pond_detail', kwargs={"pk_property": self.kwargs["pk_property"], "pk_pond": form.id}))

class PondDetailView(LoginRequiredMixin, DetailView):
    template_name = 'pond_detail.html'
    model = Pond
    pk_url_kwarg = "pk_pond"

    def get_context_data(self, **kwargs):
        context = super(PondDetailView, self).get_context_data(**kwargs)
        context["property"] = self.object.property
        context["pond_page"] = "active"
        return context

class PondUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'pond_form.html'
    model = Pond
    form_class = PondForm
    pk_url_kwarg = 'pk_pond'

    def get_success_url(self):
        pk_property = self.kwargs["pk_property"]
        return reverse_lazy('property_ponds', kwargs={"pk_property": pk_property})

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
    template_name = 'cycle_form.html'
    form_class = CycleForm

    def form_valid(self, form):
        form = form.save(commit=False)
        pond = Pond.objects.get(pk=self.kwargs["pk_pond"])
        form.pond = pond
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('pond_detail', kwargs={'pk_property': self.kwargs["pk_property"], 'pk_pond': self.kwargs["pk_pond"]})

    def get_context_data(self, **kwargs):
        context = super(CycleCreateView, self).get_context_data(**kwargs)
        context["property"] = Property.objects.get(pk=self.kwargs["pk_property"])
        context["pond"] = Pond.objects.get(pk=self.kwargs["pk_pond"])
        context["pond_page"] = "active"
        return context

class CycleUpdateView(LoginRequiredMixin, UpdateView):
    model = Cycle
    template_name = 'cycle_form.html'
    pk_url_kwarg = 'pk_cycle'
    form_class = CycleForm

    def get_success_url(self):
        return reverse_lazy('pond_detail', kwargs={'pk_property': self.kwargs["pk_property"], 'pk_pond': self.kwargs["pk_pond"]})

    def get_context_data(self, **kwargs):
        context = super(CycleUpdateView, self).get_context_data(**kwargs)
        context["property"] = Property.objects.get(pk=self.kwargs["pk_property"])
        context["pond"] = Pond.objects.get(pk=self.kwargs["pk_pond"])
        context["pond_page"] = "active"
        return context

class OldCyclesView(LoginRequiredMixin, ListView):
    model = Cycle
    template_name = 'old_cycles.html'

    def get_queryset(self):
        pond = Pond.objects.get(pk=self.kwargs["pk_pond"])
        return pond.allCycle()

    def get_context_data(self, **kwargs):
        context = super(OldCyclesView, self).get_context_data(**kwargs)
        context["property"] = Property.objects.get(pk=self.kwargs["pk_property"])
        context["pond"] = Pond.objects.get(pk=self.kwargs["pk_pond"])
        context["pond_page"] = "active"
        return context

class PopulationCreateView(LoginRequiredMixin, CreateView):
    model = Population
    form_class = PopulationForm
    template_name = 'population_form.html'

    def get_success_url(self):
        return reverse_lazy('custo', kwargs={'pk_property': self.kwargs['pk_property'], 'pk_pond': self.kwargs['pk_pond']})

    def form_valid(self, form):
        pk_pond = self.kwargs["pk_pond"]
        pond_obj = Pond.objects.get(pk=pk_pond)
        cycle = pond_obj.cycle()
        population = form.save()
        cycle.population = population
        cycle.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PopulationCreateView, self).get_context_data(**kwargs)
        context["property"] = Property.objects.get(pk=self.kwargs["pk_property"])
        context["pond"] = Pond.objects.get(pk=self.kwargs["pk_pond"])
        context["pond_page"] = "active"
        return context

class PopulationUpdateView(LoginRequiredMixin, UpdateView):
    model = Population
    template_name = 'population_form.html'
    form_class = PopulationForm
    pk_url_kwarg = 'pk_population'

    def get_success_url(self):
        return reverse_lazy('pond_detail', kwargs={'pk_property': self.kwargs["pk_property"], 'pk_pond': self.kwargs["pk_pond"]})

    def get_context_data(self, **kwargs):
        context = super(PopulationUpdateView, self).get_context_data(**kwargs)
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

def mortality_remove_view(request, pk_property, pk_pond, pk_mortality):
    mortality = Mortality.objects.get(pk=pk_mortality)
    mortality.delete()
    return reverse('pond_detail', pk_property, pk_pond)

class BiometriaCreateView(LoginRequiredMixin, CreateView):
    model = Biometria
    form_class = BiometriaForm
    template_name = 'biometria_form.html'

    def get_success_url(self):
        return reverse_lazy('custo', kwargs={'pk_property': self.kwargs['pk_property'], 'pk_pond': self.kwargs['pk_pond']})

    def form_valid(self, form):
        pond = Pond.objects.get(pk=self.kwargs["pk_pond"])
        form = form.save(commit=False)
        form.cycle = pond.cycle()
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(BiometriaCreateView, self).get_context_data(**kwargs)
        context["property"] = Property.objects.get(pk=self.kwargs["pk_property"])
        context["pond"] = Pond.objects.get(pk=self.kwargs["pk_pond"])
        context["pond_page"] = "active"
        return context

class BiometriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Biometria
    form_class = BiometriaForm
    template_name = 'biometria_form.html'
    pk_url_kwarg = 'pk_biometria'

    def get_success_url(self):
        return reverse_lazy('pond_detail', kwargs={'pk_property': self.kwargs["pk_property"], 'pk_pond': self.kwargs["pk_pond"]})

    def get_context_data(self, **kwargs):
        context = super(BiometriaUpdateView, self).get_context_data(**kwargs)
        context["property"] = Property.objects.get(pk=self.kwargs["pk_property"])
        context["pond"] = Pond.objects.get(pk=self.kwargs["pk_pond"])
        context["pond_page"] = "active"
        return context

class DespescaCreateView(LoginRequiredMixin, CreateView):
    model = Despesca
    form_class = DespescaForm
    template_name = 'despesca.html'

    def get_success_url(self):
        return reverse_lazy('pond_detail', kwargs={'pk_property': self.kwargs["pk_property"], 'pk_pond': self.kwargs["pk_pond"]})

    def form_valid(self, form):
        pk_pond = self.kwargs["pk_pond"]
        pond_obj = Pond.objects.get(pk=pk_pond)
        cycle = pond_obj.cycle()
        form = form.save(commit=False)
        form.cycle = cycle
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DespescaCreateView, self).get_context_data(**kwargs)
        context["property"] = Property.objects.get(pk=self.kwargs["pk_property"])
        context["pond"] = Pond.objects.get(pk=self.kwargs["pk_pond"])
        context["pond_page"] = "active"
        return context

class CostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'cost_form.html'
    model = Cost
    form_class = CostForm

    def get_initial(self):
        initial = super(CostCreateView, self).get_initial()
        initial = initial.copy()
        cycle = Cycle.objects.get(pond__id=self.kwargs["pk_pond"])
        if cycle.cost_set.count() > 0:
            previous_cost = cycle.cost_set.last()
            initial['price'] = previous_cost.price
            initial['weight'] = previous_cost.weight
        return initial

    def form_valid(self, form):
        pond = Pond.objects.get(id=self.kwargs["pk_pond"])
        cycle = pond.cycle()
        form = form.save(commit=False)
        form.cycle = cycle
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('pond_detail', kwargs={'pk_property': self.kwargs["pk_property"], 'pk_pond': self.kwargs["pk_pond"]})

    def get_context_data(self, **kwargs):
        context = super(CostCreateView, self).get_context_data(**kwargs)
        context["property"] = Property.objects.get(pk=self.kwargs["pk_property"])
        context["pond"] = Pond.objects.get(pk=self.kwargs["pk_pond"])
        context["pond_page"] = "active"
        return context

class WaterQualityFormView(LoginRequiredMixin, CreateView):
    template_name = 'water_quality_form.html'
    model = WaterQuality
    form_class = WaterQualityForm

    def form_valid(self, form):
        pond = Pond.objects.get(id=self.kwargs["pk_pond"])
        cycle = pond.cycle()
        form.instance.cycle = cycle
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('pond_detail', kwargs={'pk_property': self.kwargs["pk_property"], 'pk_pond': self.kwargs["pk_pond"]})

    def get_context_data(self, **kwargs):
        context = super(WaterQualityFormView, self).get_context_data(**kwargs)
        context["property"] = Property.objects.get(pk=self.kwargs["pk_property"])
        context["pond"] = Pond.objects.get(pk=self.kwargs["pk_pond"])
        context["pond_page"] = "active"
        return context