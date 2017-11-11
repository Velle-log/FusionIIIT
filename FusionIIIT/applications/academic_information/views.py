import json

from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from applications.globals.models import Designation, ExtraInfo

from .forms import MinuteForm, AcademicTimetableForm, ExamTimetableForm
from applications.globals.models import Designation, ExtraInfo
from .models import (Course, Exam_timetable, Grades, Meeting, Student,
                     Student_attendance, Timetable)


def homepage(request):
    minuteForm = MinuteForm()
    examTtForm = ExamTimetableForm()
    acadTtForm = AcademicTimetableForm()        
    try:
        senator_des = Designation.objects.get(name='senate')
        convenor_des = Designation.objects.get(name='Convenor')
        coconvenor_des = Designation.objects.get(name='Co Convenor')
        dean_des = Designation.objects.get(name='Dean')
        senates = ExtraInfo.objects.filter(designation=senator_des)
        Convenor = ExtraInfo.objects.filter(designation=convenor_des)
        CoConvenor = ExtraInfo.objects.filter(designation=coconvenor_des)
        Dean = ExtraInfo.objects.get(designation=dean_des)
        students = Student.objects.filter(id__in=senates)
        meetings = Meeting.objects.all()
        student = Student.objects.all()
        extra = ExtraInfo.objects.all()
        courses = Course.objects.all()
        timetable = Timetable.objects.all()
        exam_t = Exam_timetable.objects.all()
        grade = Grades.objects.all()
    except:
        senates = ""
        students = ""
        Convenor = ""
        CoConvenor = ""
        meetings = ""
        Dean = ""
        student = ""
        grade = ""
        courses = ""
        extra = ""
        exam_t = ""
        timetable = ""
    pass

    context = {
         'senates': senates,
         'students': students,
         'Convenor': Convenor,
         'CoConvenor': CoConvenor,
         'meetings': meetings,
         'minuteForm': minuteForm,
         'acadTtForm': acadTtForm,
         'examTtForm': examTtForm,
         'Dean': Dean,
         'student': student,
         'extra': extra,
         'grade': grade,
         'courses': courses,
         'exam': exam_t,
         'timetable': timetable,
    }    
    return render(request, "ais/ais.html", context)


###############senator##############################
@csrf_exempt
def senator(request):
    if request.method == 'POST':
        rollno = request.POST.get('rollno')
        extraInfo = ExtraInfo.objects.get(id=rollno)
        s = Designation.objects.get(name='senate')
        extraInfo.designation.add(s)
        extraInfo.save()
        student = Student.objects.get(id=extraInfo)
        data = {
            'name': extraInfo.user.username,
            'rollno': extraInfo.id,
            'programme': student.programme,
            'branch': extraInfo.department.name
        }
        return JsonResponse(data)
    else:
        data = {}
        return JsonResponse(data)

@csrf_exempt
def deleteSenator(request, pk):
    s = get_object_or_404(Designation,name="senate")
    student = get_object_or_404(ExtraInfo, id=pk)
    student.designation.remove(s)
    data = {}
    return JsonResponse(data)
#####################################################


###########covenors and coconvenors##################
@csrf_exempt
def add_convenor(request):
    s = Designation.objects.get(name='Convenor')
    p = Designation.objects.get(name='Co Convenor')
    if request.method == 'POST':
        rollno = request.POST.get('rollno_convenor')
        extraInfo = ExtraInfo.objects.get(id=rollno)
        result = request.POST.get('designation')
        if result == "Convenor":
            extraInfo.designation.add(s)
            extraInfo.save()
            designation = 'Convenor'
        else:
            extraInfo.designation.add(p)
            extraInfo.save()
            designation = 'Co Convenor'
        data = {
            'name': extraInfo.user.username,
            'rollno_convenor': extraInfo.id,
            'designation': designation,
        }
        return JsonResponse(data)
    else:
        data = {}
        return JsonResponse(data)
    

@csrf_exempt
def deleteConvenor(request, pk):
    s = get_object_or_404(Designation,name="Convenor")
    c = get_object_or_404(Designation,name="Co Convenor")
    student = get_object_or_404(ExtraInfo, id=pk)
    for des in student.designation.all():
        if des.name == s.name:
            student.designation.remove(s)
            designation = des.name
        elif des.name == c.name:
            designation = des.name 
            student.designation.remove(c)
    data = {
        'id': pk,
        'designation': designation,
    }
    return JsonResponse(data)
#######################################################


