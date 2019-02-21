"""Mobilebuilder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from index import views as index_views
from authentication import views as authen_views
from django.contrib.auth import views as auth_views
from transaction import views as trans_views
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^admin/', admin.site.urls),
    url(r'^index/', include('index.urls')), 
    url(r'^authentication/', include('authentication.urls')),
    url(r'^home/', include('home.urls')),
    url(r'^usersetup/', include('usersetup.urls')),
    url(r'^project/',include('project.urls')),
    url(r'^transaction/', include('transaction.urls')),
    url(r'^schema/',include('schema.urls')),
    url(r'^transactionview/',include('transactionview.urls')),
    url(r'^logintemplate/',include('logintemplate.urls')),
    url(r'^hometemplate/',include('hometemplate.urls')),
    url(r'^actions/',include('actions.urls')),
    url(r'^reportview/',include('reportview.urls')),
    url(r'^syncmaster/',include('syncmaster.urls')),
    url(r'^generateprocess/',include('generateprocess.urls')),
    url(r'^login/',authen_views.login,name='login'),
    url(r'^$', index_views.base, name='base'),
    url(r'^signout/', index_views.signout, name='signout'),
    url(r'^transindex/',trans_views.transindex, name='transindex'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^favicon.ico$',RedirectView.as_view(url='/static/maincss/images/user.png')),
    url(r'^rolesetup/',include('rolesetup.urls')),
    url(r'^smssetup/',include('smssetup.urls')),
    url(r'^notification/',include('notification.urls')),
    url(r'^printformat/',include('printformat.urls')),
    url(r'^eventconfiguration/',include('eventconfiguration.urls'))
]
