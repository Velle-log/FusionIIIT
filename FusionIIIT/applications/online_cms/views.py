from __future__ import unicode_literals
import json
import os
import subprocess
import collections
from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone

from applications.academic_information.models import (Course, Instructor,
                                                      Student)
from applications.academic_procedures.models import Register
from applications.globals.models import ExtraInfo

from .forms import AddDocuments, AddVideos
from .helpers import semester
from .models import CourseDocuments, CourseVideo, Forum, ForumReply, Quiz, QuizResult, StudentAssignment, Assignment

def create_thumbnail(course,row,name,ext, attach_str, thumb_time, thumb_size):
    # filepath = settings.MEDIA_ROOT + 'online_cms/' + course.course_id + 'vid/' + str(row.name) + '/' + str(row.tutorial_detail_id) + '/'
    filepath = settings.MEDIA_ROOT + '/online_cms/' + course.course_id + '/vid/' + name+ ext
    print(filepath)
    video_name=row.video_name[:-4]
    filename =settings.MEDIA_ROOT + '/online_cms/' + course.course_id + '/vid/' + name.replace(' ', '-') + '-' + attach_str + '.png'
    print (filename)
    # try:
        #process = subprocess.Popen(['/usr/bin/ffmpeg', '-i ' + filepath + row.video + ' -r ' + str(30) + ' -ss ' + str(thumb_time) + ' -s ' + thumb_size + ' -vframes ' + str(1) + ' -f ' + 'image2 ' + filepath + filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process = 'ffmpeg -y -i '+ filepath + ' -vframes ' + str(1) + ' -an -s ' + thumb_size  +  ' -ss ' + str(thumb_time) + ' ' + filename
    print(process)
    subprocess.call(process, shell=True)
    # except:
    #     print (1)
    #     pass


@login_required
def viewcourses(request):
    user = request.user
    extrainfo = ExtraInfo.objects.get(user=user)
    if extrainfo.user_type == 'student':
        student = Student.objects.get(id=extrainfo)

        roll = student.id.id[:4]
        register = Register.objects.filter(student_id=student, semester=semester(roll))
        courses = collections.OrderedDict()
        for reg in register:
            instructor=Instructor.objects.get(course_id=reg.course_id)
            courses[reg]=instructor
        return render(request, 'coursemanagement/coursemanagement.html',
                      {'courses': courses,
                       'extrainfo': extrainfo})
    else:
        instructor = Instructor.objects.filter(instructor_id=extrainfo)
        return render(request, 'coursemanagement/coursemanagement.html',
                      {'instructor': instructor,
                       'extrainfo': extrainfo})


@login_required
def course(request, course_code):
    user = request.user
    extrainfo = ExtraInfo.objects.get(user=user)
    if extrainfo.user_type == 'student':
        student = Student.objects.get(id=extrainfo)
        roll = student.id.id[:4]
        course = Course.objects.filter(course_id=course_code, sem=semester(roll))
        instructor = Instructor.objects.get(course_id=course[0])
        videos = CourseVideo.objects.filter(course_id=course[0])
        slides=CourseDocuments.objects.filter(course_id=course[0])
        quiz=Quiz.objects.filter(course_id=course)
        marks=[]
        quizs=[]
        assignment=Assignment.objects.filter(course_id=course[0])
        print(QuizResult._meta.get_fields(),"adasd")
        for q in quiz:
            qs=QuizResult.objects.filter(quiz_id=q,student_id=student)
            # if q.end_time > timezone.now():

            if len(qs) is not 0:
                marks.append(qs[0])
                # print(qs.quiz_id.quiz_name)
        # print(len(marks),"DADASDA")
        lec=0
        comments = Forum.objects.filter(course_id=course).order_by('comment_time')
        answers = collections.OrderedDict()
        for comment in comments:
            fr = ForumReply.objects.filter(forum_reply=comment)
            fr1= ForumReply.objects.filter(forum_ques=comment)
            if not fr :
                # question['{}'.format(comment.pk)]=comment
                # answers['{}'.format(comment.pk)]=fr1
                print(comment.comment)
                answers[comment]=fr1
        return render(request, 'coursemanagement/viewcourse.html',
                      {'course': course[0],
                       'quizs':marks,
                       'videos':videos,
                       'instructor': instructor,
                       'slides':slides,
                       'extrainfo': extrainfo,
                       'answers': answers,
                       'assignment' : assignment,
                       'Lecturer':lec})

    else:
        instructor = Instructor.objects.filter(instructor_id=extrainfo)
        print(instructor)
        for ins in instructor:
            # print(ins.course_id.course_id)
            if ins.course_id.course_id == course_code:
                print(ins.course_id.course_id)
                course = ins.course_id
                print(course)
        lec=1
        videos=CourseVideo.objects.filter(course_id=course)
        slides=CourseDocuments.objects.filter(course_id=course)
        quizs=Quiz.objects.filter(course_id=course)
        marks=[]
        for quiz in quizs:
            qs=QuizResult.objects.filter(quiz_id=quiz)
            marks.append(qs)
        comments = Forum.objects.filter(course_id=course).order_by('comment_time')
        answers = collections.OrderedDict()
        for comment in comments:
            fr = ForumReply.objects.filter(forum_reply=comment)
            fr1= ForumReply.objects.filter(forum_ques=comment)
            if not fr :
                # question['{}'.format(comment.pk)]=comment
                # answers['{}'.format(comment.pk)]=fr1
                print(comment.comment)
                answers[comment]=fr1
        return render(request, 'coursemanagement/viewcourse.html',
                      {'instructor': instructor,
                       'extrainfo': extrainfo,
                       'quizs':marks,
                       'videos':videos,
                       'slides':slides,
                       'course':course,
                       'answers': answers,
                       'Lecturer':lec
                       })

