from django.conf.urls import url

from . import views

app_name = 'mess'

urlpatterns = [
    url(r'^$', views.mess, name='mess'),
    url(r'^leave', views.leaverequest, name='leaverequest'),
    url(r'^invitation', views.invitation, name='invitation'),
    url(r'^minutes', views.minutes, name='minutes'),
    url(r'^placerequest', views.placerequest, name='placerequest'),
    url(r'^(?P<ap_id>[0-9]+)/response/', views.response, name='response'),
    url(r'^(?P<ap_id>[0-9]+)/responses/', views.responses, name='responses'),
]
