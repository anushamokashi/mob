# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponseRedirect, HttpResponse,HttpResponseBadRequest
from django.contrib import messages
from authentication.models import userprofile
from project.models import Projectwiseusersetup,Project
from transactionview.models import Transactionview
from schema.models import Db_profile
from .models import Actions,SaveAction,NewAction,CancelAction,DeleteAction,SearchAction,TxnPrintFormatAction,GoogleSyncAction
from .forms import ActionsForm,SaveActionForm,CancelActionForm,NewActionForm,DeleteActionForm,SearchActionform,TxnPrintFormatActionForm,GoogleSyncActionform
from transactionview.serializers import ContainerSerializer,TreeSerializer,ComponentSerializer
from django.core import serializers
from django.template.defaultfilters import slugify
import json
import ast
import MySQLdb
from django.views.decorators.csrf import csrf_exempt
from Mobilebuilder.decorators import myuser_login_required
import os
from django.conf import settings
filePath = settings.MEDIA_ROOT
# Create your views here.
@myuser_login_required
def addactions(request,txviewid):
	view = Transactionview.objects.get(pk = txviewid)
	viewid = view.id
	project_id = request.session['projectid']
	transaction_id = request.session['transactionid']
	element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])
	project_title = element.project_id.title
	projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])
	action_type = Actions.objects.filter(transactionviewid_id = viewid)

	action_lists=[action.actiontype for action in action_type]
	#print action_ser
	#print request.POST
	if request.method == 'POST':
		form = ActionsForm(request.POST)
		print form.errors
		if form.is_valid():
			
			if action_type:
				action_list = form.cleaned_data['actiontype']
				print len(action_list)
				query = Actions.objects.filter(transactionviewid_id = viewid)
				table =[]
				newtable =[]
				if len(action_list)>0:
					print "loop"
					for types in query:
						if types.actiontype in action_list:
							table.append(types.actiontype)
							print table
						else:
							typedelete = Actions.objects.filter(actiontype = types.actiontype,transactionviewid_id = viewid)
							typedelete.delete()

					for actions in action_list:
						if actions in table:
							newtable.append(actions)
						else:
							type = Actions.objects.create(actiontype=actions,displayorder = 0 ,transactionviewid_id = viewid)
							type.save()
							default_type_save(type,viewid)
							txview = Transactionview.objects.get(pk = txviewid)
							txview.createpage = False
							txview.save()


				return HttpResponseRedirect('/actions/addactions/%s'%viewid)
			else:
				action_list = form.cleaned_data['actiontype']
				for action in action_list:
					print action
					type = Actions.objects.create(actiontype=action,displayorder = 0 ,transactionviewid_id = viewid)
					type.save()
					default_type_save(type,viewid)
					txview = Transactionview.objects.get(pk = txviewid)
					txview.createpage = False
					txview.save()
					
				return HttpResponseRedirect('/actions/addactions/%s'%viewid)
		else:
			return HttpResponse('failure')		
	else:
		form = ActionsForm(initial={'actiontype':action_lists})
		return render(request,'txactions.html',locals())

def default_type_save(actions,viewid):
	if actions.actiontype == 'Save':
		save_action = SaveAction.objects.create(title ='Save',iconcls ='done-all',expression_postfix ="",expression="",actiontype_id = actions.id,transactionview_id = viewid)
	elif actions.actiontype =='Cancel':
		cancel_action = CancelAction.objects.create(title ='Cancel',iconcls ='close-circle',expression_postfix ="",expression="",actiontype_id = actions.id,transactionview_id = viewid)
	elif actions.actiontype =='New':
		new_action = NewAction.objects.create(title ='New',iconcls='create',expression_postfix ="",expression="",actiontype_id = actions.id,transactionview_id = viewid)
	elif actions.actiontype == 'Delete':
		delete_action = DeleteAction.objects.create(title = 'Delete',iconcls='trash',expression_postfix ="",expression="",actiontype_id = actions.id,transactionview_id = viewid)
	elif actions.actiontype =='Search':
		search_action = SearchAction.objects.create(title ='Search',iconcls='search',sql="",sort_type="",sort_field="",actiontype_id = actions.id,transactionview_id = viewid)
	elif actions.actiontype =='PrintFormat':
		printformat_action = TxnPrintFormatAction.objects.create(title ='Print Format',iconcls='print',expression="",actiontype_id = actions.id,transactionview_id = viewid)
	elif actions.actiontype =='GoogleSync':
		googlesync_action = GoogleSyncAction.objects.create(title ='GoogleSync',iconcls='sync',expression="",actiontype_id = actions.id,transactionview_id = viewid)
	else:
		pass


