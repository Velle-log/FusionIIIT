from django import forms

from .models import Exam_timetable, Meeting, Timetable


class MinuteForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ('date', 'minutes_file', )
        widgets = {
            'date': forms.DateInput(attrs={
                'id': 'date', 
                'required': True, 
                'placeholder': 'dd/mm/yyyy'
            }),
            'minutes_file': forms.FileInput(attrs={
                'id': 'minutes_file', 
                'required': True,
            }),
        }


class AcademicTimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ('year', 'programme', 'time_table',)


class ExamTimetableForm(forms.ModelForm):
    class Meta:
        model = Exam_timetable
        fields = ('year', 'programme', 'exam_time_table',)
