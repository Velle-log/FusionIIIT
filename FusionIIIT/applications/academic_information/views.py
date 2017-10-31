# from django.shortcuts import render
from django.shortcuts import render,redirect
from .models import Student_attendance,Course,Student
from applications.globals.models import ExtraInfo
import json
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def homepage(request):
    context = {}

    return render(request, "ais/ais.html", context)


# def add_attendanc(request):
#     return render(request,'ais/attendance.html',{})

def add_attendance(request):
    if request.method == 'POST':
        student_attend = Student_attendance()
        s_id = request.POST.get('student_id')
        c_id = request.POST.get('course_id')
        try:
           student_attend.student_id = Student.objects.get(id_id=s_id)
        except:
            error_mess = "Student Data Not Found"
            messages.error(request, error_mess)

        try:
            student_attend.course_id = Course.objects.get(course_id=c_id)
        except:
            error_mess = "Course Data Not Found"
            messages.error(request, error_mess)

    # print('student_id ',student_attend.student_id)

        student_attend.present_attend = request.POST.get('present_attend')
        student_attend.total_attend = request.POST.get('total_attend')
        success_mess = "Your Data has been successfully added"
        messages.success(request, success_mess)
        student_attend.save()
        return HttpResponse('Data Successfully added')


def get_attendance(request):
    course_id=request.GET.get('course_id')
    c_id=Course.objects.get(course_id=course_id)
    # data=Student_attendance.objects.filter(course_id_id=c_id).values_list('student_id_id','course_id_id')
    data = Student_attendance.objects.filter(course_id_id=c_id).values_list('course_id_id','student_id_id','present_attend','total_attend')
    stud_data={}
    stud_data['name']=[]
    stud_data['programme']=[]
    for obj in data:
        roll = data[0][1]
        extra_info = ExtraInfo.objects.get(id=roll)
        s_id = Student.objects.get(id=extra_info)

        s_name=s_id.name
        s_programme=s_id.programme
        print(s_name)
        print(s_programme)
        stud_data['name'].append(s_name)
        stud_data['programme'].append(s_programme)

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