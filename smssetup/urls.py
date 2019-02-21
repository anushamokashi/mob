from django.conf.urls import url
from . import views

app_name = 'smssetup'
urlpatterns = [
    url(r'^smsindex/$', views.smsindex, name='smsindex'), 

]