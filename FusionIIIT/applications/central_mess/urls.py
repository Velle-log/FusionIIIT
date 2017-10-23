from django.conf.urls import include, url


from . import views

app_name = 'mess'

urlpatterns = [

    url(r'^',views.mess, name='mess'),
    url(r'^applynonveg/',views.applynonveg) #this url not working, method not called, 123 not printed
]
