from django.db import models
from django.contrib.auth.models import User

# Venue Model
class Venue(models.Model):
	name = models.CharField('Venue name', max_length=120)
	address = models.CharField(max_length=300)
	zip_code = models.CharField('Zip Code',max_length=10,blank=True)
	phone = models.CharField('Contact phone',max_length=15,blank=True)
	web = models.URLField('Website address', blank=True)
	email = models.EmailField('Email address',blank=True)
	owner = models.PositiveIntegerField(verbose_name='Venue Owner', blank=False, default=1)
	book = models.BooleanField(default=False, blank=True)
	
	def clean(self):
		self.name = self.name.capitalize()
	

	# class Meta:
	# 	ordering = ('name',)
	def __str__(self):
		return self.name

# MyClub User
class MyClubUser(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.EmailField('User email')

	def __str__(self):
		return self.first_name + ' ' + self.last_name

# Event Model
class Event(models.Model):
	name = models.CharField('Event name', max_length=120)
	event_date = models.DateTimeField('Event date')
	venue = models.ForeignKey(Venue, null=True, on_delete=models.CASCADE)
	# venue = models.CharField(max_length=60)
	manager = models.ForeignKey(User, blank=True,on_delete=models.CASCADE)
	description = models.TextField(blank=True)
	attendees = models.ManyToManyField(MyClubUser,blank=True)
	# class Meta:
	# 	ordering = ('event_date',)

	def clean(self):
		# self.name = self.name.capitalize()
		self.description = self.description.capitalize()
	def __str__(self):
		return self.name



