from django.conf.urls import url
from . import views

app_name = 'notification'
urlpatterns = [
	url(r'^notificationindex/$', views.notificationindex, name='notificationindex'),
	url(r'^deletenotification/(?P<notificationid>.*)$',views.delNotification,name = 'delNotification'),
	url(r'^notificationEdit/(?P<notificationid>.*)$',views.notificationEdit,name = 'notificationEdit'),
	url(r'^notificationconfig/(?P<notificationid>.*)$',views.notificationConfig,name = 'notificationConfig'),
	url(r'^addstage/(?P<notificationid>.*)$',views.addStage,name = 'addstage'),
	url(r'^savestage/(?P<notificationid>.*)$',views.saveStage,name = 'savestage'),
	url(r'^updatestage/(?P<notificationstageid>.*)$',views.updateStage,name = 'updatestage'),
	url(r'^deletestage/(?P<notificationstageid>.*)$',views.deleteStage,name = 'deletestage'),
	url(r'^processType/$',views.processType,name = 'processType'),
	url(r'^gettxviewfield/(?P<txviewid>.*)$',views.getTxviewField,name = 'gettxviewfield'),
	url(r'^generateprocess/$',views.generateProcess,name = 'generateprocess'),
	
	
		
	
]