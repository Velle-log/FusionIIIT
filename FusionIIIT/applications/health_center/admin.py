from django.contrib import admin

<<<<<<< HEAD
from .models import (Ambulance_request, Appointment, Complaint, Doctor, Expiry,
                     Hospital_admit, Medicine, Prescribed_medicine, Counter,
                     Prescription, Schedule, Stock, Hospital)

admin.site.register(Doctor)
admin.site.register(Counter)
admin.site.register(Hospital)
admin.site.register(Expiry)
=======
from .models import (Ambulance_request, Appointment, Complaint, Doctor,
                     Hospital_admit, Medicine, Prescribed_medicine,
                     Prescription, Schedule, Stock, Stockinventory)

admin.site.register(Doctor)
>>>>>>> da2946e1cfafc8a828075685182d40ebba922cd8
admin.site.register(Appointment)
admin.site.register(Ambulance_request)
admin.site.register(Hospital_admit)
admin.site.register(Complaint)
admin.site.register(Stock)
<<<<<<< HEAD
=======
admin.site.register(Stockinventory)
>>>>>>> da2946e1cfafc8a828075685182d40ebba922cd8
admin.site.register(Prescription)
admin.site.register(Medicine)
admin.site.register(Prescribed_medicine)
admin.site.register(Schedule)
