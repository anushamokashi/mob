# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponseRedirect, HttpResponse,HttpResponseBadRequest
from django.shortcuts import render
from django.contrib import messages
from authentication.models import userprofile
from project.models import Projectwiseusersetup,Project
from .models import SyncTableDetails,SyncColumnDetails,EditedTableMap,EditedColumnMap
from syncmaster.forms import SyncTableDetailsForm,SyncColumnDetailsForm
from django.core import serializers
from django.template.defaultfilters import slugify
import string
import json
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from Mobilebuilder.decorators import myuser_login_required 
from django.core.exceptions import ValidationError
from django import forms
from django.db.models import Q
from update_syncmaster import update_syncmaster_table


# Create your views here.
def configurations(request):
	element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])
	projectid = element.project_id.id
	projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])
	if element.setasdefaultproject or request.session['projectid']:
		project_title = element.project_id.title
		try:
			synctable = SyncTableDetails.objects.filter( Q(projectid_id = projectid) & ~Q(db_status='deleted') )

			print synctable
		except Exception as e:
			print e

	form = SyncTableDetailsForm(pid = request.session['projectid'],userid = request.session['userid'])
	return render(request,'syncmaster.html',locals())

def tablemapsave(request):
	
	project = Project.objects.get(id = request.session['projectid'])
	
	if request.POST:
		form = SyncTableDetailsForm(request.POST,pid = request.session['projectid'],userid = request.session['userid'])
		try:
			if form.is_valid():
				newtablemap = form.save(commit = False)
				newtablemap.projectid_id = project.id
				newtablemap.db_status = 'new'
				newtablemap.save()
				return HttpResponse("Success")
			else:
				print form.errors
				return HttpResponse("Failure2")
		except Exception as e:
			print e
			return HttpResponse("Failure1")

	else:
		return render(request,'syncmaster.html',locals())

@csrf_exempt
def tablemapedit(request,tmapid):
	query = SyncTableDetails.objects.get(pk = tmapid)
	old_status = query.db_status
	print old_status
	
	if request.POST:
		
		if old_status != 'new':
			try:
				existingData = EditedTableMap.objects.get(synctable_id=query.id)
			except EditedTableMap.DoesNotExist:
				existingData = None
			
			if existingData == None:
				tablemap_backup_tab = EditedTableMap()
				tablemap_backup_tab.synctable_id = query.id
				tablemap_backup_tab.old_sourcetable = query.sourcetable
				tablemap_backup_tab.old_targettable= query.targettable
				tablemap_backup_tab.pid = query.projectid_id
				tablemap_backup_tab.save()
			else:
				existingData.old_sourcetable = query.sourcetable
				existingData.old_targettable = query.targettable
				existingData.save()


		form = SyncTableDetailsForm(request.POST,instance = query,pid = request.session['projectid'],userid = request.session['userid'])
		
		try:
			if form.is_valid():

				if old_status == 'new':
						form.save()
				else:
					mapform = form.save(commit=False)
					mapform.db_status = 'edited'
					mapform.save()
				
				return HttpResponse("Success")
			else:
				print form.errors
				return HttpResponse("Failure2")
		
		except Exception as e:
			print e
			return HttpResponse("Failure1")
	else:
		form = SyncTableDetailsForm(instance = query,pid = request.session['projectid'],userid = request.session['userid'])
		return render(request,'edittablemap.html',locals())

@myuser_login_required
def tablemapdelete(request,tmapid):
	query = SyncTableDetails.objects.get(pk = tmapid)
	query.db_status = 'deleted'
	query.save()		
	return HttpResponseRedirect('/syncmaster/configurations/')

@myuser_login_required
def columnmap(request,tmapid):
	tablemapid = tmapid
	colmap = SyncColumnDetails.objects.filter( Q(syncTable_id = tmapid) & ~Q(db_status='deleted') )
	print colmap
	return render(request,'columnmap.html',locals())

