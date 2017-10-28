from django import forms
from django.forms.extras import SelectDateWidget

from applications.globals.models import ExtraInfo

from .models import Constants, Doctor, Stock


class Request_Appointment(forms.Form):
    doctor_id = forms.ModelChoiceField(queryset=Doctor.objects.all())
    description = forms.CharField(max_length=100)
    appointment_date = forms.DateField(widget=SelectDateWidget())
    appointment_time = forms.ChoiceField(choices=Constants.TIME)

    def __init__(self, *args, **kwargs):
        super(Request_Appointment, self).__init__(*args, **kwargs)


class Request_Ambulance(forms.Form):
    reason = forms.CharField(max_length=50)
    start_date = forms.DateField(widget=SelectDateWidget())
    end_date = forms.DateField(widget=SelectDateWidget(), required=False)

    def __init__(self, *args, **kwargs):
        super(Request_Ambulance, self).__init__(*args, **kwargs)

    def clean(self):
        if self.cleaned_data['end_date'] == '':
            self.cleaned_data['end_date'] = None


class Hospital_Admission(forms.Form):
    user_id = forms.ModelChoiceField(queryset=ExtraInfo.objects.all())
    doctor_id = forms.ModelChoiceField(queryset=Doctor.objects.all(), required=False)
    hospital_name = forms.CharField(max_length=50)
    admission_date = forms.DateField(widget=SelectDateWidget())
    reason = forms.CharField(max_length=50)


class Lodge_Complaint(forms.Form):
    complaint = forms.CharField(widget=forms.Textarea())


class Add_Stock(forms.Form):
    medicine_id = forms.ModelChoiceField(queryset=Stock.objects.all())
    quantity = forms.IntegerField()


class Add_Medicine(forms.Form):
    medicine_name = forms.CharField(max_length=50)
    quantity = forms.IntegerField()
