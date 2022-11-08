from django import forms
from django.forms import ModelForm
from .models import Venue, Event

# Venue Form
class VenueForm(ModelForm):
	class Meta:
		model = Venue
		# fields = ('__all__')
		fields = ('name','address','zip_code','phone','web','email')
		labels = {
			'address': "Venue Address"
		}
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control'}),
			'address': forms.Textarea(attrs={'class':'form-control input-lg','rows':'3'}),
			'zip_code': forms.TextInput(attrs={'class':'form-control'}),
			'phone': forms.TextInput(attrs={'class':'form-control'}),
			'web': forms.TextInput(attrs={'class':'form-control'}),
			'email': forms.TextInput(attrs={'class':'form-control'}),
		}
		# def __init__(self, *args, **kwargs):
		# 	super(VenueForm, self).__init__(*args, **kwargs)
		# 	for field in self.fields.values():
		# 		field.error_messages = {'required': ugettext('The field : {fieldname} is required !!').format(fieldname=field.label),'invalid': ugettext('The field : {fieldname} is invalid !!').format(fieldname=field.label)
  #           }


class EventFormAdmin(ModelForm):
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
			'description': forms.Textarea(attrs={'class':'form-control','rows':'4'}),
			'attendees': forms.SelectMultiple(attrs={'class':'form-control'}),
		}

# This Form For Manager
class EventForm(ModelForm):
	class Meta:
		model = Event
		fields = ('name','event_date','venue','description','attendees')
		labels = {
			'event_date' : 'Event Date - YYYY-MM-DD HH:MM:SS'
		}
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control'}),
			'event_date': forms.TextInput(attrs={'class':'form-control'}),
			'venue': forms.Select(attrs={'class':'form-control'}),
			'description': forms.Textarea(attrs={'class':'form-control','rows':'4'}),
			'attendees': forms.SelectMultiple(attrs={'class':'form-control'}),
		}