@myuser_login_required
def delete_actiontype(request,actionid,txviewid):
	view = Transactionview.objects.get(pk = txviewid)
	viewid = view.id
	query = Actions.objects.filter(pk = actionid)
	query.delete()
	view.createpage = False
	view.save()
	return HttpResponseRedirect('/actions/addactions/%s'%viewid)


@csrf_exempt
def saveaction(request,actiontype,txviewid):
	action_type = actiontype
	actions = Actions.objects.get(actiontype =actiontype,transactionviewid_id = txviewid)
	viewid = txviewid
	try:
		query = SaveAction.objects.get(actiontype_id = actions.id,transactionview_id = txviewid)
		print query,"arun"
		form = SaveActionForm(request.POST or None,instance = query,viewid=viewid)
	except:
		form = SaveActionForm(request.POST or None,viewid=viewid)

	if request.method == 'POST':
		if form.is_valid():
			saveaction = form.save(commit = False)
			saveaction.actiontype_id = actions.id
			saveaction.transactionview_id = viewid
			saveaction.save()
			txview = Transactionview.objects.get(pk = viewid)
			txview.createpage = False
			txview.save()
			return HttpResponse('success')
		else:
			return HttpResponseBadRequest('failure')
	else:
		return render(request,'saveaction.html',locals())

@csrf_exempt
def newaction(request,actiontype,txviewid):
	action_type = actiontype
	actions = Actions.objects.get(actiontype =actiontype,transactionviewid_id = txviewid)
	viewid = txviewid
	try:
		query = NewAction.objects.get(actiontype_id = actions.id,transactionview_id = txviewid)
		form = NewActionForm(request.POST or None,instance = query,viewid=viewid)
	except:
		form = NewActionForm(request.POST or None,viewid=viewid)

	if request.method == 'POST':
		if form.is_valid():
			newaction = form.save(commit = False)
			newaction.actiontype_id = actions.id
			newaction.transactionview_id = viewid
			newaction.save()
			txview = Transactionview.objects.get(pk = viewid)
			txview.createpage = False
			txview.save()
			return HttpResponse('success')
		else:
			return HttpResponseBadRequest('failure')
	else:
		return render(request,'newaction.html',locals())

@csrf_exempt
def cancelaction(request,actiontype,txviewid):
	action_type = actiontype
	actions = Actions.objects.get(actiontype =actiontype,transactionviewid_id = txviewid)
	viewid = txviewid
	try:
		query = CancelAction.objects.get(actiontype_id = actions.id,transactionview_id = txviewid)
		form = CancelActionForm(request.POST or None,instance = query,viewid=viewid)
	except:
		form = CancelActionForm(request.POST or None,viewid=viewid)

	if request.method == 'POST':
		if form.is_valid():
			cancelaction = form.save(commit = False)
			cancelaction.actiontype_id = actions.id
			cancelaction.transactionview_id = viewid
			cancelaction.save()
			txview = Transactionview.objects.get(pk = viewid)
			txview.createpage = False
			txview.save()
			return HttpResponse('success')
		else:
			return HttpResponseBadRequest('failure')

	else:
		return render(request,'cancelaction.html',locals())

@csrf_exempt
def deleteaction(request,actiontype,txviewid):
	action_type = actiontype
	actions = Actions.objects.get(actiontype =actiontype,transactionviewid_id = txviewid)
	viewid = txviewid
	try:
		query = DeleteAction.objects.get(actiontype_id = actions.id,transactionview_id = txviewid)
		form = DeleteActionForm(request.POST or None,instance = query,viewid=viewid)
	except:
		form = DeleteActionForm(request.POST or None,viewid=viewid)

	if request.method == 'POST':
		if form.is_valid():
			deleteaction = form.save(commit = False)
			deleteaction.actiontype_id = actions.id
			deleteaction.transactionview_id = viewid
			deleteaction.save()
			txview = Transactionview.objects.get(pk = viewid)
			txview.createpage = False
			txview.save()
			return HttpResponse('success')
		else:
			return HttpResponseBadRequest('failure')
	else:
		return render(request,'deleteaction.html',locals())

