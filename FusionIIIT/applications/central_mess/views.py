from __future__ import unicode_literals

# import os
# import datetime
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import PermissionsMixin, User
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from .models import Rebate
from applications.globals.models import ExtraInfo
from applications.academic_information.models import Student


def mess(request):
    extrainfo = ExtraInfo.objects.get(id='2015268')
    student = Student.objects.get(id=extrainfo)
    rebates = Rebate.objects.filter(student_id=student)
    return render(request, 'messModule/mess.html', {'rebates': rebates})


# @login_required
@transaction.atomic
def leaverequest(request):
    # user = request.user
    extrainfo = ExtraInfo.objects.get(id='2015268')
    # if extrainfo.user_type == 'student'
    student = Student.objects.get(id=extrainfo)
    leave_type = request.POST.get('leave_type')
    start_date = '2017-10-29'  # request.POST.get('start_date')
    end_date = '2017-10-31'  # request.POST.get('end_date')
    purpose = request.POST.get('purpose')
    rebate_obj = Rebate(student_id=student, leave_type=leave_type, start_date=start_date,
                        end_date=end_date, purpose=purpose)
    rebate_obj.save()
    return HttpResponse("Leave Request made!")
