from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^loginindex/$', views.loginindex, name='loginindex'),
	url(r'^add/$', views.add, name='add'),
	url(r'^delete/$', views.delete, name='delete'),
	url(r'^serverconfig/$', views.serverconfig, name='serverconfig'),
	url(r'^adduser/$', views.adduser, name='adduser'),
	url(r'^edituser/(?P<userid>.*)$', views.edituser, name='edituser'),
	url(r'^deleteuser/(?P<userid>.*)$', views.deleteuser, name='deleteuser'),
	url(r'^addinfo/$', views.addinfo, name='addinfo'),
	url(r'^editinfo/(?P<infoid>.*)$', views.editinfo, name='editinfo'),
	url(r'^deleteinfo/(?P<infoid>.*)$', views.deleteinfo, name='deleteinfo'),
	url(r'^generateTemplate/(?P<pid>.*)$', views.generateTemplate, name='generateTemplate'),
	url(r'^alreadyLoginpg/(?P<pid>.*)$', views.alreadyLoginpg, name='alreadyLoginpg'),
	url(r'^createLoginpg/(?P<pid>.*)$', views.createLoginpg, name='createLoginpg'),
	url(r'^updateuserindb/$', views.update_user_in_db, name='updateuserindb'),
	url(r'^callService/$', views.callService, name='callService'),
]