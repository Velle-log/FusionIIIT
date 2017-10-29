from django.conf.urls import url

from . import views

app_name = 'mess'

urlpatterns = [
    url(r'^$', views.mess, name='mess'),
    url(r'^leave', views.leaverequest, name='leaverequest'),
]
