from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .models import Event, Venue
from .forms import VenueForm,EventForm, EventFormAdmin
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect,HttpResponse,FileResponse
# Import For Multiple search
from django.db.models import Q # For icontains multiple search
# Import for CSV
import csv
# Import paginator stuff
from django.core.paginator import Paginator

# For Upcoming & Past Events
from django.utils import timezone
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
	event_list = Event.objects.filter(
			event_date__year = year,
			event_date__month = month_number,
		)
	# time = now.strftime('%I:%M %p')
	context = {
		'year': year,
		'month': month,
		'month_number':month_number,
		'cal':cal,
		'current_year':current_year,
		# 'now':now,
		# 'time':time,
		'event_list':event_list,
	}
	return render(request, 'events/home.html', context)
 

# class VenueList(ListView):
# 	model = Event
# 	template_name = 'events/venue_list.html'
# 	context_object_name = 'venues'
# 	ordering = {'name'}

# ---------- SHOW ALL VENUE ----------
def all_venues(request):
	# venues = Venue.objects.all().order_by('?') # Random List View
	venue_count = Venue.objects.all().count()

	# Setup pagination
	p = Paginator(Venue.objects.all().order_by('name'),2)
	page = request.GET.get('page')
	venues = p.get_page(page)
	nums = "a" * venues.paginator.num_pages
	# context = {'venue_list':venue_list}
	return render(request, 'events/venue_list.html', {'venues':venues,'nums':nums,'venue_count':venue_count})

# ---------- ADD VENUE ----------

# @login_required
def add_venue(request):
	if request.user.is_authenticated:
		submitted = False
		if request.method == "POST":
			venueform = VenueForm(request.POST, request.FILES)
			if venueform.is_valid():
				venue = venueform.save(commit=False)
				venue.owner = request.user.id  # Logged in user
				venue.save()
				submitted = True
				return HttpResponseRedirect('/add-venue?submitted=True')
		else:
			venueform = VenueForm()
			if 'submitted' in request.GET:
				submitted = True
		return render(request, 'events/add_venue.html',{'venueform':venueform,'submitted':submitted})
	else:
		return redirect('login')
# ---------- UPDATE VENUE ----------

def update_venue(request, venue_id):
	if request.user.is_authenticated:
		venue = Venue.objects.get(pk=venue_id)
		form = VenueForm(request.POST or None, request.FILES or None ,instance=venue)
		if form.is_valid():
			form.save()
			return redirect('list-venue')
		return render(request, 'events/update_venue.html',{'venue':venue,'form':form})
	else:
		return redirect('login')

# ---------- Delete VENUE ----------
def deleteVenue(request, venue_id):
	if request.user.is_authenticated:
		venue = Venue.objects.get(pk=venue_id)
		venue.delete()
		return redirect('list-venue')
	return redirect('login')

# ---------- Show VENUE ----------
def show_venue(request, venue_id):
	try:
		venue = Venue.objects.get(pk=venue_id)
		venue_owner = Venue.objects.get(pk=venue.owner)
		# Grab the events from that vanue
		# events = Event.objects.event_set.all()

		
	except VenuesModel.DoesNotExist:
            return HttpResponse('Exception: Data Not Found')
	return render(request, 'events/show_venue.html', {'venue':venue,'venue_owner':venue_owner})


# ---------- ADD EVENT ----------
def addEvent(request):
	if request.user.is_authenticated:
		submitted = False
		if request.method == "POST":
			if request.user.is_superuser:
				eventform = EventFormAdmin(request.POST)
				if eventform.is_valid():
					eventform.save()
					submitted = True
					# return redirect('list-events')
					return HttpResponseRedirect('/add-event?submitted=True')
			else:
				eventform = EventForm(request.POST)
				if eventform.is_valid():
					event = eventform.save(commit=False)
					event.manager = request.user  # Logged in user
					event.save()
					submitted = True
					return HttpResponseRedirect('/add-event?submitted=True')
		else:
			if request.user.is_superuser:
				eventform = EventFormAdmin()
			else:
				eventform = EventForm()
			if 'submitted' in request.GET:
				submitted = True
		return render(request, 'events/add_event.html',{'eventform':eventform,'submitted':submitted})
	else:
		return redirect('login')

# Venue Events
def venueEvents(request,venue_id):
	# Grab the venue
	venue = Venue.objects.get(id=venue_id)
	#Grab the events from that venue
	events = venue.event_set.all()
	if events:
		return render(request,'events/venue-events.html',{'events':events})
	else:
		messages.success(request,"That Venue Has No Events At This Time..!")
		return redirect('admin-approval')

# ---------- Admin Approval Events ----------
def AdminApproval(request):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			venue_count = Venue.objects.all().count()
			venue_list = Venue.objects.all().order_by('name')
			events_list = Event.objects.all().order_by('-event_date')
			event_count = Event.objects.all().count()
			user_count = User.objects.all().count()

			if request.method == "POST":
				id_list = request.POST.getlist('boxes')
				# print(id_list)
				# Unchecked list
				events_list.update(approved=False)
				# Update database
				for x in id_list:
					Event.objects.filter(pk=int(x)).update(approved=True)

				messages.success(request,"Event approved update successfully..!")
				return redirect('list-events')
			else:
				context = {
					'venue_count':venue_count,
					'venue_list':venue_list,
					'events_list':events_list,
					'event_count':event_count,
					'user_count':user_count
				}
				return render(request, 'events/admin-approval.html',context)
		else:
			messages.success(request,'You are not Superuser...')
	else:
		return redirect('login')