@login_required
def upload_assignment(request, course_code):
    extrainfo = ExtraInfo.objects.get(user=request.user)
    if extrainfo.designation.name == "student":
        student = Student.objects.get(id=extrainfo)
        roll = student.id.id[:4]
        course = Course.objects.filter(course_id=course_code, sem=semester(roll))
        doc = request.FILES.get('img')

        assi_name=request.POST.get('assignment_topic')
        print(type(assi_name),"asdada")
        name=request.POST.get('name')
        print(assi_name,"ADasd")
        assign=Assignment.objects.get(pk=assi_name)
        filename, file_extenstion = os.path.splitext(request.FILES.get('img').name)
        filename=name
        full_path = settings.MEDIA_ROOT+"/online_cms/"+course_code+"/assi/"+assign.assignment_name+"/"+student.id.id+"/"
        url = settings.MEDIA_URL+filename
        if not os.path.isdir(full_path):
            cmd = "mkdir "+full_path
            subprocess.call(cmd, shell=True)
        fs = FileSystemStorage(full_path, url)
        fs.save(doc.name, doc)
        uploaded_file_url = "/media/online_cms/"+course_code+"/assi/"+assign.assignment_name+"/"+student.id.id+"/"+name+file_extenstion
        index = uploaded_file_url.rfind('/')

        sa=StudentAssignment(
         student_id=student,
         assignment_id=assign,
         upload_url=uploaded_file_url[:-4],
         assign_name=name+file_extenstion
        )
        sa.save()
        return HttpResponse("Upload successful.")
    else:
        return HttpResponse("not found")

@login_required
def add_document(request, course_code):
    #    CHECK FOR ERRORS IN UPLOADING
    extrainfo = ExtraInfo.objects.get(user=request.user)
    if extrainfo.designation.name == "faculty":
        instructor = Instructor.objects.filter(instructor_id=extrainfo)
        for ins in instructor:
            if ins.course_id.course_id == course_code:
                course = ins.course_id
        description = request.POST.get('description')
        doc = request.FILES.get('img')
        print(doc)
        name = request.POST.get('name')
        filename, file_extenstion = os.path.splitext(request.FILES.get('img').name)
        filename=name
        full_path = settings.MEDIA_ROOT+"/online_cms/"+course_code+"/doc/"
        url = settings.MEDIA_URL+filename+file_extenstion
        if not os.path.isdir(full_path):
            cmd = "mkdir "+full_path
            subprocess.call(cmd, shell=True)
        fs = FileSystemStorage(full_path, url)
        fs.save(filename+file_extenstion, doc)
        uploaded_file_url = "/media/online_cms/"+course_code+"/doc/"+filename+file_extenstion
        index = uploaded_file_url.rfind('/')

        CourseDocuments.objects.create(
            course_id=course,
            upload_time=datetime.now(),
            description=description,
            document_url=uploaded_file_url[:-4],
            document_name=name+file_extenstion
        )
        return HttpResponse("Upload successful.")
    else:
        return HttpResponse("not found")


@login_required
def add_videos(request, course_code):

    # CHECK FOR ERRORS IN UPLOADING
    extrainfo = ExtraInfo.objects.get(user=request.user)
    print(extrainfo.designation)
    if extrainfo.designation.name == "faculty":
        instructor = Instructor.objects.filter(instructor_id=extrainfo)
        for ins in instructor:
            if ins.course_id.course_id == course_code:
                course = ins.course_id
        description = request.POST.get('description')
        vid = request.FILES.get('img')
        # name =request.POST.get('name')
        print (vid)
        name=request.POST.get('name')
        filename, file_extenstion = os.path.splitext(request.FILES.get('img').name)
        filename=name
        print(filename)
        full_path = settings.MEDIA_ROOT+"/online_cms/"+course_code+"/vid/"
        url = settings.MEDIA_URL+filename+file_extenstion
        if not os.path.isdir(full_path):
            cmd = "mkdir "+full_path
            subprocess.call(cmd, shell=True)
        fs = FileSystemStorage(full_path, url)
        fs.save(filename+file_extenstion, vid)
        uploaded_file_url = "/media/online_cms/"+course_code+"/vid/"+filename+file_extenstion
        index = uploaded_file_url.rfind('/')

        video=CourseVideo.objects.create(
            course_id=course,
            upload_time=datetime.now(),
            description=description,
            video_url=uploaded_file_url,
            video_name=name
        )
        create_thumbnail(course,video,name, file_extenstion,'Big',1, '700:500')
        create_thumbnail(course,video,name,file_extenstion, 'Small',1, '170:127')
        print (request.POST.get('name'))
        return HttpResponse("Upload successful.")
        # elif form.errors:
        #     form.errors
    else:
        return HttpResponse("not found")


