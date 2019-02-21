from django.conf.urls import url
from . import views

app_name = 'transactionview'
urlpatterns = [
	 url(r'^transview/(?P<transactionid>.*)/(?P<projectid>.*)$', views.transview, name='transview'),
	 url(r'^viewedit/(?P<txviewid>.*)$',views.transviewedit,name ='transviewedit' ),
	 url(r'^viewdelete/(?P<txviewid>.*)$',views.transviewdelete,name = 'transviewdelete'),
	 url(r'^viewcomponent/(?P<txviewid>.*)$',views.getin,name ='getin'),
	 url(r'^tableview/$',views.tableview,name='tableview'),
	 url(r'^tabledetails/$',views.tabledetails,name='tabledetails'),
	 url(r'^editcontainer/(?P<containid>.*)$',views.editcontainer,name ='editcontainer'),
	 url(r'^deletecontainer/(?P<contid>.*)$',views.deletecontainer,name = 'deletecontainer' ),
	 url(r'^addcomponent/(?P<contid>.*)$',views.addcomponent,name='addcomponent'),
	 url(r'^savecomponent/(?P<contid>.*)$',views.savecomponent,name ='savecomponent'),
	 url(r'^deletecomponent/(?P<contid>.*)$',views.deletecomponent,name='deletecomponent'),
	 url(r'^editcomponent/(?P<componid>.*)$',views.editcomponent,name = 'editcomponent'),
	 url(r'^componentSQLModal/$',views.componentSQLModal,name = 'componentSQLModal'),
	 url(r'^generatepage/(?P<txviewid>.*)$',views.generatepage,name ='generatepage'),
	 url(r'^printhtml/$',views.printhtml,name='printhtml'),
	 url(r'^ionichtml/$',views.ionichtml,name='ionichtml'),
	 url(r'^metajson/$',views.metajson,name='metajson'),
	 url(r'^ionicpages/$',views.ionicpages,name='ionicpages'),
	 url(r'^updateSqlInDb/(?P<txviewid>.*)$',views.updateSqlInDb,name='updateSqlInDb'),
	 url(r'^eupdateAdd/(?P<txviewid>.*)$',views.eupdateAdd,name='eupdateAdd'),
	 url(r'^eupdateEdit/(?P<eupdateid>.*)$',views.eupdateEdit,name='eupdateEdit'),
	 url(r'^eupdatetype/$',views.eupdatetype,name='eupdatetype'),
	 url(r'^eupdate_trfields/$',views.eupdate_trfields,name='eupdate_trfields'),
	 url(r'^eupdateSave/(?P<txviewid>.*)$',views.eupdateSave,name='eupdateSave'),
	 url(r'^eupdateDelete/(?P<eupdateid>.*)$',views.eupdateDelete,name='eupdateDelete'),
	 url(r'^eupdateEdit/(?P<eupdateid>.*)$',views.eupdateEdit,name='eupdateEdit'),
 	 url(r'^epostadd/(?P<txviewid>.*)$',views.epostadd,name='epostadd'),
 	 url(r'^eposttarget/(?P<txviewid>.*)$',views.eposttarget,name='eposttarget'),
 	 url(r'^epostSave/(?P<txviewid>.*)$',views.epostSave,name='epostSave'),
 	 url(r'^epostUpdate/(?P<epostid>.*)/(?P<txviewid>.*)$',views.epostUpdate,name='epostUpdate'),
 	 url(r'^epostDelete/(?P<epostid>.*)$',views.epostDelete,name='epostDelete'),
 	 url(r'^epostEdit/(?P<epostid>.*)/(?P<txviewid>.*)$',views.epostEdit,name='epostEdit'),
	 url(r'^addrow/(?P<txviewid>.*)$',views.epostadd,name='epostadd'),
	 url(r'^firesqladdmodal/(?P<txviewid>.*)$',views.firesqlAdd,name='firesqlAdd'),
	 url(r'^firesqledit/(?P<txviewid>.*)/(?P<firesqlid>.*)$',views.firesqlEdit,name='firesqlEdit'),
	 url(r'^deletefiresql/(?P<firesqlid>.*)$',views.delFireSql,name='delFireSql'),
	 url(r'^txncss/(?P<txviewid>.*)$',views.txncss,name='txncss'),
	 
	
	
]
