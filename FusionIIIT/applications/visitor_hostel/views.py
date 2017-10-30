from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from applications.visitor_hostel.models import *
from datetime import date
import datetime
from django.contrib import messages
from applications.visitor_hostel.forms import ViewBooking

def visitorhostel(request):
    context = {}
    print("gluqegurg")
    return render(request, "visitor_hostel/visitorhostel.html", context)
def vh_homepage(request):
    context = {}

    return render(request, "visitor_hostel/vh_homepage.html", context)

def booking_request(request):
    if request.method == 'POST' :
        if 'confirm' in request.POST:
            room_available = Room_Status.objects.filter(status="Available")
            if not room_available:
                messages.success(request, 'no room available')
                return HttpResponseRedirect('/visitorhostel/vh_homepage/')
            br_id = request.POST.getlist('confirm')
            br_id = br_id[0]
            book = Book_room.objects.all().filter(br_id=br_id).first()
            br_id = book.br_id
            print('book room', br_id)
            Book_room.objects.filter(br_id = br_id).update (status = "Confirm" )
            book_room = Book_room.objects.get(br_id=br_id)
            
            rooms=request.POST.getlist('room')
            
            for room in rooms:
                room_id=Room.objects.all().filter(room_number=room).first()
                print('room', room_id)
                book_from = book_room.booking_from
                book_to = book_room.Booking_to
                delta = (book_to - book_from).days
                print(delta)
                for i in range(delta):
                    date_1 = book_from+ datetime.timedelta(days=i)
                    p = Room_Status.objects.all().filter(room_id=room_id)
                    p = p[0]
                    p.date = date_1
                    p.status = 'Booked'
                    p.br_id = book
                    p.save()
                    #return HttpResponse('okay')
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
        print("hello")
        if not context:
            messages.success(request, 'No new request')
            return HttpResponseRedirect('/visitorhostel/vh_homepage/')
        return render(request, "visitor_hostel/vh_view_booking_request.html" ,{ 'context' : context , 'room' : room })


def all_booking(request):
    if request.method == 'POST' :
        print("hello")
        form = ViewBooking(request.POST)
        if form.is_valid:
            date_1=request.POST.getlist('date_from')[0]
            date_2=request.POST.getlist('date_to')[0]
            booking = Book_room.objects.filter(booking_from__gte=date_1 , Booking_to__lte = date_2 )
            print(booking)
            if not booking:
                messages.success(request, 'No booking available in that date')
                return HttpResponseRedirect('/visitorhostel/vh_homepage/')
            else :
                return render(request, "visitor_hostel/show_all_booking.html" , {'booking' : booking})
        return HttpResponseRedirect('/visitorhostel/vh_homepage/')
    else :
        print("hii")
        form = ViewBooking()
        return render(request, "visitor_hostel/input_booking_date.html" , { 'form' : form})


def cancel_booked_booking(request):
    if request.method == 'POST' :
        print("yes")
        br_id = request.POST.getlist('cancel')
        br_id = br_id[0]
        Book_room.objects.filter(br_id = br_id).update (status = "Cancel" )
        Room_Status.objects.filter(br_id=br_id).update(status = "Available")
        messages.success(request, 'cancelled successfully ')
        context = Book_room.objects.filter(status ="Confirm")
        return render(request, "visitor_hostel/cancel_booked_room.html" , { 'context' : context})
    else :
        context = Book_room.objects.filter(status = "Confirm")
        print(context)
        if not context:
            messages.success(request, 'No confirm booking available')
            return HttpResponseRedirect('/visitorhostel/vh_homepage/')
        return render(request, "visitor_hostel/cancel_booked_room.html" , { 'context' : context})


def check_in(request):
    if request.method =='POST' :
        br_id=request.POST.getlist('checkedin')[0]
        print(br_id)
        messages.success(request, 'check in succesfully')
        Book_room.objects.all().filter(br_id=br_id).update(check_in=datetime.datetime.today())
        Room_Status.objects.filter(br_id=br_id).update(status="CheckedIn")
        # code 
        book_room = Book_room.objects.all().filter(booking_from__lte=datetime.datetime.today())
        room_status = Room_Status.objects.all().filter(status='Booked')
        context1 = []
        for i in room_status:
            if i.br_id.booking_from<=datetime.date.today():
                context1.append(i.br_id)
        # print('Room', room_status)
        print(context1)
        context=[]
        for x in context1:
            if x not in context:
                context.append(x)
        print(context)

        if not context:
            messages.success(request, 'No booking available')
            return HttpResponseRedirect('/visitorhostel/vh_homepage/')
        return render(request, "visitor_hostel/checkin1.html" , { 'context' : context})
       
    else :
        book_room = Book_room.objects.all().filter(booking_from__lte=datetime.datetime.today())
        room_status = Room_Status.objects.all().filter(status='Booked').distinct()
        context1 = []
        for i in room_status:
            if i.br_id.booking_from<=datetime.date.today():
                context1.append(i.br_id)
        # print('Room', room_status)
        print(context1)
        context=[]
        for x in context1:
            if x not in context:
                context.append(x)
            # if i.br_id in b_room:
            #     r_status.append(i)
        print(context)

        #return HttpResponse('okay')
        #context = Book_room.objects.filter(br_id__in=Room_Status.objects.all().filter(status = "Booked"), booking_from__gte=datetime.datetime.today())
        #print(context)
        if not context:
            messages.success(request, 'No booking available')
            return HttpResponseRedirect('/visitorhostel/vh_homepage/')
        return render(request, "visitor_hostel/checkin1.html" , { 'context' : context})

def check_out(request):
    if request.method =='POST' :
        br_id=request.POST.getlist('checkedin')[0]
        book_room=Book_room.objects.all().filter(br_id=br_id)
        Book_room.objects.all().filter(br_id=br_id).update(check_out=datetime.datetime.today())
        Room_Status.objects.filter(br_id=br_id).update(status="Available",date='',br_id='')
        print("checkout")
    else :
        room_status=Room_Status.objects.filter(status = "CheckedIn")
        book_room = Book_room.objects.all().filter(Booking_to__lte=datetime.datetime.today())
        context1 = []
        for i in room_status:
            if i.br_id.booking_from<=datetime.date.today():
                context1.append(i.br_id)
        # print('Room', room_status)
        print(context1)
        context=[]
        for x in context1:
            if x not in context:
                context.append(x)
        print(context)
        if not context:
            messages.success(request, 'No guest checked in currently')
            return HttpResponseRedirect('/visitorhostel/vh_homepage/')
        return render(request, "visitor_hostel/checkout1.html" , { 'context' : context})
