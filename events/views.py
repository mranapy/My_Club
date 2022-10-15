from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime

# Create your views here.
def home(request, year, month):
	month = month.capitalize()
	# Convert month from name to number
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	# create a calendar
	cal = HTMLCalendar().formatmonth(year, month_number)
	now = datetime.now()
	current_year = now.year
	time = now.strftime('%I:%M %p')
	context = {
		'year': year,
		'month': month,
		'month_number':month_number,
		'cal':cal,
		'current_year':current_year,
		# 'now':now,
		'time':time,
	}
	return render(request, 'home.html', context)