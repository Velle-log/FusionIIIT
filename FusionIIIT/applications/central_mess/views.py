from __future__ import unicode_literals

# import os
# import time
# import datetime
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import PermissionsMixin, User
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from applications.academic_information.models import Student
from applications.globals.models import ExtraInfo

from .forms import MinuteForm
from .models import (Feedback, Mess_meeting, Mess_minutes, Rebate,
                     Special_request)


@login_required
def mess(request):
    user = request.user
    extrainfo = ExtraInfo.objects.get(user=user)
    form = MinuteForm()

    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0

    if extrainfo.user_type == 'student':
        type = 'student'
        student = Student.objects.get(id=extrainfo)
        designation = extrainfo.designation.name
        rebates = Rebate.objects.filter(student_id=student)
        meeting = Mess_meeting.objects.all()
        minutes = Mess_minutes.objects.all()
        feedback = Feedback.objects.all()
        sprequest = Special_request.objects.filter(status='1')
        splrequest = Special_request.objects.all()
        count = 0

        for item in rebates:
            d1 = item.start_date
            d2 = item.end_date
            item.duration = abs((d2 - d1).days)+1
            item.save()

        for items in rebates:
            if items.leave_type == 'casual':
                count += item.duration
        for f in feedback:
            if f.feedback_type == 'maintenance':
                count1 += 1
            elif f.feedback_type == 'food':
                count2 += 1
            elif f.feedback_type == 'cleanliness':
                count3 += 1
            else:
                count4 += 1

        return render(request, 'messModule/mess.html', {'count': count, 'rebates': rebates,
                                                        'type': type, 'designation': designation,
                                                        'feedback': feedback, 'meeting': meeting,
                                                        'minutes': minutes, 'sprequest': sprequest,
                                                        'splrequest': splrequest, 'count1': count1,
                                                        'count2': count2, 'count3': count3,
                                                        'count4': count4, 'form': form})
    elif extrainfo.user_type == 'staff':
        type = 'mess manager'
        leave = Rebate.objects.filter(status='1')
        return render(request, 'messModule/mess.html', {'type': type, 'leave': leave})

    elif extrainfo.user_type == 'faculty':
        type = 'mess warden'
        meeting = Mess_meeting.objects.all()
        minutes = Mess_minutes.objects.all()
        feedback = Feedback.objects.all()

        for f in feedback:
            if f.feedback_type == 'maintenance':
                count1 += 1
            elif f.feedback_type == 'food':
                count2 += 1
            elif f.feedback_type == 'cleanliness':
                count3 += 1
            else:
                count4 += 1
        return render(request, 'messModule/mess.html', {'type': type, 'meeting': meeting,
                                                        'minutes': minutes, 'count1': count1,
                                                        'count2': count2, 'count3': count3,
                                                        'count4': count4, 'form': form})


@transaction.atomic
@csrf_exempt
def leaverequest(request):
    user = request.user
    extrainfo = ExtraInfo.objects.get(user=user)
    student = Student.objects.get(id=extrainfo)
    leave_type = request.POST.get('leave_type')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    purpose = request.POST.get('purpose')
    rebate_obj = Rebate(student_id=student, leave_type=leave_type, start_date=start_date,
                        end_date=end_date, purpose=purpose)
    rebate_obj.save()
    data = {
            'status': 1,
            # 'table': Rebate.objects.all(),
    }
    return JsonResponse(data)


@login_required
@transaction.atomic
def minutes(request):
    if request.method == 'POST' and request.FILES:
        form = MinuteForm(request.POST, request.FILES)
        print('Hey')
        if form.is_valid():
            form.save()
            return HttpResponse('success')
        else:
            return HttpResponse("not uploaded")


@transaction.atomic
def invitation(request):
    date = request.POST.get('date')
    venue = request.POST.get('venue')
    agenda = request.POST.get('agenda')
    time = request.POST.get('time')
    invitation_obj = Mess_meeting(meeting_date=date, agenda=agenda, venue=venue, meeting_time=time)

    invitation_obj.save()
    return HttpResponseRedirect("/mess")


def response(request, ap_id):
    leaves = Rebate.objects.get(pk=ap_id)

    if(request.POST.get('submit') == 'approve'):
        leaves.status = '2'

    else:
        leaves.status = '0'
    leaves.save()
    return HttpResponseRedirect("/mess")


def placerequest(request):
    user = request.user
    extrainfo = ExtraInfo.objects.get(user=user)
    if extrainfo.user_type == 'student':
        extrainfo = ExtraInfo.objects.get(user=user)
        student = Student.objects.get(id=extrainfo)
        fr = request.POST.get("from")
        to = request.POST.get("to")
        food1 = request.POST.get("food1")
        food2 = request.POST.get("food2")
        purpose = request.POST.get("purpose")

        spfood_obj = Special_request(student_id=student, start_date=fr, end_date=to,
                                     item1=food1, item2=food2, request=purpose)
        spfood_obj.save()
        return HttpResponseRedirect("/mess")


def responses(request, ap_id):
    sprequest = Special_request.objects.get(pk=ap_id)
    if(request.POST.get('submit') == 'approve'):
        sprequest.status = '2'
    else:
        sprequest.status = '0'

    sprequest.save()
    return HttpResponseRedirect("/mess")
