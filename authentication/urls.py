from django.conf.urls import include, url
from . import views
from django.contrib.auth import views as auth_views
app_name ='authentication'
urlpatterns = [
	url(r'^signup/', views.signup, name='signup'),
	url(r'^success/',views.success,name='success'),
	]
