from django.conf.urls import url
from . import views


app_name = 'printformat'
urlpatterns = [
    url(r'^printformatindex/$', views.printformatindex, name='printformatindex'),
    url(r'^addPFModal/$', views.addNewFormat, name='addNewFormat'),
    url(r'^savePF/$', views.addNewFormat, name='addNewFormat'),
    url(r'^editPF/(?P<id>\d+)$', views.updtaePFFormat, name='updtaePFFormat'),
    url(r'^deletepf/(?P<id>\d+)$', views.deletePFFormat, name='deletePFFormat'),
    

]