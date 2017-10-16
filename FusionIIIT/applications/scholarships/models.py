# from django.db import models

from datetime import datetime

# Create your models here.
from django.db import models

from applications.academic_information.models import Student
from applications.globals.models import ExtraInfo

# Create your models here


class Constants:
    MOTHER_OCC_CHOICES = (
          ('EMPLOYED', 'EMPLOYED'),
          ('HOUSE_WIFE', 'HOUSE_WIFE')

    )
    HOUSE_TYPE_CHOICES = (
         ('RENTED', 'RENTED'),
         ('OWNED', 'OWNED')

    )
    STATUS_CHOICES = (
        ('COMPLETE', 'COMPLETE'),
        ('INCOMPLETE', 'INCOMPLETE')
    )

    FATHER_OCC_CHOICES = (
        ('Service', (
                        ('government', 'Government'),
                        ('private', 'Private'),
                        ('public', 'Public'),
                        )
         ),
        ('Non_Salaried', (
                         ('business', 'Business'),
                         ('medical', 'Medical'),
                         ('consultant', 'Consultant'),
                        )
         ),
        ('pensioners', 'Pensioners')

    )
    time = (
        ('0', '12 Midnight'),
        ('1am', '1'),
        ('2am', '2'),
        ('3am', '3'),
        ('4am', '4'),
        ('5am', '5'),
        ('6am', '6'),
        ('7am', '7'),
        ('8am', '8'),
        ('9am', '9'),
        ('10am', '10'),
        ('11am', '11'),
        ('12 Noon', '12'),
        ('1pm', '13'),
        ('2pm', '14'),
        ('3pm', '15'),
        ('4pm', '16'),
        ('5pm', '17'),
        ('6pm', '18'),
        ('7pm', '19'),
        ('8pm', '20'),
        ('9pm', '21'),
        ('10pm', '22'),
        ('11pm', '23'),
        ('12 Midnight', '0')
    )
    batch = (
        ('UG1', 'UG1'),
        ('UG2', 'UG2'),
        ('UG3', 'UG3'),
        ('UG4', 'UG4'),
        ('PG1', 'PG1'),
        ('PG2', 'PG2')
    )


class Mcm(models.Model):
    email_id = models.CharField(max_length=25)
    extrainfo_id = models.ForeignKey(ExtraInfo, on_delete=models.CASCADE)
    income_total = models.IntegerField()
    income_file = models.FileField(null=True, blank=True)
    loan_bank_details = models.TextField(max_length=200)
    banck_acc_no = models.IntegerField()
    loan_amount = models.IntegerField()
    brother_name = models.CharField(max_length=30)
    brother_occupation = models.TextField(max_length=100)
    sister_name = models.CharField(max_length=30)
    sister_occupation = models.TextField(max_length=100)
    income_father = models.IntegerField()
    income_mother = models.IntegerField()
    father_occ_choice = models.CharField(max_length=10, choices=Constants.FATHER_OCC_CHOICES)
    father_occ = models.TextField(max_length=100)
    mother_occ_choice = models.CharField(max_length=10, choices=Constants.MOTHER_OCC_CHOICES)
    mother_occ = models.TextField(max_length=100)
    four_wheeler = models.IntegerField(default=0)
    four_wheeler_des = models.TextField(max_length=30)
    two_wheeler = models.IntegerField(default=0)
    two_wheeler_des = models.TextField(max_length=30)
    house_type = models.CharField(max_length=5, choices=Constants.HOUSE_TYPE_CHOICES)
    house_area = models.IntegerField()
    school_10 = models.CharField(max_length=40)
    school_10_fee = models.IntegerField()
    school_12 = models.CharField(max_length=40)
    school_12_fee = models.IntegerField()
    father_declation = models.FileField(null=True, blank=True)
    affidavit = models.FileField(null=True, blank=True)
    status = models.CharField(max_length=4, choices=Constants.STATUS_CHOICES)
    status_check = models.BooleanField(default=False)

    class Meta:
        db_table = 'Mcm'


class Award_and_scholarship(models.Model):
    award_name = models.CharField(max_length=1000, default='')
    catalog = models.TextField()

    class Meta:
        db_table = 'Award_and_scholarship'


class Previous_winner(models.Model):
    year = models.IntegerField(default=datetime.datetime.now().year)

    class Meta:
        db_table = 'Previous_winner'


class Release(models.Model):
    enddate = models.DateTimeField(("End date"))
    venue = models.CharField(max_length=50)
    time = models.CharField(max_length=10, choices=Constants.time)
    batch = models.CharField(max_length=10, choices=Constants.batch)

    class Meta:
        db_table = 'Release'


