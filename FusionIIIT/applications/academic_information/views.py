# from django.shortcuts import render

from django.shortcuts import render, redirect
from .models import Student, Grades, Course, Exam_timetable, Timetable
from applications.globals.models import ExtraInfo, Designation, DepartmentInfo
from django.template.defaulttags import csrf_token
from django.http import HttpResponse


def homepage(request):
    student = Student.objects.all()
    extra = ExtraInfo.objects.all()
    grade = Grades.objects.all()
    course = Course.objects.all()
    timetable = Timetable.objects.all()
    exam_t = Exam_timetable.objects.all()
    context = {
         # 'senates':senates,
        'student':student,
        'extra':extra,
        'grade':grade,
        'courses':course,
        'exam':exam_t,
        'timetable':timetable,
    }
    print(context['courses'])
    return render(request, "ais/ais.html", context)

def test(request):

   return HttpResponse("Data inputed successfully")

def add_basic_profile(request):
    if request.method=="POST":
        name = request.POST['name']
        roll = ExtraInfo.objects.get(id=request.POST['roll'])
        programme = request.POST['programme']
        batch = request.POST['batch']
        ph = request.POST['ph']
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
        else:
            return HttpResponse("Data Already Exists")
    students = Student.objects.all()
    extra = ExtraInfo.objects.all()
    context = {
        'students':students,
        'extra':extra,
    }
    return render(request, "ais/ais.html", context)

def delete_basic_profile(request):
    if request.method=="POST":

        if(Student.objects.get(id=request.POST['delete'])):
            Student.objects.get(id=request.POST['delete']).delete()
        else:
            return HttpResponse("Id Does not exist")
    return HttpResponse("Data Deleted Successfully")

def delete_advanced_profile(request):
    if request.method=="POST":
        print(request.POST['delete'])
        if Student.objects.get(id=request.POST['delete']):
            s = Student.objects.get(id=request.POST['delete'])
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
        sem = request.POST['sem']
        course = Course.objects.get(course_id=request.POST['course'])
        grade = request.POST['grade']

        # print(Grades.objects.filter(student_id=roll, course_id=course).count())
        if not Grades.objects.filter(student_id=roll, course_id=course).exists():
            db = Grades()
            db.student_id = roll
            db.course_id = course
            db.sem = sem
            db.grade = grade
            db.save()
        else:
            return HttpResponse("Data Already Exists")
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
    course = d[1]
    sem = int(d[2])
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
    if(request.method == "POST"):
        file = request.POST['file']
        db = Timetable()
        db.time_table = file
        db.save()
    timetable = Timetable.objects.all()
    context = {
        'timetable': timetable,
    }
    return HttpResponse("Added")


def add_exam_timetable(request):
    if(request.method == "POST"):
        file = request.POST['file']
        db = Exam_timetable()
        db.exam_time_table = file
        db.save()
    return HttpResponse("Data Deleted SuccessFully")


def delete_timetable(request):
    if request.method == "POST":
        data = request.POST['delete']
        t = Timetable.objects.get(time_table = data)
        t.delete()

    return HttpResponse("TimeTable Deleted")
