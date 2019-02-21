from django.conf.urls import include, url
from . import views


app_name ='index'
urlpatterns = [
	url(r'^index/', views.base, name='base'),
	url(r'^signout/', views.signout, name='signout'),
		]
