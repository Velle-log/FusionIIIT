from __future__ import unicode_literals
import json
import os
import subprocess
import collections
import random
from datetime import datetime, timedelta, date ,time
from django.shortcuts import redirect
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
from .forms import QuizForm, QuestionFormObjective
from .helpers import semester
from .models import CourseDocuments, CourseVideo, Forum, ForumReply, Quiz, QuizResult, StudentAssignment, Assignment, QuizQuestion, StudentAnswer

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
        # print(QuizResult._meta.get_fields(),"adasd")
        for q in quiz:
            qs=QuizResult.objects.filter(quiz_id=q,student_id=student)
            if q.end_time > timezone.now():
                quizs.append(q)
            if len(qs) is not 0:
                marks.append(qs[0])
                # print(qs.quiz_id.quiz_name)
        print(len(marks),"DADASDA")
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
                       'fut_quiz':quizs,
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
        quiz=Quiz.objects.filter(course_id=course)
        marks=[]
        quizs=[]
        assignment=Assignment.objects.filter(course_id=course)
        # print(QuizResult._meta.get_fields(),"adasd")
        for q in quiz:
            qs=QuizResult.objects.filter(quiz_id=q)
            if q.end_time > timezone.now():
                quizs.append(q)
            if len(qs) is not 0:
                marks.append(qs)
                # print(qs.quiz_id.quiz_name)
        print(len(qs))
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
                       'fut_quiz':quizs,
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

@login_required
def quiz(request, quiz_id):
    user=request.user
    extrainfo = ExtraInfo.objects.get(user=user)
    if extrainfo.user_type == 'student':
        student = Student.objects.get(id=extrainfo)
        roll = student.id.id[:4]
        quiz=Quiz.objects.get(pk=quiz_id)
        quizQuestion=QuizQuestion.objects.filter(quiz_id=quiz)
        length=quiz.number_of_question
        ques_pk=QuizQuestion.objects.filter(quiz_id=quiz).values_list('pk',flat=True)
        print(len(ques_pk),length)
        random_ques_pk=random.sample(list(ques_pk),length)
        shuffed_questions=[]
        for x in random_ques_pk:
            shuffed_questions.append(QuizQuestion.objects.get(pk=x))
        end=quiz.end_time
        now=timezone.now()+timedelta(hours=5.5)
        print(end,now)
        diff=end-now
        days, seconds = diff.days, diff.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        print(days,hours,minutes,seconds)
        return render (request,'coursemanagement/quiz.html',{'contest':quiz,'ques':shuffed_questions,'days':days,'hours':hours,'minutes':minutes,'seconds':seconds})
    else:
        return HttpResponse("unautherized Access!!It will be reported!!")

@login_required
def ajax_q(request,quiz_code):
    user=request.user
    extrainfo = ExtraInfo.objects.get(user=user)
    student = Student.objects.get(id=extrainfo)
    q = request.POST.get('question');
    ques=QuizQuestion.objects.get(pk=q)
    quiz_id=Quiz.objects.get(pk=ques.quiz_id.pk)
    ans=int(request.POST.get('answer'))
    # if( int(request.POST.get('answer')) == 1):
    #     ans=1
    # elif( int(request.POST.get('answer')) == 2):
    #     ans=2
    # elif( int(request.POST.get('answer')) == 3):
    #     ans=3
    # elif( int(request.POST.get('answer')) == 4):
    #     ans=3
    # elif( int(request.POST.get('answer')) == 5):
    #     ans=ques.options5
    lead = StudentAnswer.objects.filter(quiz_id=quiz_id,question_id=ques,student_id=student)
    if lead:
        lead = lead[0]
        lead.choice=ans
        lead.save()
    else:
        lead=StudentAnswer(quiz_id=quiz_id,question_id=ques,student_id=student,choice=ans)
        lead.save()
    data = { 'status': "1" }
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def create_quiz(request, course_code):
    extrainfo = ExtraInfo.objects.get(user=request.user)

    if extrainfo.user_type == 'faculty':
        instructor = Instructor.objects.filter(instructor_id=extrainfo)
        for ins in instructor:
            if ins.course_id.course_id == course_code:
                course = ins.course_id
        form = QuizForm(request.POST or None)
        errors=None
        if form.is_valid():
            # print "yes"
            st_time=form.cleaned_data['starttime']
            k1=st_time.hour
            k2=st_time.minute
            k3=st_time.second
            start_date_time=datetime.combine(form.cleaned_data['startdate'],time(k1,k2,k3))
            st_time=form.cleaned_data['endtime']
            k1=st_time.hour
            k2=st_time.minute
            k3=st_time.second
            end_date_time=datetime.combine(form.cleaned_data['enddate'],time(k1,k2,k3))
            duration=end_date_time - start_date_time
            days, seconds = duration.days, duration.seconds
            hours = days * 24 + seconds // 3600
            minutes = (seconds % 3600) // 60
            # prizes=form.cleaned_data['prizes'].replace('\r\n','/')
            description=form.cleaned_data['description'].replace('\r\n','/')
            rules=form.cleaned_data['rules'].replace('\r\n','/')
            obj=Quiz.objects.create(
                course_id=course,
                quiz_name=form.cleaned_data['name'],
                description=description,
                rules=rules,
                negative_marks=form.cleaned_data['negative_marks'],
                start_time=start_date_time,
                end_time=end_date_time,
                d_day=days,
                d_hour=hours,
                d_minute=minutes,
                            )
            # print "Done"
            return redirect('/ocms/'+course_code+'/edit_quiz/'+str(obj.pk))
            '''except:
                return HttpResponse('Unexpected Error')'''
        if form.errors:
            errors=form.errors
        return render(request, 'coursemanagement/createcontest.html', {'form': form,'errors':errors})

    else:
        return HttpResponse("unautherized Access!!It will be reported!!")

