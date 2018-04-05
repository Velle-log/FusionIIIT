import xlrd
import os
from applications.academic_information.models import Course, Student
from applications.academic_procedures.models import Register

excel = xlrd.open_workbook(os.path.join(os.getcwd(), 'dbinsertscripts/registration.xlsx'))
z = excel.sheet_by_index(0)
#print(z.cell(5,0))
#print(z.cell(12,2).value)
#file = xlrd.open_workbook(excel,'r')
for i in range(1, 2000):
    try:
        roll_no = int(z.cell(i, 0).value)
        course_code = str(z.cell(i,4).value)
        a1 = Course.objects.get(course_id = course_code)
        a2 = Student.objects.get(id = roll_no)
        print(a1,a2)

        u = Register.objects.create(
            r_id = int(i + 10),
            course_id = a1,
            year = 2018,
            student_id = a2,
            semester = 2
        )
        print('done')
        print(i)
    except Exception as e:
        print(e)
        print(i)
        break
