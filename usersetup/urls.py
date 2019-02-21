from django.conf.urls import url
from . import views

app_name = 'usersetup'
urlpatterns = [
    url(r'^userindex/$', views.userindex, name='userindex'), 
    url(r'^usersgup/$', views.usersgup, name='usersgup'),
    url(r'^delete/(?P<id>.*)$', views.delete, name='delete'),
    url(r'^edit/(?P<id>.*)$', views.edit, name='edit'),
    url(r'^mailValidation/$', views.mailValidation, name='mailValidation'),
]