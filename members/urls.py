from django.urls import path
from . import views


urlpatterns = [
	path('login_user/', views.memberLogin, name='login'),
	path('signup_user/', views.memberSignup, name='signup'),
	path('logout_user/', views.memberLogout, name='logout'),
]