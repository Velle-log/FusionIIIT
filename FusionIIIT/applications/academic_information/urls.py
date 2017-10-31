from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^attendance',views.add_attendance,name="add_attendance"),
    url(r'^get_attendance',views.get_attendance,name="get_attendance")

]