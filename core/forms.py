from django import forms
from .models import Property, Address, Pond, Cycle, Population, Mortality, Biometria, Despesca

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', ]
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'id': 'name'})
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        widgets = {
            'street': forms.TextInput(attrs={'class': 'form-control', 'id': 'street'}),
            'number': forms.NumberInput(attrs={'class': 'form-control', 'id': 'number'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'id': 'district'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'id': 'city'}),
            'state': forms.Select(attrs={'class': 'form-control m-b', 'id': 'state'}),
        }

class PondForm(forms.ModelForm):
    class Meta:
        model = Pond
        fields = ['identification', 'water_flow', 'width', 'length', ]
        widgets = {
            'identification': forms.TextInput(attrs={'class': 'form-control', 'id': 'identification', 'placeholder': "Ex.: viveiro 01"}),
            'water_flow': forms.NumberInput(attrs={'class': 'form-control', 'id': 'vazao', 'placeholder': "Ex.: 15 L/s"}),
            'width': forms.NumberInput(attrs={'class': 'form-control', 'id': 'largura', 'placeholder': "Ex.: 50m"}),
            'length': forms.NumberInput(attrs={'class': 'form-control', 'id': 'comprimento', 'placeholder': "Ex.: 80m"}),
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
        if system == 'IN' and not type_intensive:
            raise forms.ValidationError("Defina o tipo de sistema intensivo!")

class PopulationForm(forms.ModelForm):
    class Meta:
        model = Population
        fields = ['date', 'middleweight', 'amount_fish']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'middleweight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Ex.: 3 g"}),
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
            'final_middleweight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Ex.: 500 g"}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }