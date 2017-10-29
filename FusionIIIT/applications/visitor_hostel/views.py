from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from applications.visitor_hostel.models import Visitor,Room_Status, Book_room,Visitor_bill,Room,Visitor_room,Meal,Inventory
from datetime import date
import datetime
from django.contrib import messages
from applications.visitor_hostel.forms import ViewBooking

def visitorhostel(request):
    context = {}

    return render(request, "vhModule/visitorhostel.html", context)

def vh_homepage(request):
	context = {}

	return render(request, "vhModule/vh_homepage.html", context)

def booking_request(request):
	if request.method == 'POST' :
		if 'confirm' in request.POST:
			room_available = room = Room_Status.objects.filter(status="Available")
			if not room_available:
				messages.success(request, 'no room available')
				return HttpResponseRedirect('/visitorhostel/vh_homepage/')
			br_id = request.POST.getlist('confirm')
			br_id = br_id[0]
			print(br_id)
			Book_room.objects.filter(br_id = br_id).update (status = "Confirm" )
			book_room = Book_room.objects.get(br_id = br_id)
			rooms=request.POST.getlist('room')
			print(rooms)
			for room in rooms:
				room_id=Room.objects.get(room_number=room)
				print(room_id)
				book_from = book_room.booking_from
				book_to = book_room.Booking_to
				delta = (book_to - book_from).days 
				print(delta)
				for i in range(delta):
					date_1 = book_from+ datetime.timedelta(days=i)
					Room_Status.objects.filter(room_id = room_id).update(date=date_1 , status="Booked", br_id=br_id)
					print("hello")
			messages.success(request, 'you allot room succesfully')
			return HttpResponseRedirect('/visitorhostel/vh_homepage/')

		elif 'cancel' in request.POST:
			print ("hello")
			messages.success(request, 'succesfully cancelled')
			return HttpResponseRedirect('/visitorhostel/vh_homepage/')

		return HttpResponseRedirect('/visitorhostel/vh_homepage/')		

	else :
		context = Book_room.objects.filter(status = "Pending")
		room = Room_Status.objects.filter(status="Available")
		print(room)
		print("hello")
		if not context:
			messages.success(request, 'No new request')
			return HttpResponseRedirect('/visitorhostel/vh_homepage/')
		return render(request, "vhModule/vh_view_booking_request.html" ,{ 'context' : context , 'room' : room })
		

def all_booking(request):
	if request.method == 'POST' :
		print("hello")
		form = ViewBooking(request.POST)
		if form.is_valid:
			date_1=request.POST.getlist('date_from')[0]
			date_2=request.POST.getlist('date_to')[0]
			booking = Book_room.objects.filter(booking_from__gt=date_1 , Booking_to__lt = date_2 )
			print(booking)
			if not booking:
				messages.success(request, 'No booking available in that date')
				return HttpResponseRedirect('/visitorhostel/vh_homepage/')
			else :
				return render(request, "vhModule/show_all_booking.html" , {'booking' : booking})
		return HttpResponseRedirect('/visitorhostel/vh_homepage/')
	else :
		print("hii")
		form = ViewBooking()
		return render(request, "vhModule/input_booking_date.html" , { 'form' : form})


def cancel_booked_booking(request):
	if request.method == 'POST' :
		print("yes")
		br_id = request.POST.getlist('cancel')
		br_id = br_id[0]
		Book_room.objects.filter(br_id = br_id).update (status = "Cancel" )
		Room_Status.objects.filter(br_id=br_id).update(status = "Available")
		messages.success(request, 'cancelled successfully ')
		context = Book_room.objects.filter(status =True)
		return render(request, "vhModule/cancel_booked_room.html" , { 'context' : context})
	else :
		context = Book_room.objects.filter(status = "Confirm")
		print(context)
		if not context:
			messages.success(request, 'No confirm booking available')
			return HttpResponseRedirect('/visitorhostel/vh_homepage/')
		return render(request, "vhModule/cancel_booked_room.html" , { 'context' : context})


def check_in(request):
	if request.method =='POST' :
		print("checkin")
		messages.success(request, 'check in succesfully')
		Room_Status.objects.filter(br_id=request.POST.getlist('checkedin')[0]).update(status="CheckedIn")
		context = Book_room.objects.filter(br_id__in=Room_Status.objects.filter(status = "Booked", date__gte=datetime.datetime.today()))
		if not context:
			messages.success(request, 'No booking available')
			return HttpResponseRedirect('/visitorhostel/vh_homepage/')
		return render(request, "vhModule/checkin1.html" , { 'context' : context})
	else :
		context = Book_room.objects.filter(br_id__in=Room_Status.objects.filter(status = "Booked", date__gte=datetime.datetime.today()))
		visitor_id = context
		if not context:
			messages.success(request, 'No booking available')
			return HttpResponseRedirect('/visitorhostel/vh_homepage/')
		return render(request, "vhModule/checkin1.html" , { 'context' : context})

def check_out(request):
	if request.method == 'POST':
		print("check_out")
	else
		context = Book_room.objects.filter(br_id__in=Room_Status.objects.filter(status = "CheckedIn", date__gte=datetime.datetime.today()))
		if not context:
			messages.success(request, 'No booking available')
			return HttpResponseRedirect('/visitorhostel/vh_homepage/')
		return render(request, "vhModule/checkin1.html" , { 'context' : context})