###########Senate meeting Minute##################
@csrf_exempt
def addMinute(request):
    minuteForm = MinuteForm()
    if request.method == 'POST':
        minuteForm = MinuteForm(request.POST, request.FILES)
        if minuteForm.is_valid():
            print(request.POST.get('date'))
            print(request.POST.get('minutes_file'))
            minuteForm.save()
            data = {
                'date': request.POST.get('date'),
                'minutes_file': request.POST.get('minutes_file')
            }
            return JsonResponse(data)
        else:
            data = {}
            return JsonResponse(data)
    else:
        data = {}
        return JsonResponse(data)


def deleteMinute(request):
    minute = Meeting.objects.get(id=request.POST["delete"])
    minute.delete()
    return HttpResponse("Deleted")
#######################################################


###########Student basic profile##################
@csrf_exempt
def add_basic_profile(request):
    if request.method=="POST":
        name = request.POST.get('name')
        roll = ExtraInfo.objects.get(id=request.POST.get('rollno'))
        programme = request.POST.get('programme')
        batch = request.POST.get('batch')
        ph = request.POST.get('phoneno')
        if not Student.objects.filter(id=roll).exists():
            db = Student()
            st = ExtraInfo.objects.get(id=roll.id)
            db.name = name.upper()
            db.id = roll
            db.batch = batch
            db.programme = programme
            st.phone_no = ph
            db.save()
            st.save()
            data = {
                'name': name,
                'rollno': roll.id,
                'programme': programme,
                'phoneno': ph,
                'batch': batch
            }
            print(data)
            return JsonResponse(data)
        else:
            data = {}
            return JsonResponse(data)
    else:
        data = {}
        return JsonResponse(data)


@csrf_exempt
def delete_basic_profile(request, pk):
    if(Student.objects.get(id=pk)):
        Student.objects.get(id=pk).delete()
    else:
        return HttpResponse("Id Does not exist")
    data = {}
    return JsonResponse(data)
##########################################################


def add_attendance(request):
    if request.method == 'POST':
        student_attend = Student_attendance()
        s_id = request.POST.get('student_id')
        c_id = request.POST.get('course_id')
        print(s_id)
        print(c_id)
        context = {}
        try:
            student_attend.student_id = Student.objects.get(id_id=s_id)
        except:
            error_mess = "Student Data Not Found"
            context['result'] = 'Failure'
            context['message'] = error_mess
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
        student_attend.present_attend = request.POST.get('present_attend')
        student_attend.total_attend = request.POST.get('total_attend')
        if student_attend.present_attend > student_attend.total_attend:
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
    course_id = request.GET.get('course_id')
    print(course_id)
    c_id = Course.objects.get(course_id=course_id)
    data = Student_attendance.objects.filter(course_id_id=c_id).values_list('course_id_id',
                                                                            'student_id_id',
                                                                            'present_attend',
                                                                            'total_attend')
    stud_data = {}
    stud_data['name'] = []
    stud_data['programme'] = []
    stud_data['batch'] = []
    for obj in data:
        roll = data[0][1]
        extra_info = ExtraInfo.objects.get(id=roll)
        s_id = Student.objects.get(id=extra_info)
        s_name = s_id.name
        s_programme = s_id.programme
        s_batch = s_id.batch
        print(s_name)
        print(s_programme)
        stud_data['name'].append(s_name)
        stud_data['programme'].append(s_programme)
        stud_data['batch'].append(s_batch)
    print(stud_data)
    context = {}
    try:
        context['result'] = 'Success'
        context['tuples'] = list(data)
        context['stud_data'] = stud_data
    except:
        context['result'] = 'Failure'
    print(data[0][1])
    print(stud_data['name'][0])
    print(context)
    return HttpResponse(json.dumps(context), content_type='get_attendance/json')




def delete_advanced_profile(request):
    if request.method=="POST":
        st = request.POST['delete']
        arr = st.split("-")
        stu = arr[0]
        if Student.objects.get(id=stu):
            s = Student.objects.get(id=stu)
            s.father_name=""
            s.mother_name=""
            s.hall_no=1
            s.room_no=""
            s.save()
        else:
            return HttpResponse("Data Does Not Exist")

    return HttpResponse("Data Deleted Successfully")


