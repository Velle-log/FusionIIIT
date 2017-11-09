from django.db import models

# Create your models here.
from applications.academic_information.models import Student
from applications.globals.models import ExtraInfo

TIME = (
    ('6', '6 a.m.'),
    ('7', '7 a.m.'),
    ('8', '8 a.m.'),
    ('9', '9 a.m.'),
    ('10', '10 a.m.'),
    ('11', '11 a.m.'),
    ('12', '12 p.m.'),
    ('13', '1 p.m.'),
    ('14', '2 p.m.'),
    ('15', '3 p.m.'),
    ('16', '4 p.m.'),
    ('17', '5 p.m.'),
    ('18', '6 p.m.'),
    ('19', '7 p.m.'),
    ('20', '8 p.m.'),
    ('21', '9 p.m.')
)

FEST_NAME = (
    ('Tarang', 'Tarang'),
    ('Gusto', 'Gusto'),
    ('Abhikalpan', 'Abhikalpan')
)

CLUB_CATEGORY = (
    ('Technical', 'Technical'),
    ('Cultural', 'Cultural'),
    ('Sports', 'Sports')
)

FEST_DOMAIN = (
    ('Event Management and Infra', 'Event Management and Infra'),
    ('Finance and Accounts', 'Finance and Accounts'),
    ('Marketing and Sponsorship', 'Marketing and Sponsorship'),
    ('Media and Public Relations', 'Media and Public Relations'),
    ('Help desk and Security', 'Help desk and Security'),
    ('Design and Development', 'Design and Development')
)

STATUS = (
    ('A', 'Accepted'),
    ('D', 'Declined'),
    ('N', 'Not Processed Yet'),
)


class Club(models.Model):
    club_name = models.CharField(max_length=30, unique=True)
    club_co = models.ForeignKey(Student, related_name="club_coordinator", on_delete=models.CASCADE)
    club_coco = models.ForeignKey(Student, related_name="club_co_coordinator",
                                  on_delete=models.CASCADE)
    faculty_co = models.ForeignKey(ExtraInfo, on_delete=models.CASCADE)
    club_category = models.CharField(max_length=20, choices=CLUB_CATEGORY, default='Sports')

    def __str__(self):
        return str(self.club_name)


class Club_session(models.Model):
    club_id = models.ForeignKey(Club)
    session_date = models.DateField()
    session_time = models.CharField(max_length=20, choices=TIME)
    session_venue = models.CharField(max_length=20)
    session_topic = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    attachment = models.CharField(max_length=50)

    class Meta:
        db_table = 'Club_session'
        unique_together = ('club_id', 'session_date', 'session_time', 'session_venue')

    def __str__(self):
        return str(self.session_date)


class Club_member(models.Model):
    student_id = models.ForeignKey(Student)
    club_id = models.ForeignKey(Club)
    achievement = models.TextField(max_length=1000)

    class Meta:
        db_table = 'Club_member'
        unique_together = ('student_id', 'club_id')

    def __str__(self):
        return str(self.Student_id)


class Fest(models.Model):
    name = models.CharField(max_length=9, choices=FEST_NAME)
    convenor_name = models.ForeignKey(Student, max_length=25, related_name="convenor",
                                      on_delete=models.CASCADE)
    counsellor_name = models.ForeignKey(Student, max_length=25, related_name="counsellor",
                                        on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class Budget_Fest(models.Model):
    fest_id = models.ForeignKey(Fest)
    attachment = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    suggestion = models.TextField(max_length=1000)
    approve = models.CharField(max_length=1, choices=STATUS, default='N')

    def __str__(self):
        return str(self.attachment)


class Club_Budget(models.Model):
    club_id = models.ForeignKey(Club)
    attachment = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    suggestion = models.TextField(max_length=1000)
    approve = models.CharField(max_length=1, choices=STATUS, default='N')

    def __str__(self):
        return str(self.attachment)


class Core_Team(models.Model):
    student_id = models.ForeignKey(Student)
    fest_id = models.ForeignKey(Fest)
    domain = models.CharField(max_length=40, choices=FEST_DOMAIN)
    backlog_details = models.TextField(max_length=1000)
    discplinary_actions = models.TextField(max_length=1000)

    class Meta:
        db_table = 'Core_Team'
        unique_together = ('student_id', 'fest_id')

    def __str__(self):
        return str(self.domain)


class Trip(models.Model):
    club_id = models.ForeignKey(Club)
    place = models.CharField(max_length=40)
    description = models.CharField(max_length=300)
    start_date = models.DateField()
    end_date = models.DateField()
    approve = models.CharField(max_length=1, choices=STATUS, default='N')

    class Meta:
        db_table = 'Trip'

    def __str__(self):
        return str(self.description)
