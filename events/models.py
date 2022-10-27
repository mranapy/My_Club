from django.db import models


# Venue Model
class Venue(models.Model):
	name = models.CharField('Venue name', max_length=120)
	address = models.CharField(max_length=300)
	zip_code = models.CharField('Zip Code',max_length=10,blank=True)
	phone = models.CharField('Contact phone',max_length=15,blank=True)
	web = models.URLField('Website address', blank=True)
	email = models.EmailField('Email address',blank=True)

	class Meta:
		ordering = ('name',)
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
	manager = models.CharField(max_length=120)
	description = models.TextField(blank=True)
	attendees = models.ManyToManyField(MyClubUser,blank=True)
	class Meta:
		ordering = ('event_date',)
	def __str__(self):
		return self.name



