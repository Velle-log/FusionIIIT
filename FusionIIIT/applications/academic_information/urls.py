from django.conf.urls import url
from . import views 

app_name = 'academic_information'

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^senator/$', views.senator, name='senator'),
    url(r'^minutes/$', views.minutes, name='minutes'),
    url(r'^delete/$', views.delete, name='delete'),
  url(r'^attendance',views.add_attendance,name="add_attendance"),
    url(r'^get_attendance',views.get_attendance,name="get_attendance")
]