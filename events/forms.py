from django import forms
from django.forms import ModelForm
from .models import Venue


# Venue Form
class VenueForm(ModelForm):
	class Meta:
		model = Venue
		fields = ('__all__')
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control'}),
			'address': forms.TextInput(attrs={'class':'form-control'}),
			'zip_code': forms.TextInput(attrs={'class':'form-control'}),
			'phone': forms.TextInput(attrs={'class':'form-control'}),
			'web': forms.TextInput(attrs={'class':'form-control'}),
			'email': forms.TextInput(attrs={'class':'form-control'}),
		}
