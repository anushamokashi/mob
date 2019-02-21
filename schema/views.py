# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.shortcuts import render, redirect,render_to_response
from django.contrib import messages
from django.db import models
from django.contrib.auth.models import User
from schema.form import DbprofileForm
from .models import Db_connections_info
from .models import Db_profile
from schema.form import DbForm
from authentication.models import userprofile
from Mobilebuilder.decorators import myadmin_login_required 

# Create your views here.
@myadmin_login_required
def main(request):
	adminid = request.session['loggedinuserid']
	adminname = userprofile.objects.get(pk=adminid)
      #rendering the template in HttpResponse
 	return render(request,'main.html')
	
@csrf_exempt
def rgister_account(request):
	
	adminid = request.session['loggedinuserid']
	adminname = userprofile.objects.get(pk=adminid)
	
	if request.method=="POST":
		form = DbprofileForm(request.POST)
		if form.is_valid():
			
			user = form.save(commit=False)
			user.userid = userprofile.objects.get(pk=request.session['loggedinuserid'])
			user.save()
		return HttpResponseRedirect('/schema/config/')
	return render(request, "config.html", {'form': form}) 

@myadmin_login_required
def config(request):
	adminid = request.session['loggedinuserid']
	adminname = userprofile.objects.get(pk=adminid)
	objs = Db_connections_info.objects.all()
	objsprofile = Db_profile.objects.all()
	return render(request,'config.html',locals())

@myadmin_login_required
def MyView(request):
    return render_to_response('display.html', locals())

@myadmin_login_required
def addDb(request):
	form = DbprofileForm()
	return render_to_response('addDb.html', locals())    

@myadmin_login_required
def Edit(request,transactionid):
	saveedit = Db_connections_info.objects.get(pk=transactionid)

	if request.method == 'POST':
		form = DbprofileForm(request.POST, instance=saveedit)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/schema/config/')
	else:
		form = DbprofileForm(instance=saveedit)
	return render(request,'dbconnedit.html', {'form':form,'objs': Db_connections_info.objects.get(pk=transactionid)})

@myadmin_login_required
def dbView(request):
	objsprofile = Db_profile.objects.all()
	return render_to_response('db_profile.html', locals())

@myadmin_login_required
def appmodal(request):
	if request.method == "POST":
		form = DbForm(request.POST)
		if form.is_valid():
			#Title = form.cleaned_data['Title']
			#UserName = form.cleaned_data['UserName']
			prof = form.save(commit=False)
			prof.userid = userprofile.objects.get(pk=request.session['loggedinuserid'])
			prof.save()
		return HttpResponseRedirect('/schema/config/')
	else:
		form = DbForm()
	return render(request, "modal.html", {'form': form})

@myadmin_login_required
def Editprof(request,transactionid):
	saveedit1 = Db_profile.objects.get(pk=transactionid)

	if request.method == 'POST':
		form = DbForm(request.POST, instance=saveedit1)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/schema/config/')
	else:
		form = DbForm(instance=saveedit1)
	return render(request,'profedit.html', locals())

@myadmin_login_required
def deleteconn(request,transactionid):
	query =   Db_connections_info.objects.get(pk=transactionid)
	query.delete()
	return HttpResponseRedirect('/schema/config/')

@myadmin_login_required
def deleteprof(request,transactionid):
	query =  Db_profile.objects.get(pk=transactionid)
	query.delete()
	return HttpResponseRedirect('/schema/config/')    

