from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('<int:year>/<str:month>/', views.home, name="home"),
    path('events/', views.all_events, name='list-events'),
    path('venues/', views.all_venues, name='list-venue'),
    path('add-venue/', views.add_venue, name='add-venue'),
    path('show-venue/venuid?<venue_id>/', views.show_venue, name='show-venue'),
    # path('venues/',views.VenueList.as_view(), name='list-venue'),
    
]