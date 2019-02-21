from django.conf.urls import url
from . import views

app_name = 'syncmaster'
urlpatterns = [
    url(r'^configurations/$', views.configurations, name='configurations'),
    url(r'^tablemapsave/$', views.tablemapsave, name='tablemapsave'),
    url(r'^tablemapedit/(?P<tmapid>.*)$',views.tablemapedit,name ='tablemapedit' ),
    url(r'^tablemapdelete/(?P<tmapid>.*)$',views.tablemapdelete,name ='tablemapdelete' ),
    url(r'^columnmap/(?P<tmapid>.*)$',views.columnmap,name ='columnmap' ),
    url(r'^columnmapadd/(?P<tmapid>.*)$',views.columnmapadd,name ='columnmapadd' ),
    url(r'^columnmapsave/(?P<cmapid>.*)/(?P<tmapid>.*)$',views.columnmapsave,name ='columnmapsave' ),
    url(r'^coltableview/(?P<tmapid>.*)$',views.coltableview,name ='coltableview' ),
    url(r'^columnmapdelete/(?P<cmapid>.*)/(?P<tmapid>.*)$',views.columnmapdelete,name ='columnmapdelete' ),
    url(r'^columnmapedit/(?P<cmapid>.*)/(?P<tmapid>.*)$',views.columnmapedit,name ='columnmapedit' ),       
    url(r'^updatedb/$', views.updatedb, name='updatedb')
]    
