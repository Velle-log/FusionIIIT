# imports
from django.db import models
from applications.globals.models import Student, Staff
from django.utils import timezone


# Class definations:


class Constants:
    AREA = (
        ('hall-1', 'hall-1'),
        ('hall-3', 'hall-3'),
        ('hall-4', 'hall-4'),
        ('CC1', 'CC1'),
        ('CC2', 'CC2'),
        ('core_lab', 'core_lab'),
        ('LHTC', 'LHTC'),
        ('NR2', 'NR2'),
        ('Rewa_Residency', 'Rewa_Residency'),
    )
    COMPLAINT_TYPE = (
        ('Electricity', 'Electricity'),
        ('carpenter', 'carpenter'),
        ('plumber', 'plumber'),
        ('garbage', 'garbage'),
        ('dustbin', 'dustbin'),
        ('internet', 'internet'),
    )


class StudentComplain(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    complainer = models.ForeignKey(Student, on_delete=models.CASCADE)
    complaint_date = models.DateTimeField(default=timezone.now)
    complaint_finish = models.DateTimeField
    complaint_type = models.CharField(choices=Constants.COMPLAINT_TYPE)
    location = models.CharField(max_length=20, choices=Constants.AREA)
    specific_location = models.CharField(max_length=50, blank=True)
    details = models.CharField(max_length=100)
    status = models.IntegerField(default='0')
    remarks = models.CharField(max_length=300, default="Pending")
    flag = models.IntegerField(default='0')
    reason = models.CharField(max_length=100)
    feedback = models.CharField(max_length=500)


class Caretaker(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    area = models.CharField(choices=Constants.AREA)


class Workers(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    caretaker_id = models.ForeignKey(Caretaker, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    age = models.CharField(default='M')
    phone = models.IntegerField(blank=True)
    worker_type = models.CharField(choices=Constants.COMPLAINT_TYPE)
