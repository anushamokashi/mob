from django.conf.urls import url
from . import views

app_name = 'transaction'
urlpatterns = [
    url(r'^transmain/$', views.transmain, name='transmain'),
    url(r'^delete/(?P<txid>.*)$', views.delete, name='delete'),
    url(r'^tedit/(?P<transactionid>.*)$',views.tedit, name='tedit'),  
    url(r'^tsave/(?P<transid>.*)$',views.tsave,name ='tsave'),
    url(r'^switchproject/(?P<tprojectid>.*)$',views.switchproject,name = 'switchproject'),
    url(r'^saveform/$',views.saveform,name = 'saveform'),
    url(r'^transdetails/(?P<transid>.*)$',views.getin,name = 'getin'),
    url(r'^myjsonview/$',views.myModel_asJson , name ='myModel_asJson'),
    url(r'^tabledetail/$',views.tabledetail,name ='tabledetail'),
    url(r'^addtable/$',views.addtable,name ='addtable'),
    url(r'^tabledetailedit/(?P<tableeditid>.*)$',views.tabledetail_edit,name ='tabledetail_edit'),
    url(r'^tabledetaildelete/(?P<tableid>.*)$',views.tabledetail_delete,name='tabledetail_delete'),
    url(r'^tablecomponent/(?P<tableid>.*)$',views.tablecomp_create,name ='tablecomp_create'),
    url(r'^tablecomponentedit/(?P<tabcompid>.*)$',views.tablecomponent_edit,name = 'tablecomponent_edit'),
    url(r'^tablecomponentdelete/(?P<tabcompid>.*)$',views.tablecomponent_delete,name ='tablecomponent_delete'),
    url(r'^enumlist/$',views.enumlist,name ='enumdetail'),
    url(r'^enumedit/(?P<enumid>.*)$',views.enumedit,name ='enumedit'),
    url(r'^enumdelete/(?P<enumid>.*)$',views.enumdelete,name ='enumdelete'),
    url(r'^transnamevalidation/$',views.tranname_validation,name="tranname_validation"),
    url(r'^generateSchema/(?P<txnid>.*)$',views.generateSchema,name ='generateSchema'),

   
]