# ---------- SHOW ALL EVENT ----------
def all_events(request):
	event_count = Event.objects.all().count()
	today = timezone.now()
	events = Event.objects.all().order_by('event_date')

	context = {
		'events': events,
		'event_count':event_count,
	}
	return render(request, 'events/events_list.html', context)

def futurEvents(request):
	today = timezone.now()
	future_events = Event.objects.filter(event_date__gte=today).order_by('event_date')
	return render(request, 'events/upcoming-events.html', {'future_events':future_events})

def pastEvent(request):
	today = timezone.now()
	past_events = Event.objects.filter(event_date__lt=today).order_by('-event_date')
	return render(request, 'events/past-events.html', {'past_events':past_events})
# ---------- SHOW EVENT ----------
def show_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	return render(request, 'events/show_event.html',{'event':event})

# ---------- Update an Event ----------
def update_event(request, event_id):
	if request.user.is_authenticated:
		event = Event.objects.get(pk=event_id)
		if request.user.is_superuser:
			form = EventFormAdmin(request.POST or None, instance=event)
		else:
			form = EventForm(request.POST or None, instance=event)
		if form.is_valid():
			form.save()
			return redirect('list-events')
		return render(request, 'events/update_event.html',{'event':event,'form':form})
	else:
		return redirect('login')

# ---------- Delete an EVENT ----------
def deleteEvent(request, event_id):
	if request.user.is_authenticated:
		event = Event.objects.get(pk=event_id)
		event.delete()
		messages.success(request,"This Event Delete Successfully..!")
		return redirect('list-events')
	else:
		return redirect('login')


# Generate Text File for Event
def EventText(request):
	if request.user.is_authenticated:
		file_name = 'events.txt'
		lines = []
		events = Event.objects.all()
		for event in events:
			lines.append('{0};\n{1};\n{2};\n{3};\n{4};\n'.format(event.name,event.event_date,event.venue,event.manager,event.description )+'\n')
			response_content = '\n'.join(lines)
		response = HttpResponse(response_content, content_type="text/plain,charset=utf8")
		response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
		return response
	else:
		return redirect('login')
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

# Generate Text File for Venue
# def venueText(request):
# 	lines = []
# 	# Deginate the Model
# 	venues = Venue.objects.all()
# 	for venue in venues:
# 		lines.append(f'{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.email}\n{venue.web}\n\n')
# 	results = writelines().join(lines)
# 	results = HttpResponse(content_type="text/plain,charset=utf8")
# 	results['Content-Disposition'] = 'attachment; filename=venues.txt'
# 	return results

# Generate Text File for Venue
def venueText(request):
	if request.user.is_authenticated:
		file_name = 'venues.txt'
		lines = []
		venues = Venue.objects.all()
		for venue in venues:
			lines.append('{0};\n{1};\n{2};\n{3};\n{4};\n{5};\n'.format(venue.name,venue.address,venue.zip_code,venue.phone,venue.web,venue.email )+'\n')
			response_content = '\n'.join(lines)
		response = HttpResponse(response_content, content_type="text/plain,charset=utf8")
		response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
		return response
	else:
		return redirect('login')


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

# Generate a PDF File Venue List
# import io
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import inch
# from reportlab.lib.pagesizes import letter

# def venuePdf(request):
# 	# Create Bytestream Buffer
# 	buf = io.BytesIO()
# 	# create a canvas
# 	c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
# 	# create a text object
# 	textob = c.beginText()
# 	textob.setTextOrigin(inch,inch)
# 	textob.setFont("Helvetica",14)

# 	# Add some lines of text
# 	# lines = ['line1','line2','line3']
# 	# Design the venue model
# 	venues = Venue.objects.all()
# 	# create blank list
# 	lines = []
# 	for venue in venues:
# 		# lines.append(venue.name,venue.address,venue.zip_code,venue.phone,venue.email,venue.web)
# 		lines.append(venue.name)
# 		lines.append(venue.address)
# 		lines.append(venue.zip_code)
# 		lines.append(venue.phone)
# 		lines.append(venue.email)
# 		lines.append(venue.web)
# 		lines.append(" ")

# 	for line in lines:
# 		textob.textLine(line)
# 	# Finish UP
# 	c.drawText(textob)
# 	c.showPage()
# 	c.save()
# 	buf.seek(0)

# 	return FileResponse(buf, as_attachment=True, filename='venue.pdf')

 # Generate a PDF File Venue List (another way)
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
def venuePdf(request):
	if request.user.is_authenticated:
		template_path = 'events/venuepdf.html'
		# context = {'myvar': 'this is your template context'}
		venuespdf = Venue.objects.all()
		context = {'venuespdf':venuespdf}
		# Create a Django response object, and specify content_type as pdf
		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = ' filename="venues-list.pdf"'
		# find the template and render it.
		template = get_template(template_path)
		html = template.render(context)

		# create a pdf
		pisa_status = pisa.CreatePDF(html, dest=response)
		# if error then show some funny view
		if pisa_status.err:
			return HttpResponse('We had some errors <pre>' + html + '</pre>')
		return response
	else:
		return redirect('login')

def myEvents(request):
	if request.user.is_authenticated:
		# me = request.user
		events = Event.objects.all()
		return render(request, 'events/my_events.html',{'events':events})
	else:
		messages.success(request,'You have no Events..')
		return HttpResponseRedirect('list-events')