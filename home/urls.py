from django.conf.urls import include, url
from . import views


app_name ='home'
urlpatterns = [
	url(r'^main/', views.main, name='main'),
		]
