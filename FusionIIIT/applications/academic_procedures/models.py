from django.db import models
from applications.globals.models import Student, Faculty, ExtraInfo

class Thesis(models.Model):
    reg_id = models.ForeignKey(ExtraInfo, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    supervisor_id = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    topic = models.CharField(max_length=1000)

    class Meta:
        db_table = 'Thesis'

    def __str__(self):
        return self.topic & self.reg_id & self.student_id & self.supervisor_id
