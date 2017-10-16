# from django.db import models

# Create your models here.
from django.db import models
from applications.academic_information.models import Student
# Create your models here

class Mcm(models.Model):
    mcm_id              = models.IntegerField(primary_key=True)
    student_id         = models.ForeignKeyField(Student, on_delete=models.CASCADE)
    income_total        = models.IntegerField()
    income_file         = models.FileField(max_length=10)
    banck_acc           = models.CharField(max_length=15)
    brother_name        = models.CharField(max_length=30)
    brother_occupation  = models.TextField(max_length=100)
    sister_name         = models.CharField(max_length=30)
    sister_occupation   = models.TextField(max_length=100)
    income_father       = models.IntegerField()
    income_mother       = models.IntegerField()

    FATHER_OCC_CHOICES  = (
            ( 'Service',(
                        ('government','Government'),
                        ('private','Private'),
                        ('public','Public'),
                        ) 
            ),
            ('Non_Salaried',(
                         ('business','Business'),
                         ('medical','Medical'),
                         ('consultant','Consultant'),
                        )
            ),
            ('pensioners','Pensioners'),
    )
    father_occ_choice=models.CharField(max_length=10,choices=FATHER_OCC_CHOICES)
    father_occ          = models.TextField(max_length=100)
    EMPLOYED='EMP'
    
    HOUSE_WIFE='HW'
    MOTHER_OCC_CHOICES  =(
                         (EMPLOYED,'employed'),
                         (HOUSE_WIFE,'house-wife'),
    )
    mother_occ_choice=models.CharField(max_length=4,choices=MOTHER_OCC_CHOICES)
    mother_occ         = models.TextField(max_length=100)
    four_wheeler       = models.IntegerField()
    two_wheeler        = models.IntegerField()
    RENTED='rent'
    OWNES='own'
    HOUSE_TYPE_CHOICES =(
                        (RENTED,'rented'),
                        (OWNED,'owned'),
    )
    house_type         = models.CharField(max_length=5,choices=HOUSE_TYPE_CHOICES)
    house_area         = models.IntegerField()
    sSchool_10          = models.CharField(max_length=40)
    school_10_fee      = models.IntegerField()
    school_12          = models.CharField(max_length=40)
    school_12_fee      = models.IntegerField()
    father_declation   = models.FileField(null=True, blank=True)
    affidavit          = models.FileField(null=True, blank=True)
    
    COMPLETE='CMP'
    INCOMPLETE='ICMP'
    STATUS_CHOICES=(
        (COMPLETE,'complete'),
        (INCOMPLETE,'incomplete'),
    )
    status            = models.CharField(max_length=4,choices=STATUS_CHOICES)
    status_check      = models.BooleanField(default=False)

class Constants:
    time = (
        ('1am','1'),
        ('2am','2'),
        ('3am','3'),
        ('4am','4'),
        ('5am','5'),
        ('6am','6'),
        ('7am','7'),
        ('8am','8'),
        ('9am','9'),
        ('10am','10'),
        ('11am','11'),
        ('12 Noon','12'),
        ('1pm','13'),
        ('2pm','14'),
        ('3pm','15'),
        ('4pm','16'),
        ('5pm','17'),
        ('6pm','18'),
        ('7pm','19'),
        ('8pm','20'),
        ('9pm','21'),
        ('10pm','22'),
        ('11pm','23'),
        ('12 Midnight','0')
    )
    batch = (
        ('UG1','UG1'),
        ('UG2','UG2'),
        ('UG3','UG3'),
        ('UG4','UG4'),
        ('PG1','PG1'),
        ('PG2','PG2')
    )




class Award_and_scholarship(models.Model):
    award_id = models.IntegerField(primary_key=True)
    award_name = models.CharField(max_length=50, default='') 
    catalog = models.TextField()

    class Meta:
        db_table = 'Award_and_scholarship'
        
    def __str__(self):
        return str(self.award_id)

class Previous_winner(models.Model):
    previous_id = models.IntegerField(primary_key=True)
    student_id = models.ForeignKey(Student)
    award_id = models.ForeignKey(Award_and_scholarship)
    class Meta:
        db_table = 'Previous_winner'
        
    def __str__(self):
        return self.previous_id

class Release(models.Model):
    release_id = models.IntegerField(primary_key=True)
    award_id = models.ForeignKey(Award_and_scholarship)
    startdate = models.DateTimeField(auto_now=False, auto_now_add=True)
    enddate = models.DateTimeField(auto_now=False, auto_now_add=True)
    venu = models.CharField(max_length=50)
    time = models.CharField(max_length=10, choices=Constants.time)
    batch = models.CharField(max_length=10, choices=Constants.batch)
    class Meta:
        db_table = 'Release'
        
    def __str__(self):
        return str(self.release_id)





