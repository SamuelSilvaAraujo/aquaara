from django import forms
from .models import Property, Address, Pond, Cycle, Population, Mortality

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
            'identification': forms.TextInput(attrs={'class': 'form-control', 'id': 'identification'}),
            'water_flow': forms.NumberInput(attrs={'class': 'form-control', 'id': 'vazao'}),
            'width': forms.NumberInput(attrs={'class': 'form-control', 'id': 'largura'}),
            'length': forms.NumberInput(attrs={'class': 'form-control', 'id': 'comprimento'}),
        }

class CycleForm(forms.ModelForm):
    class Meta:
        model = Cycle
        fields = ['system', 'middleweight_despesca', 'type_intensive', ]
        widgets = {
            'system': forms.Select(attrs={'class': 'form-control', 'id': 'system'}),
            'middleweight_despesca': forms.Select(attrs={'class': 'form-control', 'id': 'middleweight_despesca'}),
            'type_intensive': forms.Select(attrs={'class': 'form-control', 'id': 'type_intensive'}),
        }

class PopulationForm(forms.ModelForm):
    class Meta:
        model = Population
        fields = ['date', 'middleweight', ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'middleweight': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class MortalityForm(forms.ModelForm):
    class Meta:
        model = Mortality
        fields = ['date', 'amount', ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }