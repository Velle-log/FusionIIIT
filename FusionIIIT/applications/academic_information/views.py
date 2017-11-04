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
        v = Designation.objects.get(name = 'Convenor')
        t = Designation.objects.get(name = 'Co Convenor')   
        senates = ExtraInfo.objects.filter(designation = s)
        Convenor = ExtraInfo.objects.filter(designation = v)
        CoConvenor = ExtraInfo.objects.filter(designation = t)
        students = Student.objects.filter(id__in = senates)
        
    except:
        senates = ""
        students = ""
        Convenor = ""
        CoConvenor = ""
        pass
        
    context = {
         'senates':senates,
         'students':students,
         'Convenor':Convenor,
         'CoConvenor':CoConvenor,
    }    
    return render(request, "ais/ais.html", context)

def delete(request):
   s = Designation.objects.get(name = "senate")
   student = ExtraInfo.objects.get(id = request.POST["delete"])
   student.designation.remove(s)
   return HttpResponse("Deleted")

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

def edit_convenor(request):
    s = Designation.objects.get(name = 'Convenor')
    p = Designation.objects.get(name = 'Co Convenor')
    if request.method == 'POST':
        extraInfo = ExtraInfo.objects.get(id = request.POST["Roll Number"])
        result = request.POST["Designation"]
        if result == "Convenor":
           extraInfo.designation.add(s)
           extraInfo.save()
        else:
           extraInfo.designation.add(p)
           extraInfo.save()
    return HttpResponse("Data Inputed")

def delete1(request):
   s = Designation.objects.get(name = "Convenor")
   student = ExtraInfo.objects.get(id = request.POST["delete"])
   student.designation.remove(s)
   return HttpResponse("Deleted")

def delete2(request):
   s = Designation.objects.get(name = "CoConvenor")
   student = ExtraInfo.objects.get(id = request.POST["delete"])
   student.designation.remove(s)
   return HttpResponse("Deleted")

