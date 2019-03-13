from django import forms
from .models import Property, Address, Pond, Cycle, Population

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', ]
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'})
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        widgets = {
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control m-b'}),
        }

class PondForm(forms.ModelForm):
    class Meta:
        model = Pond
        fields = ['identification', 'water_flow', 'width', 'length', ]
        widgets = {
            'identification': forms.TextInput(attrs={'class': 'form-control'}),
            'water_flow': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Vazão de Água'}),
            'width': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Largura'}),
            'length': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Comprimento'}),
        }

class CycleForm(forms.ModelForm):
    class Meta:
        model = Cycle
        fields = ['type_system', 'middleweight_despesca', ]
        widgets = {
            'type_system': forms.Select(attrs={'class': 'form-control'}),
            'middleweight_despesca': forms.NumberInput(attrs={'class': 'form-control'})
        }

class PopulationForm(forms.ModelForm):
    class Meta:
        model = Population
        fields = ['date', 'middleweight', 'amount', 'age', ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'middleweight': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'})
        }