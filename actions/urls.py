from django.conf.urls import url
from . import views

app_name = 'actions'
urlpatterns = [
	url(r'^addactions/(?P<txviewid>.*)$',views.addactions,name = 'addactions'),
	url(r'^delete_actiontype/(?P<actionid>.*)/(?P<txviewid>.*)$',views.delete_actiontype,name = 'delete_actiontype'),
	url(r'^saveaction/(?P<actiontype>.*)/(?P<txviewid>.*)$',views.saveaction,name ='saveaction'),
	url(r'^newaction/(?P<actiontype>.*)/(?P<txviewid>.*)$',views.newaction,name ='newaction'),
	url(r'^cancelaction/(?P<actiontype>.*)/(?P<txviewid>.*)$',views.cancelaction,name ='cancelaction'),
	url(r'^deleteaction/(?P<actiontype>.*)/(?P<txviewid>.*)$',views.deleteaction,name ='deleteaction'),
	url(r'^searchaction/(?P<actiontype>.*)/(?P<txviewid>.*)$',views.searchaction,name ='searchaction'),
	url(r'^printformataction/(?P<actiontype>.*)/(?P<txviewid>.*)$',views.txnprintformataction,name ='txnprintformataction'),
	url(r'^searchsqlvalidate/$',views.searchsqlvalidate,name = 'searchsqlvalidate'),
	url(r'^googlesyncaction/(?P<actiontype>.*)/(?P<txviewid>.*)$',views.googlesyncaction,name ='googlesyncaction'),
]    
