# from django.shortcuts import render

from django.shortcuts import render
from .models import Student
from applications.globals.models import ExtraInfo, Designation, DepartmentInfo
from django.http import HttpResponse
from django.db.models.query import QuerySet
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


def homepage(request):
    try:
        s = Designation.objects.get(name = 'senate')
        senates = ExtraInfo.objects.filter(designation = s)
        students = Student.objects.filter(id__in = senates)
        
    except:
        senates = ""
        students = ""
        pass
        
    context = {
         'senates':senates,
         'students':students,
    }
    
    return render(request, "ais/ais.html", context)

@csrf_exempt
def senate(request):    
    if request.method == 'POST':
        rollno = request.POST.get('rollno')
        s = Designation.objects.get(name = 'senate')
        extraInfo = ExtraInfo.objects.get(id = rollno)
        extraInfo.designation.add(s)
        extraInfo.save()
        student = Student.objects.get(id = extraInfo)
        data = {
            'name' : extraInfo.user.username,
            'rollno' : extraInfo.id,
            'programme' : student.programme,
            'branch' : extraInfo.department.name
        }
        return JsonResponse(data)
    else:        
        data = {}
        return JsonResponse(data)


