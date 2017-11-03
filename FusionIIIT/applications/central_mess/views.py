import datetime

# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render

from applications.academic_information.models import Student
from applications.globals.models import ExtraInfo

from .models import Feedback, Menu, Nonveg_data, Nonveg_menu, Vacation_food


def mess(request):
    extrainfo = ExtraInfo.objects.get(id='2015034')
    student = Student.objects.get(id=extrainfo)
    vaca_obj = Vacation_food.objects.filter(student_id=student)
    feedback_obj = Feedback.objects.filter(student_id=student)
    data = Nonveg_data.objects.filter(student_id=student)
    y = Menu.objects.all()
    x = Nonveg_menu.objects.all()

    context = {
               'menu': y,
               'nonveg': x,
               'vaca': vaca_obj,
               'info': extrainfo,
               'feedback': feedback_obj,
               'student': student,
               'data': data
    }
    return render(request, "messModule/mess.html", context)


def applynonveg(request):
    x = Nonveg_menu.objects.all()
    context = {
               'nonveg': x
    }
    return render(request, "messModule/nonvegfood.html", context)


# @login_required
@transaction.atomic
def placeorder(request):
    # user = request.user
    extrainfo = ExtraInfo.objects.get(id='2015034')
    # if extrainfo.user_type == 'student':
    student = Student.objects.get(id=extrainfo)
    # stu=Mess.objects.get(student=student) check for nonvegmess
    print(request.POST.get("dish"))
    dish = Nonveg_menu.objects.get(dish=request.POST.get("dish"))
    order_interval = dish.order_interval
    order_date = datetime.datetime.now().date()
    nonveg_obj = Nonveg_data(student_id=student, order_date=order_date,
                             order_interval=order_interval, dish=dish)
    nonveg_obj.save()

    return HttpResponse("data added to nonveg data")
    # return render(request,'mess.html',context)

    # else:
    #     message = "you can't apply for this application.
    #     context={
    #     'message': message
    #     }

    #     return render(request,'mess.html',context)
    # else:
    #     return redirect('globals:dashboard')


@transaction.atomic
def submit(request):
    extrainfo = ExtraInfo.objects.get(id='2015034')
    student = Student.objects.get(id=extrainfo)
    fdate = datetime.datetime.now().date()
    description = request.POST.get('description')
    print(description)
    feedback_type = request.POST.get('feedback_type')
    print(feedback_type)
    feedback_obj = Feedback(student_id=student, fdate=fdate,
                            description=description,
                            feedback_type=feedback_type)

    feedback_obj.save()
    return HttpResponse("data added to feedback table")


@transaction.atomic
def vacasubmit(request):
    extrainfo = ExtraInfo.objects.get(id='2015034')
    student = Student.objects.get(id=extrainfo)
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    purpose = request.POST.get('purpose')
    vaca_obj = Vacation_food(student_id=student, start_date=start_date,
                             end_date=end_date, purpose=purpose)

    vaca_obj.save()
    return HttpResponse("data added to vacation food table")

# def bill(request):
#     extrainfo = ExtraInfo.objects.get(id='2015034')
#     student = Student.objects.get(id=extrainfo)
#     # stu=Mess.objects.get(student=student)
#     # if stu.mess_option='mess1'
#     # add nonveg
#     data = Nonveg_data.objects.filter(student_id=student)
#     amount = 0
#     nonveg_total_bill = 0
#     for i in data:
#         nonveg_total_bill += i.price
#     rebate_count = Rebate.objects.filter(student_id=student)
#     foodforvaca = Vacation_food.objects.filter(student_id=student)
#     monthly_bill = Monthly_bill.objects.filter(student_id=student)
#     amount = monthly_bill.amount + nonveg_total_bill

# @transaction.atomic
# def menusubmit(request):
#     # user = request.user
#     # extrainfo = ExtraInfo.objects.get(user=user)
#     # if extrainfo.designation == 'mess convener':
#     dish = Menu.objects.get(dish=request.POST.get("dish"))
#     request = request.POST.get("request")
#     # app_date = datetime.datetime.now().date() first update changes in models
#     app_obj = Menu_change_request(dish=dish,request=request)
#     app_obj.save()

#     return HttpResponse("data added to menu change request")