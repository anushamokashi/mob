from django.conf.urls import include, url
from schema import views

#app_name ='schema'
urlpatterns = [
	url(r'^main/$', views.main, name='main'),
	url(r'^config/$', views.config, name='config'), 
	url(r'^rgister_account/$', views.rgister_account, name='rgister_account'),
	url(r'^MyView/$', views.MyView, name='MyView'), 
	url(r'^Edit/(?P<transactionid>\d+)/$', views.Edit, name='Edit'),
	url(r'^addDb/$', views.addDb, name='addDb'),  
	url(r'^dbView/$', views.dbView, name='dbView'), 
    url(r'^appmodal/$', views.appmodal, name='appmodal'),
    #url(r'^editsave/(?P<transactionid>\d+)/$', views.editsave, name='editsave'),
    url(r'^Editprof/(?P<transactionid>\d+)/$', views.Editprof, name='Editprof'),
    url(r'^deleteprof/(?P<transactionid>\d+)/$', views.deleteprof, name='deleteprof'),
    url(r'^deleteconn/(?P<transactionid>\d+)/$', views.deleteconn, name='deleteconn'),    
		]