def add_advanced_profile(request):
    if request.method=="POST":
        try:
            roll = ExtraInfo.objects.get(id=request.POST['roll'])
            father = request.POST['father']
            mother = request.POST['mother']
            hall = request.POST['hall']
            room = request.POST['room']
            dp = request.POST['dp']
        except:
            return HttpResponse("Student Does Not Exist")
        try:
            db = Student.objects.get(id=roll)
        except:
            return HttpResponse("Student Does Not Exist")
        db.father_name = father.upper()
        db.mother_name = mother.upper()
        db.hall_no = hall
        db.room_no = room.upper()
        db.save()
        # db2 = ExtraInfo()
        # db2.profile_picture = dp
        # db2.save()
    return HttpResponse("Data successfully inputed")


def add_grade(request):
    if request.method=="POST":
        try:
            roll = Student.objects.get(id=request.POST['roll'])
        except:
            return HttpResponse("Student Does Not Exist")
        subject = request.POST['course']
        sem = request.POST['sem']
        grade = request.POST['grade']
        course = Course.objects.get(course_id=subject)
        arr = []
        for c in roll.courses.all():
            arr.append(c)
        flag = 1
        print(arr)
        for i in arr:
            if(subject == str(i)):
                if(sem == str(c.sem)):
                    if not Grades.objects.filter(student_id=roll, course_id=course).exists():
                        db = Grades()
                        db.student_id = roll
                        db.course_id = course
                        db.sem = sem
                        db.grade = grade
                        db.save()
                        flag = 0
                        break
                    else:
                        return HttpResponse("Data Already Exists")
                else:
                    return HttpResponse("Student did not take " + subject + " in semester " + sem)
        if(flag == 1):
            return HttpResponse("Student did not opt for course")
        grades = Grades.objects.all()
        context={
            'grades':grades,
        }
    return render(request, "ais/ais.html", context)


def delete_grade(request):
    print(request.POST['delete'])
    data =request.POST['delete']
    d = data.split("-")
    id = d[0]
    course = d[2]
    sem = int(d[3])
    #print(course)
    if request.method=="POST":
        if(Grades.objects.filter(student_id=id, sem=sem)):
            s = Grades.objects.filter(student_id=id, sem=sem)
            for p in s:
                if (str(p.course_id)==course):
                    print(p.course_id)
                    p.delete()
        else:
            return HttpResponse("Unable to delete data")
    return HttpResponse("Data Deleted SuccessFully")

def add_course(request):
    if request.method=="POST":
        try:
            c = Student.objects.get(id=request.POST['roll'])
        except:
            return HttpResponse("Student Does Not Exist")
        if(request.POST['c1']):
            c_id=Course.objects.get(course_id=request.POST['c1'])
            c.courses.add(c_id)
        if(request.POST['c2']):
            c_id2 = Course.objects.get(course_id=request.POST['c2'])
            c.courses.add(c_id2)
        if(request.POST['c3']):
            c_id3 = Course.objects.get(course_id=request.POST['c3'])
            c.courses.add(c_id3)
        if(request.POST['c4']):
            c_id4 = Course.objects.get(course_id=request.POST['c4'])
            c.courses.add(c_id4)
        if(request.POST['c5']):
            c_id5 = Course.objects.get(course_id=request.POST['c5'])
            c.courses.add(c_id5)
        if(request.POST['c6']):
            c_id6 = Course.objects.get(course_id=request.POST['c6'])
            c.courses.add(c_id6)

        c.save()
        print(c.courses.all())
    return HttpResponse("Data Entered Successfully")


def add_timetable(request):
    acadTtForm = AcademicTimetableForm()
    if request.method == 'POST' and request.FILES:
        acadTtForm = AcademicTimetableForm(request.POST, request.FILES)
        if acadTtForm.is_valid():
            acadTtForm.save()
            return HttpResponse('sucess')
    else:
        return HttpResponse('not uploaded')


def add_exam_timetable(request):
    examTtForm = ExamTimetableForm()
    if request.method == 'POST' and request.FILES:        
        examTtForm = ExamTimetableForm(request.POST, request.FILES)
        if examTtForm.is_valid():
            examTtForm.save()
            return HttpResponse('sucess')
    else:
        return HttpResponse('not uploaded')


def delete_timetable(request):
    if request.method == "POST":
        data = request.POST['delete']
        t = Timetable.objects.get(time_table = data)
        t.delete()

    return HttpResponse("TimeTable Deleted")

def delete_exam_timetable(request):
    if request.method == "POST":
        data = request.POST['delete']
        t = Exam_timetable.objects.get(exam_time_table = data)
        t.delete()

    return HttpResponse("TimeTable Deleted")
