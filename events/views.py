from django.shortcuts import render,redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .models import Event, Venue
from .forms import VenueForm,EventForm
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
 
# ---------- SHOW ALL EVENT ----------
def all_events(request):
	events = Event.objects.all()
	return render(request, 'events/events_list.html', {'events':events})

# class VenueList(ListView):
# 	model = Event
# 	template_name = 'events/venue_list.html'
# 	context_object_name = 'venues'
# 	ordering = {'name'}

# ---------- SHOW ALL VENUE ----------
def all_venues(request):
	venues = Venue.objects.all()
	return render(request, 'events/venue_list.html', {'venues':venues})

# ---------- ADD VENUE ----------
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

# ---------- ADD EVENT ----------
def addEvent(request):
	submitted = False
	if request.method == "POST":
		eventform = EventForm(request.POST)
		if eventform.is_valid():
			eventform.save()
			submitted = True
			# return redirect('list-events')
			return HttpResponseRedirect('/add-event?submitted=True')
	else:
		eventform = EventForm()
		if 'submitted' in request.GET:
			submitted = True
	return render(request, 'events/add_event.html',{'eventform':eventform,'submitted':submitted})

# ---------- SHOW VENUE ----------
def show_venue(request, venue_id):
	try:
		venue = Venue.objects.get(pk=venue_id)
	except VenuesModel.DoesNotExist:
            return HttpResponse('Exception: Data Not Found')
	return render(request, 'events/show_venue.html', {'venue':venue})

# ---------- SHOW EVENT ----------
def show_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	return render(request, 'events/show_event.html',{'event':event})

# ---------- SEARCH VENUE AND EVENT ----------
def search_any(request):
	if request.method == "POST":
		searched = request.POST['searched']
		if searched == "":
			return HttpResponseRedirect('/')
		else:
			venues = Venue.objects.filter(name__icontains=searched)
			events = Event.objects.filter(name__icontains=searched)
			return render(request, 'events/search.html',{'searched':searched,'venues':venues,'events':events})

# ---------- UPDATE VENUE ----------

def update_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	form = VenueForm(request.POST or None, instance=venue)
	if form.is_valid():
		form.save()
		return redirect('list-venue')
	return render(request, 'events/update_venue.html',{'venue':venue,'form':form})


