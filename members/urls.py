from django.urls import path
from . import views


urlpatterns = [
	path('login_user/', views.membersAdd, name='login'),
	path('signup_user/', views.membersSignup, name='signup'),
	path('logout_user/', views.membersLogout, name='logout'),
]