@csrf_exempt
def searchaction(request,actiontype,txviewid):
	action_type = actiontype
	actions = Actions.objects.get(actiontype =actiontype,transactionviewid_id = txviewid)
	viewid = txviewid
	try:
		query = SearchAction.objects.get(actiontype_id = actions.id,transactionview_id = txviewid)
		form = SearchActionform(request.POST or None,instance = query)
	except:
		form = SearchActionform(request.POST or None)

	if request.method == 'POST':
		if form.is_valid():
			searchaction = form.save(commit = False)
			searchaction.actiontype_id = actions.id
			searchaction.transactionview_id = viewid
			searchaction.save()
			txview = Transactionview.objects.get(pk = viewid)
			txview.createpage = False
			txview.save()
			return HttpResponse('success')
		else:
			return HttpResponseBadRequest('failure')

	else:
		return render(request,'searchaction.html',locals())



@csrf_exempt
def txnprintformataction(request,actiontype,txviewid):

	action_type = actiontype
	actions = Actions.objects.get(actiontype =actiontype,transactionviewid_id = txviewid)
	viewid = txviewid

	try:
		query = TxnPrintFormatAction.objects.get(actiontype_id = actions.id,transactionview_id = txviewid)
		pfform = TxnPrintFormatActionForm(request.POST or None,instance = query,viewid=viewid)
	except Exception as e:
		pfform = TxnPrintFormatActionForm(request.POST or None,viewid=viewid)


	if request.method == 'POST':
		print "POST METHOD"
		try:
			if pfform.is_valid():
				pfaction = pfform.save(commit = False)
				pfaction.actiontype_id = actions.id
				pfaction.transactionview_id = viewid
				pfaction.save()
				txview = Transactionview.objects.get(pk = viewid)
				txview.createpage = False
				txview.save()
				return HttpResponse('success')
		except Exception as e:
			print "FAILURE"
			print pfform.errors
			return HttpResponse('failure')
	else:
		print "NORMAL MODAL CALLING"
		return render(request,'txnprintformat.html',locals())

@csrf_exempt
def searchsqlvalidate(request):
	userid = request.session['userid']
	project_id = request.session['projectid']
	sql = request.POST.get('sql')
	try:
		element =Projectwiseusersetup.objects.get(userid=userid,project_id = request.session['projectid'])
		profile = Db_profile.objects.get(id = element.db_profileid_id)
		host = profile.appdb.host
		password = profile.appdb.password
		username = profile.appdb.username
		port = profile.appdb.port
		dbname  = profile.appdb.dbname
		db = MySQLdb.connect(host,username,password,dbname,int(port))
		try:
			cursor = db.cursor()
			exe = cursor.execute(sql)
			print cursor.description
			num_fields = len(cursor.description)
			field_names = [i[0] for i in cursor.description]
			return HttpResponse(json.dumps(field_names))
		except (MySQLdb.Error) as e:
			print e
			return HttpResponseBadRequest(e)

	except Exception as e:
		print e
		return HttpResponseBadRequest("Db Connection Error")

@csrf_exempt
def googlesyncaction(request,actiontype,txviewid):
	action_type = actiontype
	actions = Actions.objects.get(actiontype =actiontype,transactionviewid_id = txviewid)
	viewid = txviewid
	try:
		query = GoogleSyncAction.objects.get(actiontype_id = actions.id,transactionview_id = txviewid)
		form = GoogleSyncActionform(request.POST or None,instance = query,viewid=viewid)
	except:
		form = GoogleSyncActionform(request.POST or None,viewid=viewid)
		
	if request.method == 'POST':
		if form.is_valid():
			newaction = form.save(commit = False)
			newaction.actiontype_id = actions.id
			newaction.transactionview_id = viewid
			newaction.save()
			txview = Transactionview.objects.get(pk = viewid)
			txview.createpage = False
			txview.save()
			return HttpResponse('success')
		else:
			return HttpResponseBadRequest('failure')
	else:
		return render(request,'googlesyncaction.html',locals())
