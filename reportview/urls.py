from django.conf.urls import url
from . import views
#from .views import getSqlComponents


app_name = 'reportview'
urlpatterns = [
    url(r'^repoviewdetails/$', views.reportview, name='repoviewdetails'),
    url(r'^saveReports/$', views.saveReports, name='saveReports'),
    url(r'^editReport/(?P<title>\d+)/$', views.reportedit, name='editReport'),
    url(r'^editmodal/(?P<title>\d+)/$', views.editmodal, name='editmodal'),
    url(r'^updateReport/(?P<reportId>\d+)/$', views.updateReport, name='updateReport'),
    url(r'^delReport/(?P<reportId>\d+)/$', views.delReport, name='delReport'),
    url(r'^parammodal/(?P<title>\d+)/$', views.parammodal, name='parammodal'),
    url(r'^saveparams/(?P<repoid>\d+)/$',views.saveparams,name ='saveparams'),
    url(r'^parameditmodal/(?P<title>\d+)/(?P<pk>\d+)/$', views.parameditmodal, name='parameditmodal'),
    url(r'^fieldmodal/(?P<title>\d+)/$', views.fieldmodal, name='fieldmodal'),
    url(r'^fieldsave/(?P<repoid>\d+)/$',views.fieldsave, name='fieldsave'),
    url(r'^fieldeditmodal/(?P<title>\d+)/(?P<pk>\d+)/$', views.fieldeditmodal, name='fieldeditmodal'),
    url(r'^Querymodal/(?P<title>\d+)/$', views.Querymodal, name='Querymodal'),
    url(r'^reportQuerySave/(?P<repoid>\d+)/$',views.reportQuerySave, name='reportQuerySave'),
    url(r'^Queryeditmodal/(?P<title>\d+)/(?P<pk>\d+)/$', views.Queryeditmodal, name='Queryeditmodal'), 
    url(r'^groupmodal/(?P<title>\d+)/$', views.groupmodal, name='groupmodal'),
    url(r'^groupingsave/(?P<repoid>\d+)/$',views.groupingsave, name='groupingsave'),
    url(r'^groupeditmodal/(?P<title>\d+)/(?P<pk>\d+)/$', views.groupeditmodal, name='groupeditmodal'),
    url(r'^delQuery/(?P<title>\d+)/$', views.delQuery, name='delQuery'),
    url(r'^delgroup/(?P<title>\d+)/$', views.delgroup, name='delgroup'),
    url(r'^delfield/(?P<title>\d+)/$', views.delfield, name='delfield'),
    url(r'^delparam/(?P<title>\d+)/$',views.delparam, name='delparam'),    
    url(r'^reportprocess/(?P<title>\d+)/(?P<pk>.*)/$', views.reportprocess, name='reportprocess'),
    url(r'^generatepage/(?P<reportid>\d+)/$', views.generate_reportpage, name='generatepage'),
    url(r'^print_format_config/(?P<title>\d+)/(?P<pk>\d+)/$', views.print_format_config, name='print_format_config'),
    url(r'^add_action_report/(?P<report_id>\d+)/$', views.add_action_report, name='add_action_report'),
    url(r'^pdf_config/(?P<title>\d+)/(?P<pk>\d+)/$',views.report_pdf,name='report_pdf'),
    url(r'^csv_config/(?P<title>\d+)/(?P<pk>\d+)/$',views.report_csv,name='report_csv'),
    url(r'^html_config/(?P<title>\d+)/(?P<pk>\d+)/$',views.report_html,name='report_config'),
    url(r'^report_pdf/(?P<title>\d+)/(?P<pk>\d+)/$',views.report_pdf,name='report_pdf'),
    url(r'^submit_config/(?P<title>\d+)/(?P<pk>\d+)/$',views.report_submit,name='report_submit'),
    url(r'^payment_config/(?P<title>\d+)/(?P<pk>\d+)/$',views.payment,name='payment'),
    url(r'^new_config/(?P<title>\d+)/(?P<pk>\d+)/$',views.newaction,name='newaction'),
    url(r'^del_action/(?P<title>\d+)/(?P<pk>\d+)/$',views.delaction,name='delaction'),
     ]