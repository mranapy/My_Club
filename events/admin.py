from django.contrib import admin
from . models import Venue, MyClubUser, Event
# Register your models here.

# admin.site.register(Venue)
admin.site.register(MyClubUser)
admin.site.register(Event)
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
	list_display = ('name','address')
	# ordering = ('name',)