from django.conf.urls import url

from . import views

app_name = 'mess'

urlpatterns = [

    url(r'^$', views.mess, name='mess'),
    url(r'^applynonveg/', views.applynonveg),
    url(r'^placeorder/', views.placeorder, name='placeorder'),
    url(r'^submit/', views.submit, name='submit'),
    url(r'^vacasubmit/', views.vacasubmit, name='vacasubmit'),
]
