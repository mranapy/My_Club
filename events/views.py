from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from .forms import VenueForm
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect,HttpResponse
# Create your views here.
def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	month = month.capitalize()
	# Convert month from name to number
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)
	
	# create a calendar
	cal = HTMLCalendar().formatmonth(year, month_number)
	now = datetime.now()
	current_year = now.year
	time = now.strftime('%I:%M %p')
	context = {
		'year': year,
		'month': month,
		'month_number':month_number,
		'cal':cal,
		'current_year':current_year,
		# 'now':now,
		'time':time,
	}
	return render(request, 'events/home.html', context)
 
# All Events
def all_events(request):
	events = Event.objects.all()
	return render(request, 'events/events_list.html', {'events':events})

# class VenueList(ListView):
# 	model = Event
# 	template_name = 'events/venue_list.html'
# 	context_object_name = 'venues'
# 	ordering = {'name'}

def all_venues(request):
	venues = Venue.objects.all()
	return render(request, 'events/venue_list.html', {'venues':venues})

def add_venue(request):
	submitted = False
	if request.method == "POST":
		venueform = VenueForm(request.POST)
		if venueform.is_valid():
			venueform.save()
			submitted = True
			return HttpResponseRedirect('/add-venue?submitted=True')
	else:
		venueform = VenueForm()
		if 'submitted' in request.GET:
			submitted = True
	return render(request, 'events/add_venue.html',{
				'venueform':venueform,
				'submitted':submitted
			})


def show_venue(request, venue_id):
	try:
		venue = Venue.objects.get(pk=venue_id)
	except VenuesModel.DoesNotExist:
            return HttpResponse('Exception: Data Not Found')
	return render(request, 'events/show_venue.html', {'venue':venue})



def search_any(request):
	if request.method == "POST":
		searched = request.POST['searched']
		if searched == "":
			return HttpResponseRedirect('/')
		else:
			venues = Venue.objects.filter(name__icontains=searched)
			events = Event.objects.filter(name__icontains=searched)
			return render(request, 'events/search.html',{'searched':searched,'venues':venues,'events':events})
	
