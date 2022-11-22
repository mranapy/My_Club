from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Venue Model
class Venue(models.Model):
	name = models.CharField(verbose_name='Venue name', max_length=120)
	address = models.CharField(max_length=300)
	zip_code = models.CharField('Zip Code',max_length=10,blank=True)
	phone = models.CharField('Contact phone',max_length=15,blank=True)
	web = models.URLField('Website address', blank=True)
	email = models.EmailField('Email address',blank=True)
	owner = models.PositiveIntegerField(verbose_name='Venue Owner', blank=False, default=1)
	book = models.BooleanField(default=False, blank=True)
	images = models.ImageField(upload_to='venue/images/',verbose_name='Upload Image')
	
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
	venue = models.ForeignKey(Venue, null=True, on_delete=models.CASCADE) # Many to One Relation
	# venue = models.CharField(max_length=60)
	manager = models.ForeignKey(User, blank=True,on_delete=models.CASCADE) # Many to one Relation
	description = models.TextField(blank=True)
	attendees = models.ManyToManyField(MyClubUser,blank=True) # Many to Many Relation
	# class Meta:
	# 	ordering = ('-event_date',)

	def clean(self):
		# self.name = self.name.capitalize()
		self.description = self.description.capitalize()
	def __str__(self):
		return self.name

	@property
	def Days_till(self):
		today = date.today()
		days_till = self.event_date.date() - today
		days_till_stipped = str(days_till).split(',',1)[0]
		return days_till_stipped

	@property
	def Is_Past(self):
		today = date.today()
		if self.event_date.date() < today:
			thing = "Past"
		else:
			thing = "Upcoming"
		return thing


