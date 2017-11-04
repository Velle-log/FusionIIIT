from django.shortcuts import render
from .models import Student, Meeting, Student_attendance,Course,Student
from applications.globals.models import ExtraInfo, Designation, DepartmentInfo
from django.http import HttpResponse
from django.db.models.query import QuerySet
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from .forms import MinuteForm
import json


def homepage(request):
    form = MinuteForm()
    try:
        s = Designation.objects.get(name = 'senate')
        v = Designation.objects.get(name = 'Convenor')
        t = Designation.objects.get(name = 'Co Convenor')   
        senates = ExtraInfo.objects.filter(designation = s)
        Convenor = ExtraInfo.objects.filter(designation = v)
        CoConvenor = ExtraInfo.objects.filter(designation = t)
        students = Student.objects.filter(id__in = senates)
        meetings = Meeting.objects.all()
    except:
        senates = ""
        students = ""
        Convenor = ""
        CoConvenor = ""
        meetings = ""
        pass
        
    context = {
         'senates':senates,
         'students':students,
         'Convenor':Convenor,
         'CoConvenor':CoConvenor,
    }    
         'meetings' : meetings,
         'form': form,
    } 
    if request.method == 'POST' and request.FILES :
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

def add_attendance(request):
    if request.method == 'POST':
        student_attend = Student_attendance()
        s_id = request.POST.get('student_id')
        c_id = request.POST.get('course_id')
        print(s_id)
        print(c_id)
        context={}
        try:
           student_attend.student_id = Student.objects.get(id_id=s_id)
        except:
            error_mess = "Student Data Not Found"
            context['result']='Failure'
            context['message']=error_mess
            messages.error(request, error_mess)
            return HttpResponse(json.dumps(context), content_type='add_attendance/json')


        try:
            student_attend.course_id = Course.objects.get(course_id=c_id)
        except:
            error_mess = "Course Data Not Found"
            context['result'] = 'Failure'
            context['message'] = error_mess
            messages.error(request, error_mess)
            return HttpResponse(json.dumps(context), content_type='add_attendance/json')

    # print('student_id ',student_attend.student_id)


        student_attend.present_attend = request.POST.get('present_attend')
        student_attend.total_attend = request.POST.get('total_attend')

        if student_attend.present_attend > student_attend.total_attend :
            error_mess = "Present attendance should not be greater than Total attendance"
            context['result'] = 'Failure'
            context['message'] = error_mess
            return HttpResponse(json.dumps(context), content_type='add_attendance/json')


        success_mess = "Your Data has been successfully added"
        messages.success(request, success_mess)
        student_attend.save()
        context['result'] = 'Success'
        context['message'] = success_mess
        messages.error(request, success_mess)
        return HttpResponse(json.dumps(context), content_type='add_attendance/json')


def get_attendance(request):
    course_id=request.GET.get('course_id')
    print(course_id)
    c_id=Course.objects.get(course_id=course_id)
    # data=Student_attendance.objects.filter(course_id_id=c_id).values_list('student_id_id','course_id_id')
    data = Student_attendance.objects.filter(course_id_id=c_id).values_list('course_id_id','student_id_id','present_attend','total_attend')
    stud_data={}
    stud_data['name']=[]
    stud_data['programme']=[]
    stud_data['batch']=[]
    for obj in data:
        roll = data[0][1]
        extra_info = ExtraInfo.objects.get(id=roll)
        s_id = Student.objects.get(id=extra_info)

        s_name=s_id.name
        s_programme=s_id.programme
        s_batch=s_id.batch
        print(s_name)
        print(s_programme)
        stud_data['name'].append(s_name)
        stud_data['programme'].append(s_programme)
        stud_data['batch'].append(s_batch)

    print(stud_data)
    context={}
    try:
        context['result'] = 'Success'
        context['tuples'] = list(data)
        context['stud_data']=stud_data

    except:
        context['result'] = 'Failure'


    print(data[0][1])
    print(stud_data['name'][0])
    print(context)
    return HttpResponse(json.dumps(context),content_type='get_attendance/json')
