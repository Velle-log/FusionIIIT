from django.conf.urls import url

from .views import healthcenter
app_name = 'healthcenter'

urlpatterns = [

    url(r'^$', healthcenter, name='healthcenter'),
]
