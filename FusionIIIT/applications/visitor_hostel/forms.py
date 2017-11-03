from django import forms
from django.forms import ModelForm
from applications.visitor_hostel.models import *
import datetime


#class booking_request(forms.Form):
class ViewBooking(forms.Form):
	date_from = forms.DateField(initial=datetime.date.today)
	date_to = forms.DateField(initial=datetime.date.today)

class MealBooking(ModelForm):
	date = forms.DateField(initial=datetime.date.today)
	class Meta:
	        model = Meal
	        exclude = ['meal_date']

class RoomAvailability(forms.Form):
	date_from = forms.DateField(initial=datetime.date.today)
	date_to = forms.DateField(initial=datetime.date.today)