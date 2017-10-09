from django.db import models
from applications.globals.models import Student, ExtraInfo

# Class definitions:


# # Class for various choices on the enumerations
class Constants:
    SEM_CHOICES = (
        ('1', '1')
        ('2', '2')
        ('3', '3')
        ('4', '4')
        ('5', '5')
        ('6', '6')
        ('7', '7')
        ('8', '8')
    )


class FinalRegistrations(models.Model):
    reg_id = models.ForeignKey(ExtraInfo)
    sem = models.IntegerField(max_length=1, choices=Constants.SEM_CHOICES)
    student_id = models.ForeignKey(Student)
    registration = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)