@login_required
def forum(request, course_code):
    #take care od sem
    course=Course.objects.get(course_id=course_code, sem=5)
    comments = Forum.objects.filter(course_id=course).order_by('comment_time')
    instructor = Instructor.objects.get(course_id=course)
    if instructor.instructor_id.user.pk == request.user.pk:
        lec=1
    else:
        lec=0
    question = {}
    answers = collections.OrderedDict()
    for comment in comments:
        fr = ForumReply.objects.filter(forum_reply=comment)
        fr1= ForumReply.objects.filter(forum_ques=comment)
        if not fr :
            # question['{}'.format(comment.pk)]=comment
            # answers['{}'.format(comment.pk)]=fr1
            print(comment.comment)
            answers[comment]=fr1
    print(answers)

    context = {'course':course, 'answers': answers,'Lecturer':lec}
    return render(request,'online_cms/forum.html',context)


@login_required
def ajax_reply(request, course_code):
    course = Course.objects.get(course_id=course_code, sem=5)
    ex = ExtraInfo.objects.get(user=request.user)
    f = Forum(
        course_id=course,
        commenter_id=ex,
        comment=request.POST.get('reply')
    )
    f.save()
    print(f.comment)
    print(request.POST.get('question'))
    ques = Forum.objects.get(pk=request.POST.get('question'))
    fr = ForumReply(
        forum_ques=ques,
        forum_reply=f
    )
    # fo=Forum.objects.filter(pk=f.pk)
    # dat=serializers.serialize('json',fo)
    fr.save()
    name=request.user.first_name+" "+request.user.last_name
    time = f.comment_time.strftime('%b. %d, %Y, %I:%M %P')
    data = {'pk':f.pk,'reply':f.comment, 'replier':name,'time':time}
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def ajax_new(request, course_code):
    course = Course.objects.get(course_id=course_code, sem=5)
    ex = ExtraInfo.objects.get(user=request.user)
    f = Forum(
        course_id=course,
        commenter_id=ex,
        comment=request.POST.get('question')
    )
    f.save()
    name=request.user.first_name+" "+request.user.last_name
    time = f.comment_time.strftime('%b. %d, %Y, %I:%M %P')
    data = {'pk':f.pk,'question':f.comment, 'replier':f.commenter_id.user.username,'time':time, 'name':name }
    print(data,"new")
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def ajax_remove(request, course_code):
    course = Course.objects.get(course_id=course_code, sem=5)
    ex = ExtraInfo.objects.get(user=request.user)
    f = Forum.objects.get(
        pk=request.POST.get('question')
    )
    fr = ForumReply.objects.filter(
        forum_reply=f
    )

    if not fr:
        fr1=ForumReply.objects.filter(
            forum_ques=f
        )
        for x in fr1:
            x.forum_reply.delete()
            x.delete()
        f.delete()
    else:
        fr.delete()
        f.delete()
    data = {'message':'deleted'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def add_assignment(request, course_code):
    #    CHECK FOR ERRORS IN UPLOADING
    extrainfo = ExtraInfo.objects.get(user=request.user)
    if extrainfo.designation.name == "faculty":
        instructor = Instructor.objects.filter(instructor_id=extrainfo)
        for ins in instructor:
            if ins.course_id.course_id == course_code:
                course = ins.course_id
        description = request.POST.get('description')
        assi = request.FILES.get('img')
        name = request.POST.get('name')
        print(assi)
        filename, file_extenstion = os.path.splitext(request.FILES.get('img').name)
        filename=name
        full_path = settings.MEDIA_ROOT+"/online_cms/"+course_code+"/assi/"+name+"/"
        url = settings.MEDIA_URL+filename
        if not os.path.isdir(full_path):
            cmd = "mkdir "+full_path
            subprocess.call(cmd, shell=True)
        fs = FileSystemStorage(full_path, url)
        fs.save(assi.name, assi)
        uploaded_file_url = "/media/online_cms/"+course_code+"/assi/"+name+"/"+name+file_extenstion
        index = uploaded_file_url.rfind('/')
        name = request.POST.get('name')
        assign=Assignment(
            course_id=course,
            submit_date=request.POST.get('myDate'),
            assignment_url=uploaded_file_url,
            assignment_name=name
        )
        assign.save()
        return HttpResponse("Upload successful.")
    else:
        return HttpResponse("not found")
