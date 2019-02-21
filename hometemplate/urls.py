from django.conf.urls import url
from . import views

app_name = 'hometemplate'
urlpatterns = [
	url(r'^pagecomponent/$',views.hometemplate,name='hometemplate'),
	url(r'^transview_asjson/$',views.transview_asjson,name='transview_asjson'),
	url(r'^addmenu/$',views.addmenu,name = 'addmenu'),
	url(r'^editmenu/(?P<menuid>.*)$',views.editmenu,name ='editmenu'),
	url(r'^deletemenu/(?P<menuid>.*)$',views.deletemenu,name = 'deletemenu'),
	url(r'^generatepage/(?P<homeid>.*)$',views.generatepage,name = 'generatepage'),
	url(r'^homehtml/(?P<pid>.*)$',views.homehtml,name = 'homehtml'),
	url(r'^submenuadd/$',views.submenuadd,name = 'submenuadd'),
	url(r'^submenuedit/(?P<menuid>.*)$',views.submenuedit,name ='submenuedit'),
	url(r'^submenutable/(?P<homeid>.*)$',views.submenutable,name = 'submenutable'),
	url(r'^deletesubmenu/(?P<menuid>.*)$',views.deletesubmenu,name = 'deletesubmenu'),
	url(r'^rootpage/(?P<homeid>.*)$',views.rootpage,name='rootpage'),
]
