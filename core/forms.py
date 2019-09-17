from django import forms
from .models import *

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'district', 'city', 'state', 'complement', ]
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'complement': forms.TextInput(attrs={'class': 'form-control'})
        }

class PondForm(forms.ModelForm):
    class Meta:
        model = Pond
        fields = ['identification', 'water_flow', 'width', 'length', ]
        widgets = {
            'identification': forms.TextInput(attrs={'class': 'form-control', 'id': 'identification'}),
            'water_flow': forms.NumberInput(attrs={'class': 'form-control', 'id': 'vazao'}),
            'width': forms.NumberInput(attrs={'class': 'form-control', 'id': 'largura'}),
            'length': forms.NumberInput(attrs={'class': 'form-control', 'id': 'comprimento'}),
        }

class CycleForm(forms.ModelForm):
    class Meta:
        model = Cycle
        fields = ['system', 'final_middleweight', 'type_intensive', ]
        widgets = {
            'system': forms.Select(attrs={'class': 'form-control', 'id': 'system'}),
            'final_middleweight': forms.Select(attrs={'class': 'form-control', 'id': 'middleweight_despesca'}),
            'type_intensive': forms.Select(attrs={'class': 'form-control', 'id': 'type_intensive'}),
        }

    def clean(self):
        system = self.cleaned_data["system"]
        type_intensive = self.cleaned_data["type_intensive"]
        if system == Cycle.INTENSIVE and not type_intensive:
            self.add_error('type_intensive', "Defina o tipo de sistema intensivo!")

class PopulationForm(forms.ModelForm):
    class Meta:
        model = Population
        fields = ['date', 'middleweight', 'amount_fish']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'middleweight': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount_fish': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class MortalityForm(forms.ModelForm):
    class Meta:
        model = Mortality
        fields = ['date', 'amount', ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Ex.: 10 peixes"}),
        }

    # def __init__(self, *args, **kwargs):
    #     self.pond_id = kwargs.pop('pond_id', None)
    #     super(MortalityForm, self).__init__(*args, **kwargs)
    #
    # def clean_amount(self):
    #     pond = Pond.objects.get(id=self.pond_id)
    #     amount = self.cleaned_data['amount']
    #     if amount > pond.cycle().amount_fish_current():
    #         raise forms.ValidationError("Quantidade de peixes maior que a quantidade de peixes atual!")
    #     return amount


class BiometriaForm(forms.ModelForm):
    class Meta:
        model = Biometria
        fields = ['date', 'middleweight', ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'middleweight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Ex.: 50 g"}),
        }

class DespescaForm(forms.ModelForm):
    class Meta:
        model = Despesca
        fields = ['date', 'middleweight', 'amount']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'middleweight': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CostForm(forms.ModelForm):
    class Meta:
        model = Cost
        fields = ['weight', 'price']
        widgets = {
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class WaterQualityForm(forms.ModelForm):
    class Meta:
        model = WaterQuality
        exclude = ['date']
        widgets = {
            'ph': forms.NumberInput(attrs={'class': 'form-control'}),
            'oxygen': forms.NumberInput(attrs={'class': 'form-control'}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control'}),
            'transparency': forms.NumberInput(attrs={'class': 'form-control'}),
        }