class Financial_assitance(models.Model):
    name = models.CharField(max_length=60)
    amount_month = models.IntegerField()
    awarding_authority = models.CharField(max_length=50)
    total_amount = models.IntegerField()

    class Meta:
        db_table = 'Financial_assitance'


class Dm_proficiency_gold_PG(models.Model):
    nearst_policestation = models.CharField(max_length=100)
    nearst_railwaystation = models.CharField(max_length=100)
    correspondance_address = models.CharField(max_length=300)
    title_thesis = models.CharField(max_length=100)
    thesis_details = models.TextField(max_length=1500)
    thesis_document = models.FileField()

    class Meta:
        db_table = 'Dm_proficiency_gold_PG')


class IIITDMJ_proficiency_gold_PG(models.Model):
    nearst_policestation = models.CharField(max_length=100)
    nearst_railwaystation = models.CharField(max_length=100)
    correspondance_addres = models.CharField(max_length=300)
    title_thesis = models.CharField(max_length=100)
    thesis_details = models.TextField(max_length=1500)
    thesis_document = models.FileField()

    class Meta:
        db_table = 'IIITDMJ_proficiency_gold_PG'


class Dm_proficiency_gold_UG(models.Model):
    correspondance_address = models.CharField(max_length=300)
    title = models.CharField(max_length=100)
    project_details = models.TextField(max_length=1500)
    project_documents = models.FileField()

    class Meta:
        db_table = 'Dm_proficiency_gold_UG'


class IIITDMJ_proficiency_gold_UG(models.Model):
    IIITDMJ_gold_UG = models.IntegerField(primary_key=True)
    correspondance_address = models.CharField(max_length=300)
    title = models.CharField(max_length=100)
    project_details = models.TextField(max_length=1500)
    project_documents = models.FileField()

    class Meta:
        db_table = 'IIITDMJ_proficiency_gold_UG'


class Group_students(models.Model):
    dm_gold_UG = models.ForeignKey(Dm_proficiency_gold_UG)

    class Meta:
        db_table = 'Group_students'
        unique_together = ('student_id', 'dm_gold_UG'


class Director_gold_UG(models.Model):
    nearst_policestation = models.CharField(max_length=100)
    nearst_railwaystation = models.CharField(max_length=100)
    correspondance_address = models.CharField(max_length=300)
    academic_achievements = models.TextField(max_length=1500)
    research_achievements = models.TextField(max_length=1500)
    science_achievements = models.TextField(max_length=1500)
    cultural_achievements = models.TextField(max_length=1500)
    games_achievements = models.TextField(max_length=1500)
    social_service = models.TextField(max_length=1500)
    academic_documents = models.FileField()
    research_documents = models.FileField()
    science_documents = models.FileField()
    cultural_documents = models.FileField()
    games_documents = models.FileField()
    social_service_documents = models.FileField()

    class Meta:
        db_table = 'Director_gold_UG'


class Director_gold_PG(models.Model):
    nearst_policestation = models.CharField(max_length=100)
    nearst_railwaystation = models.CharField(max_length=100)
    correspondance_address = models.CharField(max_length=300)
    academic_achievements = models.TextField(max_length=1500)
    research_achievements = models.TextField(max_length=1500)
    science_achievements = models.TextField(max_length=1500)
    cultural_achievements = models.TextField(max_length=1500)
    games_achievements = models.TextField(max_length=1500)
    social_service = models.TextField(max_length=1500)
    academic_documents = models.FileField()
    research_documents = models.FileField()
    science_documents = models.FileField()
    cultural_documents = models.FileField()
    games_documents = models.FileField()
    social_service_documents = models.FileField()

    class Meta:
        db_table = 'Director_gold_PG'


class Director_silver_UG_cultural(models.Model):
    nearst_policestation = models.CharField(max_length=100)
    nearst_railwaystation = models.CharField(max_length=100)
    correspondance_address = models.CharField(max_length=300)
    participation_details = models.TextField(max_length=1500)
    participation_documents = models.FileField()

    class Meta:
        db_table = 'Director_silver_UG_cultural'


class Director_silver_UG_sports(models.Model):
    nearst_policestation = models.CharField(max_length=100)
    nearst_railwaystation = models.CharField(max_length=100)
    correspondance_address = models.CharField(max_length=300)
    participation_details = models.TextField(max_length=1500)
    participation_documents = models.FileField()

    class Meta:
        db_table = 'Director_silver_UG_sports'
