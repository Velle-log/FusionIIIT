# from django.shortcuts import render

from django.shortcuts import render
from .models import Student, Meeting
from applications.globals.models import ExtraInfo, Designation, DepartmentInfo
from django.http import HttpResponse
from django.db.models.query import QuerySet
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import MinuteForm
import json


def homepage(request):
    form = MinuteForm()
    try:
        s = Designation.objects.get(name = 'senate')
        senates = ExtraInfo.objects.filter(designation = s)
        students = Student.objects.filter(id__in = senates)
        meetings = Meeting.objects.all()
    except:
        senates = ""
        students = ""
        meetings = ""
        pass
        
    context = {
         'senates':senates,
         'students':students,
         'meetings' : meetings,
         'form': form,
    } 
    if request.method == 'POST':
        form = MinuteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('sucess')            
        else:
            return HttpResponse('not uploaded')   
    return render(request, "ais/ais.html", context)

def delete(request):
   s = Designation.objects.get(name = "senate")
   student = ExtraInfo.objects.get(id = request.POST["delete"])
   student.designation.remove(s)
   return HttpResponse("Deleted")

@csrf_exempt
def senator(request):    
    if request.method == 'POST':
        rollno = request.POST.get('rollno')
        extraInfo = ExtraInfo.objects.get(id = rollno)
        s = Designation.objects.get(name = 'senate')
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