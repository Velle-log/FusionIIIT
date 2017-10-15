from django.db import models
from django.utils import timezone


class StudentComplain(models.Model):
    complaint_date=models.DateTimeField(default=timezone.now)
    complaint_finish=models.DateTimeField
    location = models.CharField(max_length=20)
    specific_location=models.CharField(max_length=50,blank=True, default='')
    details = models.CharField(max_length=100)
    status=models.IntegerField(default='0')
    user_id=models.CharField(max_length=8,default='0')
    remarks=models.CharField(max_length=300,default="Pending")
    flag=models.IntegerField(default='0')

    def __str__(self):
        return self.location

class s_user_name(models.Model):
    s_userid=models.CharField(max_length=8)

    def __str__(self):
        return self.s_userid

class c_user_name(models.Model):
    c_user_id=models.CharField(max_length=8)
    c_location=models.CharField(max_length=8)

    def __str__(self):
        return self.c_user_id + '--' + self.c_location

class w_user_name(models.Model):
    w_user_id=models.CharField(max_length=8)
    w_location=models.CharField(max_length=8)

    def __str__(self):
        return self.w_user_id + '--' + self.w_location

class supvisor_user_name(models.Model):
    sup_user_id=models.CharField(max_length=8)

    def __str__(self):
        return self.sup_user_id

class feedback(models.Model):
    compl_id=models.IntegerField()
    detail=models.CharField(max_length=500)

    def __str__(self):
        return self.compl_id

