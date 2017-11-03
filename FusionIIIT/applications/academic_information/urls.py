from django.conf.urls import url
from . import views 

app_name = 'academic_information'

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^senate/$', views.senate, name='senate'),
    url(r'^input/$', views.test, name='input'),
    url(r'^delete/$', views.delete, name='delete'),
]