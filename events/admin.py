from django.contrib import admin
from . models import Venue, MyClubUser, Event
# Register your models here.

# admin.site.register(Venue)
admin.site.register(MyClubUser)
# admin.site.register(Event)
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin): # For backend 
	list_display = ('name','address')
	# ordering = ('name',)
	search_fields = ('name','address')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin): # For backend 
	fields = (('name','venue'),'event_date','description','manager','approved')
	list_display = ('name','event_date','venue')
	list_filter = ('event_date','venue')
	# ordering = ('event_date',)
	search_fields = ('name','address')