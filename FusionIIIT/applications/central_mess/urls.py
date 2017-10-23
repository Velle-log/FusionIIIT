from django.conf.urls import include, url


from . import views

app_name = 'mess'

urlpatterns = [

    url(r'^', views.mess, name='mess'),
    url(r'^applynonveg', views.nonveg, name='applynonveg')
]
