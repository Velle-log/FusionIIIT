from django.contrib import admin

from .models import (Ambulance_request, Appointment, Complaint, Doctor,
                     Hospital_admit, Stock, Stockinventory)

admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Ambulance_request)
admin.site.register(Hospital_admit)
admin.site.register(Complaint)
admin.site.register(Stock)
admin.site.register(Stockinventory)
