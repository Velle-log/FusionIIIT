from django.conf.urls import url
from . import views 

app_name = 'academic_information'

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^senate/$', views.senate, name='senate'),
    url(r'^input/$', views.test, name='input'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^edit_convenor/$', views.edit_convenor, name='edit_convenor'),
    url(r'^delete1/$', views.delete1, name='delete1'),
    url(r'^delete2/$', views.delete2, name='delete2'),
]
