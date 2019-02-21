# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from authentication.models import userprofile
from project.models import Project

# Create your views here.
def main(request):
	adminid = request.session['loggedinuserid']
	adminname = userprofile.objects.get(pk=adminid)
	print adminname
	users = userprofile.objects.filter(is_user = True, adminuserid = adminid )
	usercount = {'users':users}
	print usercount
	project = Project.objects.filter(admin_id = adminid )
	projectcount = {'project':project}
	print projectcount
	return render(request,'main.html', {'users':users,'project':project, 'adminname':adminname} )
