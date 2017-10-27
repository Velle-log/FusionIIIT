from django import forms
import datetime

#class booking_request(forms.Form):
class ViewBooking(forms.Form):
	date_from = forms.DateField(initial=datetime.date.today)
	date_to = forms.DateField(initial=datetime.date.today)