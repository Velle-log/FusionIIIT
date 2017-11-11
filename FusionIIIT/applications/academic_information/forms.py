from django import forms

from .models import Meeting, Timetable, Exam_timetable


class MinuteForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ('date', 'minutes_file', )

class AcademicTimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ('year', 'programme', 'time_table',)

class ExamTimetableForm(forms.ModelForm):
    class Meta:
        model = Exam_timetable
        fields = ('year', 'programme', 'exam_time_table',)
