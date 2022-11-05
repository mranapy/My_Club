from django.urls import path
from . import views


urlpatterns = [
	path('login_user/', views.membersAdd, name='login'),
]