@login_required
def edit_quiz(request,course_code,quiz_code):
    extrainfo = ExtraInfo.objects.get(user=request.user)
    if extrainfo.user_type == 'faculty':
        instructor = Instructor.objects.filter(instructor_id=extrainfo)
        for ins in instructor:
            if ins.course_id.course_id == course_code:
                course = ins.course_id
        errors=None
        quiz=Quiz.objects.get(pk=quiz_code)
        if request.method == 'POST':
            form = QuestionFormObjective(request.POST,request.FILES)
            if(form.is_valid()):
                image=request.FILES['image']
                filename, file_extenstion=os.path.splitext(request.FILES['image'].name)
                full_path=settings.MEDIA_ROOT+"/"+course_code+"/quiz/"+quiz_code+"/"
                url=settings.MEDIA_URL+filename
                if not os.path.isdir(full_path):
                    cmd="mkdir "+full_path
                    subprocess.call(cmd,shell=True)
                fs = FileSystemStorage(full_path,url)
                file_name = fs.save(image.name, image)
                uploaded_file_url = "/media/"+course_code+"/quiz/"+quiz_code+"/"+image.name
                # print uploaded_file_url
                options1=form.cleaned_data['option1']
                options2=form.cleaned_data['option2']
                options3=form.cleaned_data['option3']
                options4=form.cleaned_data['option4']
                options5=form.cleaned_data['option5']
                obj=QuizQuestion.objects.create(
                quiz_id=quiz,
                image=uploaded_file_url,
                question=form.cleaned_data['problem_statement'],
                marks=form.cleaned_data['score'],
                answer=form.cleaned_data['answer'],
                options1=options1,options2=options2,options3=options3,options4=options4,options5=options5,
                )
                # print "HOGAYA"
                quiz.total_score+=form.cleaned_data['score'];
                quiz.number_of_question+=1
                quiz.save();
                obj3=QuizQuestion.objects.filter(quiz_id=quiz)
                # print obj3
                # return render(request,'/quiz/'+'edit_contest/'+str(obj.pk), {'form1': form1 ,'form2':form2,'obj':obj3})
                return redirect('/ocms/'+course_code+'/edit_quiz/'+str(quiz.pk))
            elif(form.errors):
                errors=form.errors
        else:
            form = QuestionFormObjective()
            questions=QuizQuestion.objects.filter(quiz_id=quiz)
            st=quiz.start_time
            end_time=quiz.end_time
            # prizes=obj.prizes
            # prizes=[z.encode('ascii','ignore') for z in prizes.split('/')]
            # print prizes
            description=quiz.description
            description=[z.encode('ascii','ignore') for z in description.split('/')]
            rules=quiz.rules
            rules=[z.encode('ascii','ignore') for z in rules.split('/')]
            # details={'cname':obj.contest_name,'description':obj.description,'c_type':obj.c_type,'rules':obj.rules,'starttime':st,'endtime':end_time}
            return render(request, 'coursemanagement/editcontest.html',{'form':form,'details':quiz,'course':course,'questions':questions,'description':description,'rules':rules})
    else:
        return HttpResponse("unautherized Access!!It will be reported!!")
