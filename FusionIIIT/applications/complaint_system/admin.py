from django.contrib import admin

from .models import Caretaker, StudentComplain, Workers

admin.site.register(Caretaker)
admin.site.register(Workers)
admin.site.register(StudentComplain)
