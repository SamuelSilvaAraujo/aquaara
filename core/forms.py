from django import forms
from .models import *

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', ]
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'})
        }

class AdressForm(forms.ModelForm):
    class Meta:
        model = Adress
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
        fields = ['identification', 'type_system', 'width', 'length', ]
        widgets = {
            'identification': forms.TextInput(attrs={'class': 'form-control'}),
            'type_system': forms.Select(attrs={'class': 'form-control'}),
            'width': forms.TextInput(attrs={'class': 'form-control'}),
            'length': forms.TextInput(attrs={'class': 'form-control'}),
        }