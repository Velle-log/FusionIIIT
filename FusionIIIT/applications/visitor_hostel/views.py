from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from applications.visitor_hostel.models import Visitor,Book_room,Visitor_bill,Room,Visitor_room,Meal,Inventory

def visitorhostel(request):
    context = {}

    return render(request, "vhModule/visitorhostel.html", context)

def vh_homepage(request):
	context = {}

	return render(request, "vhModule/vh_homepage.html", context)

def booking_request(request):
	if request.method == 'POST' :
		if 'confirm' in request.POST:
			br_id = request.POST.getlist('confirm')
			br_id = br_id[0]
			print(br_id)
			Book_room.objects.filter(br_id = br_id).update (status = True )
			Redirect('/visitorhostel/vh_homepage/')
		elif 'cancel' in request.POST:
			print ("hello")
			Redirect('/visitorhostel/vh_homepage/')
    		

	else :
		context = Book_room.objects.filter(status = False)
		room = Room.objects.filter(room_status = "available")
		
		return render(request, "vhModule/vh_view_booking_request.html" ,{ 'context' : context , 'room' : room })
		