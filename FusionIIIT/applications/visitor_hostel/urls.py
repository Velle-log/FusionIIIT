from django.conf.urls import url

from . import views

app_name = 'visitorhostel'

urlpatterns = [

    url(r'^$', views.visitorhostel, name='visitorhostel'),
    url(r'^vh_homepage/', views.vh_homepage, name ='vh_homepage'),
    url(r'^vh_booking_request/' , views.booking_request , name ='booking_request'),
]
