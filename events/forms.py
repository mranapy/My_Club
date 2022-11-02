from django import forms
from django.forms import ModelForm
from .models import Venue, Event


# Venue Form
class VenueForm(ModelForm):
	class Meta:
		model = Venue
		fields = ('__all__')
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control'}),
			'address': forms.Textarea(attrs={'class':'form-control'}),
			'zip_code': forms.TextInput(attrs={'class':'form-control'}),
			'phone': forms.TextInput(attrs={'class':'form-control'}),
			'web': forms.TextInput(attrs={'class':'form-control'}),
			'email': forms.TextInput(attrs={'class':'form-control'}),
		}


class EventForm(ModelForm):
	class Meta:
		model = Event
		fields = ('name','event_date','venue','manager','description','attendees')
		labels = {
			'event_date' : 'Event Date - YYYY-MM-DD HH:MM:SS'
		}
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control'}),
			'event_date': forms.TextInput(attrs={'class':'form-control'}),
			'venue': forms.Select(attrs={'class':'form-control'}),
			'manager': forms.Select(attrs={'class':'form-control'}),
			'description': forms.Textarea(attrs={'class':'form-control'}),
			'attendees': forms.SelectMultiple(attrs={'class':'form-control'}),
		}

		