from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Property, Pond
from .forms import PondForm, PropertyForm, AdressForm

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
    slug_url_kwarg = 'slug_property'

    def get_context_data(self, **kwargs):
        context = super(PropertyPondsView, self).get_context_data(**kwargs)
        context["slug_property"] = self.kwargs["slug_property"]
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
        return HttpResponseRedirect(reverse_lazy('propriedade_list'))

class PondCreateView(LoginRequiredMixin, CreateView):
    form_class = PondForm
    template_name = 'pond_create.html'
    slug_url_kwarg = 'slug_property'

    def get_context_data(self, **kwargs):
        context = super(PondCreateView, self).get_context_data(**kwargs)
        context["slug_property"] = self.kwargs["slug_property"]
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        slug = self.kwargs["slug_property"]
        obj.property = Property.objects.filter(slug=slug)[0]
        obj.save()
        return HttpResponseRedirect(reverse_lazy('propriedade_ponds', kwargs={"slug_property": slug}))

class PondDetailView(LoginRequiredMixin, DetailView):
    template_name = 'pond_detail.html'
    model = Pond
    slug_url_kwarg = "slug_pond"

    def get_context_data(self, **kwargs):
        context = super(PondDetailView, self).get_context_data(**kwargs)
        context["slug_property"] = self.kwargs["slug_property"]
        return context

class PondUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'pond_update.html'
    model = Pond
    form_class = PondForm
    slug_url_kwarg = 'slug_pond'

    def get_success_url(self):
        slug_property = self.kwargs["slug_property"]
        slug = self.kwargs["slug_pond"]
        return  reverse_lazy('viveiro_detail', kwargs={"slug_property": slug_property, "slug_pond": slug})

    def get_context_data(self, **kwargs):
        context = super(PondUpdateView, self).get_context_data(**kwargs)
        context["slug_property"] = self.kwargs["slug_property"]
        context["slug_pond"] = self.kwargs["slug_pond"]
        return context

class PondDeleteView(LoginRequiredMixin, DeleteView):
    model = Pond
    template_name = 'pond_delete.html'
    slug_url_kwarg = 'slug_pond'

    def get_success_url(self):
        slug_property = self.kwargs["slug_property"]
        return  reverse('propriedade_ponds', kwargs={"slug_property": slug_property})

    def get_context_data(self, **kwargs):
        context = super(PondDeleteView, self).get_context_data(**kwargs)
        context["slug_property"] = self.kwargs["slug_property"]
        return context