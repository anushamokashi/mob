# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt


from Mobilebuilder.decorators import myuser_login_required 
from .models import SMSServer, SMSAttributes
from .forms import SMSServerForm,SMSAttributesForm
from project.models import Project, Projectwiseusersetup
from authentication.models import userprofile

# Create your views here.


@myuser_login_required
def smsindex(request):
    loginModel = userprofile.objects.get(is_user = True ,id = request.session['userid'])
    element =Projectwiseusersetup.objects.get(userid=loginModel.id,project_id_id = request.session['projectid'] )
    projectselect =Projectwiseusersetup.objects.filter(userid =request.session['userid'])
    project_title = element.project_id.title
    projectid = request.session['projectid']
    smsServerForm = SMSServerForm()
    return render(request, 'smsindex.html', locals())
