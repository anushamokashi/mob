from django.conf.urls import url
from . import views

app_name = 'eventconfiguration'
urlpatterns = [
    url(r'^mapTxnFields/$', views.mapTxnFields, name='mapTxnFields'),
    url(r'^getcomponents/(?P<txviewid>\d+)/$', views.getcomponents, name='getcomponents'),
    url(r'^addEvent/$', views.addEvent, name='addEvent'),
    url(r'^deleteEvent/(?P<eventid>\d+)$', views.deleteEvent, name='deleteEvent')
    

]