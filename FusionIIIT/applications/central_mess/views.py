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
    
    
   

    context={
    
    
    }
    return render(request, "messModule/mess.html", context)

# @login_required
# def submit(request):

#         user = request.user
#         extrainfo = ExtraInfo.objects.get(user=user)

#         if extrainfo.user_type == 'student':
#             student = Student.objects.get(id=extrainfo)

#             stu=Mess.objects.get(student=student)
#                 if stu.mess_option == 'mess1':

#                     order_date=datetime.datetime.now().date()
                    
#                     nonveg_obj=Nonveg_data(student_id=student,order_date=order_date,order_interval=request.POST.get('order_interval'),dish=request.POST.get('dish'))
        
        

        
        
       
#             if mess_option = 'mess2':
#                 message = "you can't apply for this application., Facility available for Nonveg Mess students"
#                 context={
#                 'message': message
#                 }

#             return render(request,'mess.html',context)

#             else:
#                 nonveg_obj.save()   

#         else:
#             return redirect('globals:dashboard')


def applynonveg(request):
    
    print("xyz")
    x = Nonveg_menu.objects.all()
    context={
    'nonveg':x
    } 
    print("abc")
    return render(request, "messModule/nonvegfood.html", context)

def viewmenu(request):
    y = Menu.objects.all()
    context={
    'menu':y
    }
    return render(request, "messModule/views.html", context)