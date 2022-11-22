from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('<int:year>/<str:month>/', views.home, name="home"),
    path('events/', views.all_events, name='list-events'),
    path('upcoming-events/', views.futurEvents, name='upcoming-events'),
    path('past-events/', views.pastEvent, name='past-events'),
    path('venues/', views.all_venues, name='list-venue'),
    path('add-venue/', views.add_venue, name='add-venue'),
    path('update-venue/venuid-<venue_id>/', views.update_venue, name='update-venue'),
    path('delete-venue/venuid-<venue_id>/', views.deleteVenue, name='delete-venue'),
    path('show-venue/venuid?<venue_id>/', views.show_venue, name='show-venue'),


    path('show-event/eventid<int:event_id>/', views.show_event, name='show-event'),
    path('add-event/', views.addEvent, name='add-event'),
    path('update-event/eventid-<event_id>/', views.update_event, name='update-event'),
    path('delete-event/eventid-<event_id>/', views.deleteEvent, name='delete-event'),
    path('searchany/', views.search_any, name='searchany'),
    path('my-events/', views.myEvents, name='my-events'),
    # path('venues/',views.VenueList.as_view(), name='list-venue'),

    # Generate txt, csv & pdf File
    path('venue_text/', views.venueText, name='venue-text'),
    path('venue_csv/', views.venueCSV, name='venue-csv'),
    path('venue_pdf/', views.venuePdf, name='venue-pdf'),

    # Generate txt File
    path('event_text/', views.EventText, name='event-text'),
    
]