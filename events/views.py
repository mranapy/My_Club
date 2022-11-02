from django.shortcuts import render,redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .models import Event, Venue
from .forms import VenueForm,EventForm
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.db.models import Q # For icontains multiple search
import csv
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
	events = Event.objects.all().order_by('-event_date')
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

# ---------- UPDATE VENUE ----------

def update_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	form = VenueForm(request.POST or None, instance=venue)
	if form.is_valid():
		form.save()
		return redirect('list-venue')
	return render(request, 'events/update_venue.html',{'venue':venue,'form':form})

# ---------- Delete VENUE ----------
def deleteVenue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	venue.delete()
	return redirect('list-venue')

# ---------- Show VENUE ----------
def show_venue(request, venue_id):
	try:
		venue = Venue.objects.get(pk=venue_id)
	except VenuesModel.DoesNotExist:
            return HttpResponse('Exception: Data Not Found')
	return render(request, 'events/show_venue.html', {'venue':venue})


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


# ---------- SHOW EVENT ----------
def show_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	return render(request, 'events/show_event.html',{'event':event})

# ---------- Update an Event ----------
def update_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	form = EventForm(request.POST or None, instance=event)
	if form.is_valid():
		form.save()
		return redirect('list-events')
	return render(request, 'events/update_event.html',{'event':event,'form':form})

# ---------- Delete an EVENT ----------
def deleteEvent(request, event_id):
	event = Event.objects.get(pk=event_id)
	event.delete()
	return redirect('list-events')


# ---------- SEARCH VENUE AND EVENT ----------
def search_any(request):
	if request.method == "POST":
		searched = request.POST['searched']
		if searched == "":
			return HttpResponseRedirect('/')
		else:
			venues = Venue.objects.filter(Q(name__icontains=searched) | Q(address__icontains=searched))
			events = Event.objects.filter(name__icontains=searched)
			return render(request, 'events/search.html',{'searched':searched,'venues':venues,'events':events})

# Generate CSV File  for Venue
def venueCSV(request):
	results = HttpResponse(content_type="text/csv,charset=utf8")
	results['Content-Disposition'] = 'attachment; filename=venues.csv'
	# create csv file
	writer = csv.writer(results)

	# Deginate the Model
	venues = Venue.objects.all()
	# Add column heading csv file
	writer.writerow(['Venue Name', 'Address', 'Zip Code','Phone no.','Email Address', 'Web Address'])
	for venue in venues:
		writer.writerow([venue.name,venue.address,venue.zip_code,venue.phone,venue.email,venue.web])
	return results

# Generate Text File for Venue
def venueText(request):
    file_name = 'Venues.txt'
    lines = []
    venues = Venue.objects.all()
    for venue in venues:
       lines.append('{0};\n{1};\n{2};\n{3};\n{4};\n{5};\n'.format(venue.name,venue.address,venue.zip_code,venue.phone,venue.web,venue.email )+'\n')
    response_content = '\n'.join(lines)
    response = HttpResponse(response_content, content_type="text/plain,charset=utf8")
    response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
    return response


