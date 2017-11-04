from django.conf.urls import url

from .views import healthcenter,compounder_view,student_view,student_appointment_view

app_name = 'healthcenter'

urlpatterns = [

    url(r'^$', healthcenter, name='healthcenter'),
    url(r'^compounder/$', compounder_view, name='compounder_view'),
    url(r'^student/$', student_view, name='student_view'),
    url(r'^student/appointment/$', student_appointment_view, name='student_appointment_view'),
]