@myuser_login_required
def columnmapadd(request,tmapid):
	tbdetails = SyncTableDetails.objects.get(id = tmapid)
	cform = SyncColumnDetailsForm(tmapid = tbdetails.id,userid = request.session['userid'])
	return render(request,'columnmapadd.html',locals())

@csrf_exempt
def columnmapsave(request,cmapid,tmapid):
	project = Project.objects.get(id = request.session['projectid'])
	tbdetails = SyncTableDetails.objects.get(id = tmapid)
	try:
		coldetails = SyncColumnDetails.objects.get(id = cmapid)
		old_status = coldetails.db_status
		print old_status
		
		if request.POST:
			
			if old_status != 'new':
				try:
					existingData = EditedColumnMap.objects.get(synccolumn_id=coldetails.id)
				except EditedColumnMap.DoesNotExist:
					existingData = None
				
				if existingData == None:
					cmap_backup_tab = EditedColumnMap()
					cmap_backup_tab.synccolumn_id = coldetails.id
					cmap_backup_tab.synctable_id = coldetails.syncTable_id
					cmap_backup_tab.old_sourcefield = coldetails.sourcefield
					cmap_backup_tab.old_targetfield = coldetails.targetfield
					cmap_backup_tab.pid = coldetails.projectid_id
					cmap_backup_tab.save()
				else:
					existingData.old_sourcefield = coldetails.sourcefield
					existingData.old_targetfield = coldetails.targetfield
					existingData.save()
			
			cform = SyncColumnDetailsForm(request.POST,instance = coldetails,tmapid = tbdetails.id,userid = request.session['userid'])
			print cform.is_valid()
			
			if cform.is_valid():

				if old_status == 'new':
					cform.save()
				else:
					colmap = cform.save(commit =False)
					colmap.db_status = 'edited'
					colmap.save()
			else:
				print cform.errors

				
			return HttpResponseRedirect('/syncmaster/coltableview/%s'%tmapid)
		else:
			return HttpResponseBadRequest("error")

	except Exception as e:
		print e
		if request.POST:
			cform = SyncColumnDetailsForm(request.POST,tmapid = tbdetails.id,userid = request.session['userid'])
		
			if cform.is_valid():
				
				colmap = cform.save(commit =False)
				colmap.syncTable_id = tmapid
				colmap.projectid_id = project.id
				colmap.db_status = 'new'
				colmap.save()
				
				return HttpResponseRedirect('/syncmaster/coltableview/%s'%tmapid)
			else:
				
				return HttpResponseBadRequest("error")
			
				

@myuser_login_required
def columnmapedit(request,cmapid,tmapid):
	tbdetails = SyncTableDetails.objects.get(id = tmapid)
	query = SyncColumnDetails.objects.get(id = cmapid)
	cmapid= query.id
	cform = SyncColumnDetailsForm(instance = query,tmapid = tbdetails.id,userid = request.session['userid'])
	return render(request,'columnmapadd.html',locals())


@csrf_exempt
def columnmapdelete(request,cmapid,tmapid):
	try:
		query = SyncColumnDetails.objects.get(id = cmapid)
		query.db_status = 'deleted'
		query.save()
		tablemapid = tmapid
		colmap = SyncColumnDetails.objects.filter(Q(syncTable_id = tmapid) & ~Q(db_status='deleted'))
		return render(request,'coltableview.html',locals())
	except Exception as e:
		return HttpResponseBadRequest("error")
		

@myuser_login_required
def coltableview(request,tmapid):
	tablemapid = tmapid
	colmap = SyncColumnDetails.objects.filter(Q(syncTable_id = tmapid) & ~Q(db_status='deleted'))
	return render(request,'coltableview.html',locals())


@csrf_exempt
def updatedb(request):
	project_id = request.session['projectid']
	user_id = request.session['userid']
	db_error = []
	
	errors = update_syncmaster_table(request,user_id,project_id,"server")
	errors += update_syncmaster_table(request,user_id,project_id,"client")
	
	if len(errors) > 0:
		for error in errors:
			db_error.append(str(error))
			print db_error
		return HttpResponse(json.dumps(db_error))
	else:
		return HttpResponse("SUCCESS")




