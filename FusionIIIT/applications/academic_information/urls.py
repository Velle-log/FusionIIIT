from django.conf.urls import url
from . import views 

app_name = 'academic_information'

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
<<<<<<< HEAD
    url(r'^senate/$', views.senate, name='senate'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^edit_convenor/$', views.edit_convenor, name='edit_convenor'),
    url(r'^delete1/$', views.delete1, name='delete1'),
    url(r'^delete2/$', views.delete2, name='delete2'),
=======
    url(r'^senator/$', views.senator, name='senator'),
    url(r'^minutes/$', views.minutes, name='minutes'),
    url(r'^delete/$', views.delete, name='delete'),
  url(r'^attendance',views.add_attendance,name="add_attendance"),
    url(r'^get_attendance',views.get_attendance,name="get_attendance")
>>>>>>> 912a11178daaef08de17299f53b8a62bbc63b12b
]