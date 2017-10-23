from django.contrib.auth.models import User

from django.shortcuts import render
from applications.academic_information.models import Student
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from applications.globals.models import ExtraInfo
from django.contrib.auth.models import User
from .models import (Feedback, Menu, Menu_change_request, Mess, Mess_meeting,
                                 Monthly_bill, Nonveg_data, Nonveg_menu, Payments, Rebate,
                                 Special_request, Vacation_food) 

def mess(request):
    
    x = Nonveg_menu.objects.all()
    context={
    'nonveg':x
    }
    return render(request, "messModule/mess.html", context)

def applynonveg(request):
    
    print("xyz")
    # x = Nonveg_menu.objects.all()
    # context={
    # 'nonveg':x
    # } this code works for Mess method but not applynonveg -->this method not called only.
    print("abc")
    return render(request, "messModule/nonvegfood.html", {'nonveg': '1'})