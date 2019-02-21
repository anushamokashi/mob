from django.conf.urls import url
from . import views

app_name = 'rolesetup'
urlpatterns = [
    url(r'^roleindex/$', views.roleindex, name='roleindex'), 
    url(r'^rolesave/$', views.rolesave, name='rolesave'),
    url(r'^roledelete/(?P<roleid>.*)$', views.roledelete, name='roledelete'),
    url(r'^roleedit/(?P<roleid>.*)$', views.roleedit, name='roleedit'),
    url(r'^assignview/(?P<roleid>.*)$', views.assignview, name='assignview')
]