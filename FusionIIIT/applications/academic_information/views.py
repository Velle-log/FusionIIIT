# from django.shortcuts import render

from django.shortcuts import render
from .models import Student
from applications.globals.models import ExtraInfo, Designation, DepartmentInfo
from django.template.defaulttags import csrf_token
from django.http import HttpResponse


def homepage(request):

    s = Designation.objects.get(name = 'senate')
    try:
        senates = ExtraInfo.objects.filter(designation = s)
    except:
        senates = ""
        pass
        
    context = {
         'senates':senates,
    }
    
    return render(request, "ais/ais.html", context)

def test(request):
    s = Designation.objects.get(name = 'senate')
    if request.method == 'POST':
        extraInfo = ExtraInfo.objects.get(id = request.POST['Roll Number'])
        extraInfo.designation.add(s)
        extraInfo.save()
    return HttpResponse("Data Inputed")


def delete(request):
   s = Designation.objects.get(name = "senate")
   student = ExtraInfo.objects.get(id = request.POST["delete"])
   student.designation.remove(s)
   return HttpResponse("Deleted")


