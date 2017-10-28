from django.conf.urls import url

from .views import (add_hospital_admission, add_medicine, add_stock,
                    approve_appointment, lodge_complaint, request_ambulance,
                    request_appointment, view_admissions, view_ambulance,
                    view_complaints, view_my_admission, view_my_ambulance,
                    view_my_appointment, view_my_complaint)

urlpatterns = [
    url(r'^request_app/$', request_appointment, name='request_ambulance'),
    url(r'^approve_app/$', approve_appointment, name='approve_appointment'),
    url(r'^request_amb/$', request_ambulance, name='request_ambulance'),
    url(r'^view_amb/$', view_ambulance, name='view_ambulance'),
    url(r'^view_my_app/$', view_my_appointment, name='view_my_appointment'),
    url(r'^view_my_amb/$', view_my_ambulance, name='view_my_ambulance'),
    url(r'^view_my_com/$', view_my_complaint, name='view_my_complaint'),
    url(r'^view_my_adm/$', view_my_admission, name='view_my_admission'),
    url(r'^add_stock/$', add_stock, name='add_stock'),
    url(r'^add_medicine/$', add_medicine, name='add_medicine'),
    url(r'^view_adm/$', view_admissions, name='view_admissions'),
    url(r'^view_com/$', view_complaints, name='view_complaints'),
    url(r'^lodge_complaint/$', lodge_complaint, name='lodge_complaint'),
    url(r'^add_hospital_admission/$', add_hospital_admission, name='add_hospital_admission'),

]
