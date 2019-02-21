# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponseRedirect, HttpResponse,HttpResponseBadRequest
from django.shortcuts import render
from django.contrib import messages
from authentication.models import userprofile
from project.models import Projectwiseusersetup,Project
from transaction.models import Transaction,Txtabledetails,Txtablecomponentdetails
from transaction.serializers import TxtbdetailsSerializer
from rolesetup.models import Role,ViewsForRole
from .models import Transactionview,Container,Component,Eupdate,Epost,EpostMapField,FireSql,txnCssutilites
from transactionview.forms import TransactionviewForm,ContainerForm,ComponentForm,EupdateForm,EpostForm,EpostMapForm,FireSqlForm,CssTxnForm
from transactionview.serializers import ContainerSerializer,TreeSerializer,ComponentSerializer,ViewtreeSerializer,EpostComponentSerializer
from actions.serializers import ActionsSerializer
from actions.models import Actions,TxnPrintFormatAction
from schema.models import Db_connections_info, Db_profile
from hometemplate.models import Homepage,Menu,RootPage
from printformat.models import PrintFormat
from generateprocess.views import dbconnection
from django.core import serializers
from django.template.defaultfilters import slugify
from django.db import transaction
import string
import json
import os
import zipfile
import StringIO
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from operator import itemgetter
from Mobilebuilder.decorators import myuser_login_required
from django.forms.models import modelformset_factory
from django.db.models import Q
import re
import MySQLdb
import logintemplate

# Create your views here.
@myuser_login_required
def transview(request,transactionid,projectid):
	transaction = Transaction.objects.get(pk = transactionid)
	transaction_title = transaction.txname
	transaction_id = transaction.id
	request.session['transactionid']=transaction_id
 	project = Project.objects.get(pk = projectid)
 	project_id = project.id
	element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])
	projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])
	transgroup =  Transactionview.objects.filter(transactionid_id = transaction_id,projectid_id = project_id )
	if request.method == 'POST':
		exp = request.POST.get('expression')
		form = TransactionviewForm(request.POST)
		if form.is_valid():
			newview = form.save(commit = False)
			newview.transactionid_id = transaction_id
			newview.projectid_id = project_id
			newview.identifiers = newview.title.lower().replace(" ","")+"_txn"
			newview.postfixexp = json.dumps(parseEventsIntoMap(exp))
			newview.save()
			return HttpResponseRedirect('/transactionview/transview/%s/%s'% (transaction_id,project_id))
		else:
			messages.add_message(request, messages.ERROR, 'There was some problems while saving.')
			return render(request, 'transview.html',{'form':form,'transgroup':transgroup,'element':element,'projectselect':projectselect,'transactionid':transaction_id,'projectid':project_id,'tran_title':transaction_title})
	else:
		form = TransactionviewForm()
		return render(request, 'transview.html',{'form':form,'transgroup':transgroup,'element':element,'projectselect':projectselect,'transactionid':transaction_id,'projectid':project_id,'tran_title':transaction_title})

@myuser_login_required
def transviewedit(request,txviewid):
	viewid = txviewid
	transaction_id = request.session['transactionid']
	project_id = request.session['projectid']

	query = Transactionview.objects.get(pk = txviewid)
	if request.method == 'POST':
		exp = request.POST.get('expression')
		form = TransactionviewForm(request.POST,instance=query)
		if form.is_valid():
			txview = form.save(commit = False)
			txview.createpage = False
			txview.identifiers = txview.title.lower().replace(" ","")+"_txn"
			txview.postfixexp = json.dumps(parseEventsIntoMap(exp))
			txview.save()
			return HttpResponseRedirect('/transactionview/transview/%s/%s'% (transaction_id,project_id))
		else:
			element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])
			project_title = element.project_id.title
			projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])
			transgroup =  Transactionview.objects.filter(transactionid_id = transaction_id,projectid_id = project_id )
			messages.add_message(request, messages.ERROR, 'There was some problems while saving.')
			return render(request, 'transview.html',locals())
	else:
		form = TransactionviewForm(instance = query)
		return render(request,'vieweditmodel.html',{'form':form,'viewid':viewid})

@myuser_login_required
def transviewdelete(request,txviewid):
	transaction_id = request.session['transactionid']
	project_id = request.session['projectid']
	query = Transactionview.objects.get(pk = txviewid)
	try:
		role = Role.objects.filter(projectid_id = project_id)
		for r in role:
			roleid = r.id
			views = ViewsForRole.objects.filter(role_id = roleid)
			for view in views:
				lists = json.loads(view.txview)
				try:
					menu  = Menu.objects.filter(transactionview_id = txviewid)
					for m in menu:
						ids =  str(m.id)
						lists.remove(ids)

					view.txview = json.dumps(lists)
					view.save()
				except Exception as ed:
					print ed


	except Exception as e:
		print e
	query.delete()
	return HttpResponseRedirect('/transactionview/transview/%s/%s'% (transaction_id,project_id))

@csrf_exempt
@myuser_login_required
def getin(request,txviewid):
	element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])
	projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])
	view = Transactionview.objects.get(pk = txviewid)
	viewtitle = view.title.upper()
	viewtype =view.viewtype
	viewid = view.id
	project_id = request.session['projectid']
	transaction_id = request.session['transactionid']
	request.session['viewid'] = viewid
	tablegroup = Container.objects.filter(transactionviewid_id = viewid ).order_by('displayorder')
	tablegroup_serializer = ContainerSerializer(instance=tablegroup,many=True)
	tablegroup_serializer_json = json.dumps(tablegroup_serializer.data)
	tablegroup_serializer_json_obj = json.loads(tablegroup_serializer_json)
	tablegroup = Container.objects.filter(transactionviewid_id = viewid,parent = None )
	tree_serializer = TreeSerializer(instance=tablegroup,many=True,)
	tree_serializer_json = json.dumps(tree_serializer.data)
	component = Component.objects.filter(transactionviewid_id = viewid)
	componet_ser =ComponentSerializer(instance=component,many=True)
	componet_ser_json= json.dumps(componet_ser.data)
	eupdatedetails = Eupdate.objects.filter(transactionview_id = viewid)
	epostdetails = Epost.objects.filter(source_tx_view_id = viewid)
	request.session['transactionviewid'] = viewid
	firesqlObj  = FireSql.objects.filter(transactionview_id = viewid)
	if request.method == 'POST':
		contform = ContainerForm(request.POST,tranid = transaction_id,viewid = viewid)
		if contform.is_valid():
			newcomponent = contform.save(commit = False)
			newcomponent.transactionviewid_id = viewid
			newcomponent.identifiers = slugify(newcomponent.title).replace("-","_")
			newcomponent.save()
			view.createpage = False
			view.save()
			tablegroup = Container.objects.filter(transactionviewid_id = viewid).order_by('displayorder')
			tablegroup_serializer = ContainerSerializer(instance=tablegroup,many=True)
			tablegroup_serializer_json = json.dumps(tablegroup_serializer.data)
			tablegroup_serializer_json_obj = json.loads(tablegroup_serializer_json)
			component = Component.objects.filter(transactionviewid_id = request.session['transactionviewid'])
			componet_ser =ComponentSerializer(instance=component,many=True)
			componet_ser_json= json.dumps(componet_ser.data)
			return render(request,'tableview.html',{'tablegroup_serializer':tablegroup_serializer_json_obj,'componet_ser_json':componet_ser_json})
		else:
			return HttpResponseBadRequest(json.dumps(contform.errors))		
	else:			
		form = ContainerForm(tranid = transaction_id,viewid = viewid)

	return render(request,'viewcomponent.html',{'tablegroup_serializer':tablegroup_serializer_json_obj,'componet_ser_json':componet_ser_json,'projectselect':projectselect,'view':view,'element':element,'viewtitle':viewtitle,'viewid':viewid,'project_id':project_id,'transaction_id':transaction_id,'form':form,'eupdatedetails':eupdatedetails,'epostdetails':epostdetails,'firesqlObj':firesqlObj})

@myuser_login_required
def tableview(request):
	element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])
	project_title = element.project_id.title
	projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])
	viewid = request.session['transactionviewid']
	component = Component.objects.filter(transactionviewid_id = request.session['transactionviewid'])
	componet_ser =ComponentSerializer(instance=component,many=True)
	componet_ser_json= json.dumps(componet_ser.data)
	tablegroup = Container.objects.filter(transactionviewid_id = viewid ).order_by('displayorder')
	tablegroup_serializer = ContainerSerializer(instance=tablegroup,many=True)
	tablegroup_serializer_json = json.dumps(tablegroup_serializer.data)
	tablegroup_serializer_json_obj = json.loads(tablegroup_serializer_json)
	return render(request,'tableview.html',{'element':element,'projectselect':projectselect,'tablegroup_serializer_json_obj':tablegroup_serializer_json_obj,'componet_ser_json':componet_ser_json})

@csrf_exempt
def tabledetails(request):
	dbtableid = request.POST.get('Dbtableid')
	if request.POST:
		dbtable = Txtabledetails.objects.filter(id = dbtableid)
		dbtable_serializer = TxtbdetailsSerializer(instance=dbtable,many=True)
		dbtable_serializer_json = json.dumps(dbtable_serializer.data)
		dbtable_serializer_json_obj = json.loads(dbtable_serializer_json)
		return HttpResponse(dbtable_serializer_json)
	else:
		return HttpResponseBadRequest("error")		

@myuser_login_required
def deletecontainer(request,contid):
	txviewid = request.session['viewid']
	container = Container.objects.get(pk = contid)
	container.delete()
	view = Transactionview.objects.get(pk = txviewid)
	view.createpage = False
	view.save()
	return HttpResponseRedirect('/transactionview/viewcomponent/%s'%request.session['transactionviewid'])

@myuser_login_required
def addcomponent(request,contid):
	request.session['containerid'] = contid
	viewid = request.session['viewid']
	containerid = contid
	transactionviewid =  request.session['transactionviewid']
	transactionview = Transactionview.objects.get(pk = transactionviewid)
	container = Container.objects.get(pk = contid)
	containerid = container.id
	if request.method == 'POST':
		form = ComponentForm(request.POST,contid = containerid,viewid = viewid)
		if form.is_valid():
			addcomponent = form.save(commit = False)
			addcomponent.identifiers = slugify(addcomponent.title).replace("-","_")
			addcomponent.transactionviewid_id =  transactionview.id
			addcomponent.containerid_id = container.id
			addcomponent.save()
			transactionview.createpage = False
			transactionview.save()
			return HttpResponseRedirect('/transactionview/viewcomponent/%s'%request.session['transactionviewid'])
	form = ComponentForm(contid = containerid,viewid = viewid)
	return render(request,'addcomponent.html',locals())


@csrf_exempt
def savecomponent(request,contid):
	container = Container.objects.get(pk = contid)
	viewid = request.session['viewid']
	transactionviewid =  request.session['transactionviewid']
	transactionview = Transactionview.objects.get(pk = transactionviewid)
	component_length = Component.objects.filter(containerid_id = contid).count()+1
	exist_dporder = Component.objects.filter(containerid_id = contid,displayorder = component_length)
	if len(exist_dporder)>0:
		component_length = component_length+1
	comprefer = json.loads(request.POST.get('jsonData'))
	if comprefer:
		form = ComponentForm(request.POST,contid = container.id,viewid = viewid)
		if form.is_valid():
			addcomponent = form.save(commit = False)
			if addcomponent.title:
				identifiers = slugify(addcomponent.title).replace("-","_")
				title = comprefer['title']
			else:
			   	identifiers = slugify(comprefer['field_slug']).replace("-","_")
			   	title = comprefer['field_slug']

			addcomponent.title = title
			addcomponent.identifiers = identifiers
			addcomponent.componentrefer_id = comprefer['id']
			addcomponent.componenttype = comprefer['datatype']
			addcomponent.dbcolumn = comprefer['field_slug']
			addcomponent.componentrefer_dt = request.POST.get('jsonData')
			addcomponent.transactionviewid_id =  transactionview.id
			addcomponent.containerid_id = container.id
			addcomponent.displayorder = component_length
			addcomponent.save()
			transactionview.createpage = False
			transactionview.save()
			tablegroup = Container.objects.filter(transactionviewid_id = transactionviewid).order_by('displayorder')
			tablegroup_serializer = ContainerSerializer(instance=tablegroup,many=True)
			tablegroup_serializer_json = json.dumps(tablegroup_serializer.data)
			tablegroup_serializer_json_obj = json.loads(tablegroup_serializer_json)
			component = Component.objects.filter(transactionviewid_id = request.session['transactionviewid'])
			componet_ser =ComponentSerializer(instance=component,many=True)
			componet_ser_json= json.dumps(componet_ser.data)
			return render(request,'tableview.html',{'tablegroup_serializer':tablegroup_serializer_json_obj})
		else:
			return HttpResponseBadRequest(json.dumps(form.errors))			

@myuser_login_required
def deletecomponent(request,contid):
	txviewid = request.session['viewid']
	component = Component.objects.get(pk = contid)
	component.delete()
	view = Transactionview.objects.get(pk = txviewid)
	view.createpage = False
	view.save()
	return HttpResponseRedirect('/transactionview/viewcomponent/%s'%request.session['transactionviewid'])

@myuser_login_required
def editcontainer(request,containid):
	viewid = request.session['transactionviewid']
	transaction_id = request.session['transactionid']
	containerid = containid
	model =Container.objects.get(pk = containid)
	if request.method == 'POST':
			form = ContainerForm(request.POST,instance=model,tranid = transaction_id,viewid = viewid)
			# postfixexp = form['expression'].value()
			if form.is_valid():
				editcontainer = form.save(commit = False)
				editcontainer.identifiers = slugify(editcontainer.title).replace("-","_")
				# editcontainer.postexp = json.dumps(parseEventsIntoMap(postfixexp));
				editcontainer.save()
				view = Transactionview.objects.get(pk = viewid)
				view.createpage = False
				view.save()
				tablegroup = Container.objects.filter(transactionviewid_id = viewid ).order_by('displayorder')
				tablegroup_serializer = ContainerSerializer(instance=tablegroup,many=True)
				tablegroup_serializer_json = json.dumps(tablegroup_serializer.data)
				tablegroup_serializer_json_obj = json.loads(tablegroup_serializer_json)
				component = Component.objects.filter(transactionviewid_id = request.session['transactionviewid'])
				componet_ser =ComponentSerializer(instance=component,many=True)
				componet_ser_json= json.dumps(componet_ser.data)
				return render(request,'tableview.html',{'tablegroup_serializer':tablegroup_serializer_json_obj,'componet_ser_json':componet_ser_json})
			else:
				return HttpResponseBadRequest(json.dumps(form.errors))
	else:
		form = ContainerForm(instance = model,tranid = transaction_id,viewid = viewid)
		return render(request,'contproperty.html',locals())

def parseEventsIntoMap(lines):
    event_dest={}
    statement_List =[]
    key =""
    event_obj = ""

    if lines:
		splited_lines = string.split(lines, '\r\n')
		for line in splited_lines:
			statement_List =[]
			if line:
				if line[0]=='{':
					key = str(line)
					if not event_dest.has_key(str(key)):
						event_dest[str(key)] = statement_List
				else:
					if key:
						statement_List = event_dest.get(key)
					if not statement_List:
						statement_List.append(str(line))
					else:
						statement_List.append(str(line))
	
		event_obj = adjustEvents(event_dest)             
    return event_obj

def adjustEvents(event_dest):
    adjustedEventdest = {}
    subEventdest = {}
    tempdest = {}

    for eventKey,eventVal in event_dest.iteritems():
        eventSign = []
        eventSign = getEventAndArguments(eventKey)
        if eventSign.__len__() > 1:
                eventName = str(eventSign[0].lower())
                arg1 = eventSign[1].lower()
                if not adjustedEventdest.has_key(eventName):
                        subEventdest = {}
                        if arg1:
                                subEventdest[arg1]= eventVal
                        else:
                                subEventdest["COMPEVENT"]= eventVal
                        adjustedEventdest[eventName]=subEventdest
                else:
                        tempdest =  adjustedEventdest.get(eventName)
                        tempdest[arg1]=eventVal
        elif eventSign.__len__() == 1:
                eventName = str(eventSign[0].lower())
                arg1 = "COMPEVENT"
                subEventdest = {}
                subEventdest[arg1]= eventVal
                adjustedEventdest[eventName] = subEventdest
    return adjustedEventdest

def getEventAndArguments(strLine):
        firstWord = ""
        restOfString = ""

        rpStrLine = strLine.replace("{", "").replace("}", "")

        temp = rpStrLine.split(" ")

        firstWord = temp[0]


        for index in range(len(temp)):
            if index != 0:
                restOfString += temp[index]
                restOfString += " "


        if len(restOfString) == 0:
            re = []
            re.append(firstWord)
            return re;
        else:
           alter = restOfString;
           re = []
           re.append(firstWord.strip())
           re.append(alter.strip())
           return re;

def creatingLogicalField(request,sql,txvId,containerid,title,do):

	sqlArray = sql.split("where")

	loginModel = userprofile.objects.get(is_user = True ,id = request.session['userid'])
	element =Projectwiseusersetup.objects.get(userid=loginModel.id,project_id = request.session['projectid'])
	if element:
		dbprofile = element.db_profileid_id

		dbProfileData = Db_profile.objects.get(pk=dbprofile)
		appDbId = dbProfileData.appdb_id
		appDbData = Db_connections_info.objects.get(pk=appDbId)

		host = appDbData.host
		username = appDbData.username
		password = appDbData.password
		database = appDbData.dbname 
		
		#Making connection
		db = MySQLdb.connect(host,username,password,database)
		cursor = db.cursor()

		try:
			cursor.execute(sqlArray[0])
			result = cursor.fetchone()	
			field_names = [i[0] for i in cursor.description]

			containerObj = Container.objects.get(id=containerid)
			txviewObj = Transactionview.objects.get(id=txvId)

			originaslFieldDO = do
			no_of_total_logical_field= 0
			no_of_total_logical_field = len(field_names)
			no_of_logical_existing_field = 0;
			last_existing_logical_field_do = 0;
			do_to_add = originaslFieldDO + no_of_total_logical_field

			#Find Display order of last logical field
			for field in field_names:
				try:
					componentObj = Component.objects.get(title="logical_"+title+"_"+field,containerid_id=containerid)

					if componentObj.displayorder > last_existing_logical_field_do:
						last_existing_logical_field_do = componentObj.displayorder

					no_of_logical_existing_field = no_of_logical_existing_field+1;

				except Component.DoesNotExist:
					print "New Field"



			if no_of_logical_existing_field>0:
				componentsToUpdateDO = Component.objects.filter(displayorder__gt = last_existing_logical_field_do,containerid_id=containerid).order_by('displayorder') #.values_list('displayorder')

			else:
				componentsToUpdateDO = Component.objects.filter(displayorder__gt = originaslFieldDO,containerid_id=containerid).order_by('displayorder') #.values_list('displayorder')


			#Updating other fields DO
			for comp in componentsToUpdateDO:
				do_to_add = do_to_add+1
				comp.displayorder = do_to_add
				comp.save()

			#Updating logical field DO
			for field in field_names:
				originaslFieldDO = originaslFieldDO+1

				try:
					componentObj = Component.objects.get(title="logical_"+title+"_"+field,containerid_id=containerid)
					componentObj.displayorder = originaslFieldDO
					componentObj.save()
				except Component.DoesNotExist:
					Component.objects.create(title="logical_"+title+"_"+field,
											caption="logical_"+title+"_"+field+field,
											is_hidden=True,
											widgettype="text",
											modeOfEntry = "tbe",
											componenttype="CharField",
											containerid=containerObj,
											transactionviewid=txviewObj,
											identifiers="logical_"+title+"_"+field,
											displayorder=originaslFieldDO,
											componentrefer_dt=""
											)
		
			return "Success"
		except Exception as e:
			print e
			return e


@myuser_login_required
def editcomponent(request,componid):
	viewid = request.session['transactionviewid']
	containerid = componid
	model = Component.objects.get(pk = containerid)
	contid = model.containerid_id
	componentrefer_id = model.componentrefer_id
	dbcolumn = model.dbcolumn
	componenttype = model.componenttype
	comprefer = model.componentrefer_dt
	if request.method == 'POST':

		form = ComponentForm(request.POST,instance=model,initial={'modeOfEntry':'tbe'},contid = contid,viewid = viewid)
		if form.is_valid():
			editcomponent = form.save(commit = False)
			editcomponent.componentrefer_id = componentrefer_id
			editcomponent.identifiers = slugify(editcomponent.title).replace("-","_")
			editcomponent.dbcolumn = dbcolumn
			editcomponent.componenttype = componenttype
			editcomponent.componentrefer_dt = comprefer
			editcomponent.save()
			if editcomponent.componenttype == "OneToOneField" and editcomponent.sql:
				sql = json.loads(editcomponent.sql)
				txvId = editcomponent.transactionviewid_id
				containerid =  editcomponent.containerid_id
				title = editcomponent.title
				do = editcomponent.displayorder
				res = creatingLogicalField(request,sql['Sql'],txvId,containerid,title,do)
				if res != "Success":
					return HttpResponseBadRequest(res)
			
					
			view = Transactionview.objects.get(pk = viewid)
			view.createpage = False
			view.save()
			tablegroup = Container.objects.filter(transactionviewid_id = viewid ).order_by('displayorder')
			tablegroup_serializer = ContainerSerializer(instance=tablegroup,many=True)
			tablegroup_serializer_json = json.dumps(tablegroup_serializer.data)
			tablegroup_serializer_json_obj = json.loads(tablegroup_serializer_json)
			component = Component.objects.filter(transactionviewid_id = request.session['transactionviewid'])
			componet_ser =ComponentSerializer(instance=component,many=True)
			componet_ser_json= json.dumps(componet_ser.data)
			return render(request,'tableview.html',{'tablegroup_serializer':tablegroup_serializer_json_obj,'componet_ser_json':componet_ser_json})
		else:
			return HttpResponseBadRequest(json.dumps(form.errors))
	else:
		form = ComponentForm(instance = model,initial={'modeOfEntry':'tbe'},contid = contid,viewid = viewid)
		return render(request,'comproperty.html',{'form':form,'containerid':containerid})


@myuser_login_required
def componentSQLModal(request):
	return render(request,'sqlmodal.html',locals())


def eupdateAdd(request,txviewid):
	viewid = txviewid
	tx = ""
	eform = EupdateForm(viewid = txviewid,tx = tx)
	return render(request,'eupdatemodal.html',{'eform':eform,'viewid':viewid})

def eupdateEdit(request,eupdateid):
	tx = ""
	element = Eupdate.objects.get(id = eupdateid)
	targettx = Transactionview.objects.filter(savetype =element.updatetype,projectid_id = element.projectid_id)
	component = Component.objects.filter(transactionviewid_id = element.targettxview_id)
	txviewid = element.transactionview_id
	if request.POST:
		if request.POST.get('targettxview'):
			tx = request.POST.get('targettxview')
		eform = EupdateForm(request.POST,instance=element,viewid = txviewid,tx = tx)
		eformedit = eform.save(commit = False)
		eformedit.targettxview_id = request.POST.get('targettxview')
		eformedit.target_ui_field_id = request.POST.get('target_ui_field')
		eformedit.save()
		eupdatedetails = Eupdate.objects.filter(transactionview_id = element.transactionview_id)
		return render(request,'eupdatetableview.html',{'eupdatedetails':eupdatedetails})

	else:
		eform = EupdateForm(instance=element,viewid = txviewid,tx = tx)
		return render(request,'eupdatemodal.html',{'eform':eform,'viewid':txviewid,'element':element,'targettx':targettx,'component':component,'epudateedit':'edit'})

@csrf_exempt
def eupdatetype(request):
	try:
		data = serializers.serialize("json", Transactionview.objects.filter(savetype = request.POST['type'],projectid_id = request.session['projectid']))
		return HttpResponse(data)
	except Exception as e:
		print e
		return HttpResponseBadRequest('error')

@csrf_exempt
def eupdate_trfields(request):
	try:
		data = serializers.serialize("json", Component.objects.filter(transactionviewid_id = request.POST['tx']))
		return HttpResponse(data)
	except Exception as e:
		print e
		return HttpResponseBadRequest('error')

@csrf_exempt
def eupdateSave(request,txviewid):
	tx = ""
	if request.POST:
		if request.POST.get('targettxview'):
			tx = request.POST.get('targettxview')
		form = EupdateForm(request.POST,viewid = txviewid,tx=tx)
		if form.is_valid():
			eupdatesave = form.save(commit = False)
			eupdatesave.targettxview_id = request.POST.get('targettxview')
			eupdatesave.target_ui_field_id = request.POST.get('target_ui_field')
			eupdatesave.transactionview_id = txviewid
			eupdatesave.projectid_id  = request.session['projectid']
			eupdatesave.save()
			eupdatedetails = Eupdate.objects.filter(transactionview_id = txviewid)
			return render(request,'eupdatetableview.html',{'eupdatedetails':eupdatedetails})
		else:
			print form.errors
			return HttpResponseBadRequest(json.dumps(form.errors))

@csrf_exempt
def eupdateDelete(request,eupdateid):
	try:
		query = Eupdate.objects.get(id = eupdateid)
		txviewid = query.transactionview_id
		query.delete()
		eupdatedetails = Eupdate.objects.filter(transactionview_id = txviewid)
		return render(request,'eupdatetableview.html',{'eupdatedetails':eupdatedetails})
	except Exception as e:
		print e
		return HttpResponseBadRequest('error')



EpostMapFormSet = modelformset_factory(EpostMapField,form = EpostMapForm,can_delete=True,extra=1)

@csrf_exempt
def epostadd(request,txviewid):
	viewid = txviewid
	tx = ""
	pid = request.session['projectid']
	epostForm = EpostForm()
	epostForm.fields['target_tx_view'].queryset = Transactionview.objects.filter(Q(projectid_id=pid) & ~Q(id=viewid))
	epostForm.fields['based_on_container'].queryset = Container.objects.filter(transactionviewid_id=viewid)
	epostForm.fields['ui_control_field'].queryset = Component.objects.filter(transactionviewid_id=viewid)
	# EpostMapFormSet = modelformset_factory(EpostMapField,form = EpostMapForm,extra=1,can_delete=True)
	formset = EpostMapFormSet(queryset=EpostMapField.objects.none(),form_kwargs={'viewid': viewid,'tx':tx})
	return render(request,'epostaddmodal.html',locals())

@csrf_exempt
def eposttarget(request,txviewid):
	try:
		component = Component.objects.filter(transactionviewid_id = txviewid)
		tablegroup_serializer = EpostComponentSerializer(instance=component,many=True)
		tablegroup_serializer_json = json.dumps(tablegroup_serializer.data)
		return HttpResponse(tablegroup_serializer_json)
	except Exception as e:
		print e
		return HttpResponseBadRequest("error")

@csrf_exempt
@transaction.atomic
def epostSave(request,txviewid):
	tx = ""
	viewid = txviewid
	pid = request.session['projectid']
	epostform = EpostForm(request.POST)
	if request.POST.get('target_tx_view'):
		tx = request.POST.get('target_tx_view')
	print epostform.errors
	if epostform.is_valid():
		newform = epostform.save(commit = False)
		newform.source_tx_view_id = txviewid
		newform.projectid_id = pid
		newform.save()
		formset = EpostMapFormSet(request.POST,queryset=EpostMapField.objects.none(),form_kwargs={'viewid': viewid,'tx':tx})
		print formset.errors

		for form in formset:
			if form.is_valid():
				print form.is_valid()
				try:
					if form.cleaned_data.get('DELETE') and form.instance.pk:
						form.instance.delete()
					else:
						instance = form.save(commit=False)
						instance.epost_id = newform.id
						try:
							instance.save()
							#messages.success(request, "saved successfully")
						except Exception as e:
							print e
							return HttpResponseBadRequest("error")


				except:
					return HttpResponseBadRequest("error")

			else:
				formsetErrorArray =  json.dumps(formset.errors)
				return HttpResponseBadRequest(json.dumps(formset.errors))

		epostdetails = Epost.objects.filter(source_tx_view_id = txviewid)
		return render(request,'epostTableview.html',locals())
	else:
		return HttpResponseBadRequest("error")

@csrf_exempt
def epostDelete(request,epostid):
	try:
		query = Epost.objects.get(id = epostid)
		txviewid = query.source_tx_view_id
		query.delete()
		epostdetails = Epost.objects.filter(source_tx_view_id = txviewid)
		return render(request,'epostTableview.html',{'epostdetails':epostdetails})
	except Exception as e:
		print e
		return HttpResponseBadRequest('error')

@csrf_exempt
def epostEdit(request,epostid,txviewid):
	tx = ""
	viewid = txviewid
	element = Epost.objects.get(id = epostid)
	pid = request.session['projectid']
	tx = element.target_tx_view_id
	epostForm = EpostForm(instance = element)
	epostForm.fields['target_tx_view'].queryset = Transactionview.objects.filter(Q(projectid_id=pid) & ~Q(id=txviewid))
	epostForm.fields['based_on_container'].queryset = Container.objects.filter(transactionviewid_id=txviewid)
	epostForm.fields['ui_control_field'].queryset = Component.objects.filter(transactionviewid_id=txviewid)
	formset = EpostMapFormSet(queryset=EpostMapField.objects.filter(epost_id = element.id),form_kwargs={'viewid': viewid,'tx':tx})

	return render(request,'epostaddmodal.html',locals())

@csrf_exempt
@transaction.atomic
def epostUpdate(request,epostid,txviewid):
	tx = ""
	viewid = txviewid
	if request.POST.get('target_tx_view'):
		tx = request.POST.get('target_tx_view')
	element = Epost.objects.get(id = epostid)
	epostForm = EpostForm(request.POST,instance = element)

	if epostForm.is_valid():
		epostForm.save()
		formset = EpostMapFormSet(request.POST,queryset=EpostMapField.objects.filter(epost_id = element.id),form_kwargs={'viewid': viewid,'tx':tx})

		if formset.deleted_forms:
			for form in formset.deleted_forms:

				form.instance.delete()

		if formset.is_valid():
			instance = formset.save(commit = False)
			for item in instance:
				item.epost_id = element.id
				try:
					item.save()
				except Exception as e:
					print e
					return HttpResponseBadRequest("error")


		else:
			return HttpResponseBadRequest("error")

		epostdetails = Epost.objects.filter(source_tx_view_id = txviewid)
		return render(request,'epostTableview.html',locals())

		
	else:
		return HttpResponseBadRequest("error")

@csrf_exempt
def firesqlAdd(request,txviewid): 

	tx = ""
	viewid = txviewid

	if request.method == "POST":
	
		form = FireSqlForm(request.POST)
		title = request.POST.get('title')
		
		if form.is_valid():
			newform = form.save(commit = False)
			newform.slug = slugify(title).replace("-","_")
			newform.transactionview_id = viewid
			try:
				newform.save()
				return HttpResponse("Success")
			except Exception as e:
				print e
				return HttpResponse("Failure1")
		else:
			print form.errors
			return HttpResponse("Failure2")

	else:

		form=FireSqlForm()
		return render (request,'firesqlmodal.html',locals())

def firesqlEdit(request,txviewid,firesqlid):

	tx = ""
	viewid = txviewid

	firesqlComponent = FireSql.objects.get(id=firesqlid)


	if request.method == "POST":

		form = FireSqlForm(request.POST,instance=firesqlComponent)
		title = request.POST.get('title')

		if form.is_valid():
			newform = form.save(commit = False)
			newform.slug = slugify(title).replace("-","_")
			try:
				newform.save()
				return HttpResponse("Success")
			except Exception as e:
				print e
				return HttpResponse("Failure1")
		else:
			print form.errors
			return HttpResponse("Failure2")

	else:

		form = FireSqlForm(instance = firesqlComponent)
		return render (request,'firesqleditmodal.html',locals())

def delFireSql(request,firesqlid):
	query = FireSql.objects.get(id=firesqlid)
	query.delete()
	return HttpResponseRedirect('/transactionview/viewcomponent/%s'%request.session['transactionviewid'])



filePath = settings.MEDIA_ROOT

@myuser_login_required
def generatepage(request,txviewid):
	projectid = request.session['projectid']
	project = Project.objects.get(pk = projectid)
	ptitle = project.slug
	view = Transactionview.objects.get(id = txviewid)
	viewid = view.id
	view.createpage = True
	view.save()
	txnid = view.transactionid_id
	txnObj = Transaction.objects.get(id=txnid)

	if not os.path.exists(filePath+"static/ionicmeta/"+ptitle):
		os.makedirs(filePath+"static/ionicmeta/"+ptitle)
	if txnObj.txname == "Muser":
		#call restOfString
		print "REGISTERATION PAGE CREATION"
		logintemplate.views.generateRegTemplate(viewid,ptitle)
		return HttpResponse('success')

	else:
		try:
			temphtml = ionichtml(viewid,ptitle)
			return HttpResponse('success')
		except Exception as e:
			return HttpResponseBadRequest(e)


def txnCreation(pid,txviewid):
	projectid = pid
	project = Project.objects.get(pk = projectid)
	ptitle = project.slug
	try:
		if not os.path.exists(filePath+"static/ionicmeta/"+ptitle):
			os.makedirs(filePath+"static/ionicmeta/"+ptitle)

		temphtml = ionichtml(txviewid,ptitle)
		return HttpResponse('success')
	except Exception as e:
		raise Exception('Error In '+transaction.title+' Page Creation.Please Check.')

def printhtml(request):
	filenames = ["/home/bcs/Mobilebuilder/ionichtml/model.html", "/home/bcs/Mobilebuilder/ionichtml/mine.html"]
	# Folder name in ZIP archive which contains the above files
	# E.g [thearchive.zip]/somefiles/file2.txt
	# FIXME: Set this to something better
	zip_subdir = "pages"
	zip_filename = "%s.zip" % zip_subdir
	# Open StringIO to grab in-memory ZIP contents
	s = StringIO.StringIO()
	# The zip compressor
	zf = zipfile.ZipFile(s, "w")
	for fpath in filenames:
		# Calculate path for file in zip
		fdir, fname = os.path.split(fpath)
		zip_path = os.path.join(zip_subdir, fname)
		# Add file, at correct path
		zf.write(fpath, zip_path)

	# Must close zip for all contents to be written
	zf.close()

	# Grab ZIP file from in-memory, make response with correct MIME-type
	resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
	# ..and correct content-disposition
	resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
	return resp

def metajson(request):
	lines =""
	with open("ionichtml/app.module.ts") as f:
		lines = f.readlines()
		#print lines
		i = lines.index("import { HomePage } from '../pages/home/home';\n")
		try:
			if lines.index("Different random text;\n"):
				line2 = lines.index("Different random text;\n")

		except:
			lines.insert(i+1, "Different random text;\n")
			d = lines.index( '  declarations: [\n')
			ent = lines.index( '  entryComponents: [\n')
			lines.insert(ent+2, "    fileNamePage,\n")

	with open("ionichtml/app.module.ts","w") as file:
		for tslines in lines:
			file.write(tslines)

	return HttpResponse("success")

def ionicpages(request):
	projectid = request.session['projectid']
	transgroup = Transactionview.objects.filter(projectid_id = projectid)
	project = Project.objects.get(pk = projectid)
	projectTitle = project.slug
	for transaction in transgroup:
		#print transaction.id
		pages = pagemeta(transaction.id,projectTitle)
	return  HttpResponse("success")

def pagemeta(viewid,ptitle):
	filePath = settings.MEDIA_ROOT
	try:
		transaction = Transactionview.objects.get(id = viewid)
		transgroup = Transactionview.objects.filter(id = viewid)
		tran_serializer = ViewtreeSerializer(instance=transgroup,many=True)
		tran_serializer_json = json.dumps(tran_serializer.data)
		fileName = tran_serializer.data[0]['idt'].lower().replace(" ","")
		if os.path.exists(filePath+"static/ionicmeta/"+ptitle+"/"+fileName+"/"+fileName+".html"):
			if not os.path.exists(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName):
				os.makedirs(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName)

			with open(filePath+"static/ionicmeta/"+ptitle+"/"+fileName+"/"+fileName+".html") as f:
				with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".html", "w") as f1:
					for line in f:
						f1.write(line)

			if tran_serializer.data[0]['vt'] == 'carousel' or tran_serializer.data[0]['vt'] == 'grid':
				glist = []
				try:
					cont_meta = tran_serializer.data[0]['cont_meta']
					for cont in cont_meta:
						if cont['ctype'] == 'grid':
							glist.append(cont['idt'])

						if cont['children']:
							#print cont['children']
							child_meta = cont['children']
							for child in child_meta:
								if child['ctype'] == 'grid':
									glist.append(child['idt'])


					if glist:
						#print glist
						for gl in glist:
							gridfileName = fileName+gl
							if not os.path.exists(filePath+"ionicapps/"+ptitle+"/src/pages/"+gridfileName+"modal"):
								os.makedirs(filePath+"ionicapps/"+ptitle+"/src/pages/"+gridfileName+"modal")

							try:
								with open(filePath+"static/ionicmeta/"+ptitle+"/"+gridfileName+"modal/"+gridfileName+"modal.html") as f:
									with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+gridfileName+"modal/"+gridfileName+"modal.html", "w") as f1:
										for line in f:
											f1.write(line)

							except Exception as e:
								print e
								with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+gridfileName+"modal/"+gridfileName+"modal.html", "w") as f1:
									f1.write("<ion-content></ion-content>")

							modelfile = modeltsfile(gridfileName+"modal",ptitle)

				except Exception as e:
					print e

		tsPage = tsFile(fileName,ptitle,tran_serializer)
		scssPage = scssFile(fileName,ptitle)
		metajson = pagejson(fileName,ptitle)
		copyTxnTemplate(viewid,fileName,ptitle)
		return "success"
	except Exception as e:
		print e
		raise Exception('Error In '+transaction.title+' Page Creation.Please Check.')
		return "error"


def copyTxnTemplate(viewid,fileName,ptitle):
	filePath = settings.MEDIA_ROOT
	txviewObj = Transactionview.objects.get(id = viewid)
	try:
		actionObj = Actions.objects.get(transactionviewid_id = viewid,actiontype="PrintFormat")
		txnPFObj = TxnPrintFormatAction.objects.get(actiontype_id = actionObj.id)
	except Actions.DoesNotExist:
		actionObj = None
		txnPFObj = None

	if txnPFObj:
		pfConfigObj = PrintFormat.objects.get(id=txnPFObj.pfconfig_id)

		FileUrl = pfConfigObj.htmlfile
		print filePath+str(FileUrl)

		if os.path.exists(filePath+str(FileUrl)):
			if not os.path.exists(filePath+"ionicapps/"+ptitle+"/src/assets/mustache"):
				os.makedirs(filePath+"ionicapps/"+ptitle+"/src/assets/mustache")

			with open(filePath+str(FileUrl)) as f:
				with open(filePath+"ionicapps/"+ptitle+"/src/assets/mustache/"+fileName+".html", "w") as f1:
					for line in f:
						f1.write(line)
		else:
			raise Exception("Could not a find a uplaoded jasper file for "+txviewObj.identifiers+" view")

	return "success"

def txncss(request,txviewid):
	element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])
	projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])
	view = Transactionview.objects.get(pk = txviewid)
	csstxn = txnCssutilites.objects.filter(transactionview_id = txviewid)
	if csstxn:
		txncss = txnCssutilites.objects.get(transactionview_id = txviewid)
		form = CssTxnForm(request.POST or None,instance =  txncss)
	else:
		form = CssTxnForm(request.POST or None)
	if request.POST:
		if form.is_valid():
			csstxn = form.save(commit = False)
			csstxn.transactionview_id = txviewid
			csstxn.save()
			return HttpResponse('success')
		else:
			return HttpResponseBadRequest(form.errors)
	return render(request,'cssutilites.html',locals())


def pagejson(fileName,ptitle):
	filePath = settings.MEDIA_ROOT
	if os.path.exists(filePath+"static/ionicmeta/"+ptitle+"/"+fileName+"/"+fileName+".json"):
			if not os.path.exists(filePath+"ionicapps/"+ptitle+"/src/assets/json"):
				os.makedirs(filePath+"ionicapps/"+ptitle+"/src/assets/json")

			with open(filePath+"static/ionicmeta/"+ptitle+"/"+fileName+"/"+fileName+".json") as f:
				with open(filePath+"ionicapps/"+ptitle+"/src/assets/json/"+fileName+".json", "w") as f1:
					for line in f:
						f1.write(line)

	return "success"

def ionichtml(viewid,ptitle):
	txviewid = viewid
	filePath = settings.MEDIA_ROOT
	completehtml =""
	carsouelChild=""
	scssPage =""
	tsPage =""
	transgroup = Transactionview.objects.filter(id = viewid)
	tran_serializer = ViewtreeSerializer(instance=transgroup,many=True)
	tran_serializer_json = json.dumps(tran_serializer.data)
	actiongroup = Actions.objects.filter(transactionviewid_id = viewid)
	action_serializer = ActionsSerializer(actiongroup,many = True)
	fileName = tran_serializer.data[0]['idt'].lower().replace(" ","")
	fabbutton  = action_serializer.data
	projectid = tran_serializer.data[0]['pt']
	css_txn = txnCssutilites.objects.filter(transactionview_id = viewid)
	home = Homepage.objects.filter(project_id_id = projectid)
	if css_txn:
		header_type = css_txn[0].ionic_header
		header_color = css_txn[0].header_color
		header_label_cr = css_txn[0].header_label_color
		label_cr = css_txn[0].label_color
		if css_txn[0].custom_header_title != "" and css_txn[0].custom_header_title != None:
			header_title = css_txn[0].custom_header_title
		else:
			header_title = tran_serializer.data[0]['tt']
		if css_txn[0].background != "" and css_txn[0].background != None:
			print css_txn[0].background
			print "color arun"
			bgcolor =  'class="bg-'+css_txn[0].background+'"'
			print bgcolor
		else:
			bgcolor =""
			print "no color"
	else:
		header_type = 'fix'
		header_color = 'yes'
		header_title = tran_serializer.data[0]['tt']
		bgcolor =""
		header_label_cr = 'primary'
		label_cr = 'primary'

	if tran_serializer.data[0]['vt'] == 'carousel':

		if fabbutton:
			fabconthtml = fab(fabbutton,header_color,home)
		else:
			fabconthtml=""""""

		carouselStart = """<ion-slides pager>"""
		carouselEnd ="""</ion-slides>"""
		slideStart ="""<ion-slide><ion-scroll scrollY="true" style="height:500px">"""
		slideEnd = """</ion-scroll></ion-slide>"""
		formhtml = tran_serializer.data[0]
		viewtype = tran_serializer.data[0]['vt']
		bodyhtml = typeofView(formhtml,viewtype,ptitle,label_cr)
		if formhtml['cont_meta'][0]['children']:
			children_sorted = sorted(formhtml['cont_meta'][0]['children'],key = itemgetter('do'))
			for child in children_sorted:
				childbody = children(child,fileName,ptitle)
				carsouelChild += slideStart+childbody+slideEnd


		completehtml =  carouselStart+slideStart+bodyhtml+slideEnd+carsouelChild+carouselEnd
		# if not os.path.exists(filePath+"static/ionicmeta/"+ptitle+"/"+fileName+"modal"):
		# 	os.makedirs(filePath+"static/ionicmeta/"+ptitle+"/"+fileName+"modal")

		# Html_file= open(filePath+"static/ionicmeta/"+ptitle+"/"+fileName+"modal/"+fileName+"modal.html","w")
		# Html_file.write("<ion-content></ion-content>")
		# Html_file.close()

	else:
		formhtml = tran_serializer.data[0]
		viewtype = tran_serializer.data[0]['vt']
		completehtml = typeofView(formhtml,viewtype,ptitle,label_cr)
		if fabbutton:
			fabconthtml = fab(fabbutton,header_color,home)
		else:
			fabconthtml=""""""



	try:
		content_start ="""<ion-content """+bgcolor+""">"""
		form_start ="""<form id="myForm" name="myForm" data-eformid=\""""+tran_serializer.data[0]['idt']+"""\">"""
		hhtml =""
		h_start = """<ion-header>"""
		h_end = """</ion-header>"""
		if home[0].menutype == "sidemenu":
			if header_color == 'yes':
				hhtml="""<div *ngIf="!viewMode"><ion-toolbar color="primary"><ion-buttons """+home[0].sidemenu+"""><button ion-button menuToggle><ion-icon name="menu"></ion-icon></button></ion-buttons><ion-title>"""+tran_serializer.data[0]['tt']+"""</ion-title></ion-toolbar></div><div *ngIf="viewMode"><ion-navbar color="primary"><ion-title>"""+tran_serializer.data[0]['tt']+"""</ion-title><ion-buttons *ngIf="modifyMode" end><button color="secondary" ion-button clear (click)="save($event)"  data-modetype="modify" data-exp="">save</button></ion-buttons></ion-navbar></div>"""+fabconthtml
			else:
				hhtml="""<div *ngIf="!viewMode"><ion-toolbar class="toolbar_hd_no"><ion-buttons """+home[0].sidemenu+"""><button ion-button menuToggle class="menu_hd_no"><ion-icon name="menu"></ion-icon></button></ion-buttons><ion-title><div class="menu_hd_no">"""+tran_serializer.data[0]['tt']+"""</div></ion-title></ion-toolbar></div><div *ngIf="viewMode"><ion-navbar ><ion-title><div menu_hd_no>"""+tran_serializer.data[0]['tt']+"""</div></ion-title><ion-buttons *ngIf="modifyMode" end><button color="primary" ion-button clear (click)="save($event)"  data-modetype="modify" data-exp="">save</button></ion-buttons></ion-navbar></div>"""+fabconthtml

		else:
			if header_color == 'yes':
				hhtml="""<ion-navbar color="primary"><ion-title>"""+header_title+"""</ion-title><ion-buttons *ngIf="modifyMode" end><button color="secondary" ion-button clear (click)="save($event)"  data-modetype="modify" data-exp="">save</button></ion-buttons></ion-navbar>"""+fabconthtml
			else:
				hhtml="""<ion-navbar><ion-title><div class="menu_hd_no">"""+header_title+"""</div></ion-title><ion-buttons *ngIf="modifyMode" end><button color="primary" ion-button clear (click)="save($event)"  data-modetype="modify" data-exp="">save</button></ion-buttons></ion-navbar>"""+fabconthtml

		if header_type == 'flex':
			headerhtml =  content_start+form_start+hhtml
		elif header_type == 'noheader':
			title_css =""
			if css_txn[0].background != "" and css_txn[0].background != None:
				title_css = 'class="title_color"'
			else:
				title_css = 'class="title_color_primary"'

			logout =fabconthtml
			root_page = RootPage.objects.filter(project_id = projectid)

			if root_page[0].pageoption != 'default':
				if root_page[0].pageValue.transactionview:
					if root_page[0].pageValue.transactionview_id == txviewid:
						logout ="""<button ion-button icon-end clear class="icon_logout" (click)="logout()"><ion-icon name="exit"></ion-icon></button>"""
			headerhtml =  content_start+"""<ion-row><ion-col col-2></ion-col><ion-col col-8><ion-title class="no_header_title"><div """+title_css+""">"""+header_title+"""</div></ion-title></ion-col><ion-col col-2>"""+logout+"""</ion-col></ion-row>"""+form_start
		else:
			headerhtml =  h_start+hhtml+h_end+content_start+form_start


	except Exception as e:
		print e
		raise Exception("Please select Menu Type in HomePage.")

	#headerhtml="""<ion-header><ion-navbar><ion-title>"""+tran_serializer.data[0]['tt']+"""</ion-title></ion-navbar>"""+fabconthtml+"""</ion-header><ion-content><form id="myForm" name="myForm">"""
	footerhtml="""</form></ion-content>"""
	transactionhtml = headerhtml+completehtml+footerhtml
	#Html_file= open("ionichtml/transaction.html","w")
	if not os.path.exists(filePath+"static/ionicmeta/"+ptitle+"/"+fileName):
		os.makedirs(filePath+"static/ionicmeta/"+ptitle+"/"+fileName)

	Html_file= open(filePath+"static/ionicmeta/"+ptitle+"/"+fileName+"/"+fileName+".html","w")
	Html_file.write(transactionhtml)
	Html_file.close()
	jsonMeta = ionicmetaJson(tran_serializer_json,fileName,ptitle)
	return "success"

def ionicmetaJson(tranjson,fileName,ptitle):
	filePath = settings.MEDIA_ROOT
	if not os.path.exists(filePath+"static/ionicmeta/"+ptitle+"/"+fileName):
		os.makedirs(filePath+"static/ionicmeta/"+ptitle+"/"+fileName)

	json_file= open(filePath+"static/ionicmeta/"+ptitle+"/"+fileName+"/"+fileName+".json","w")
	json_file.write(tranjson)
	json_file.close()


def tsFile(fileName,ptitle,tran_serializer):
	filePath = settings.MEDIA_ROOT
	with open(filePath+"static/ionicsrc/transaction/transaction.ts") as f:
		with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".ts", "w") as f1:
			for line in f:
				f1.write(line)

	with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".ts", "r") as file :
		filedata = file.read()

	# Replace the target string
	filedata = filedata.replace('page-transaction', 'page-'+fileName)
	filedata = filedata.replace('transaction.html', fileName+'.html')
	filedata = filedata.replace('TransactionPage', fileName.capitalize()+'Page')
	filedata = filedata.replace('transaction.json', fileName+'.json')
	# Write the file out again
	with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".ts", "w") as file:
		file.write(filedata)

	appincludeTs(fileName,ptitle)
	if tran_serializer.data[0]['vt'] == 'carousel' or tran_serializer.data[0]['vt'] == 'grid':
		glist = []
		try:
			cont_meta = tran_serializer.data[0]['cont_meta']

			for cont in cont_meta:
				if cont['ctype'] == 'grid':
					glist.append(cont['idt'])

				if cont['children']:
					child_meta = cont['children']
					for child in child_meta:
						if child['ctype'] == 'grid':
							glist.append(child['idt'])
							#print glist

			if glist:
				with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".ts") as modalfile :
					lines = modalfile.readlines()

				for gl in glist:
					gridfilename = fileName+gl
					imp = lines.index("import { HomePage } from '../home/home';\n")
					lines.insert(imp+1, "import { "+gridfilename.capitalize()+"modalPage } from '../"+gridfilename+"modal/"+gridfilename+"modal';\n")
					md = lines.index('        this.modelpages = [\n')
					lines.insert(md+1,"      { id: '"+gl+"', component: "+gridfilename.capitalize()+"modalPage },\n")



				with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".ts","w") as file:
					for mdpages in lines:
						file.write(mdpages)

		except Exception as e:
			print "no grid"
			print e

	return filedata

def appincludeTs(fileName,ptitle):
	filePath = settings.MEDIA_ROOT
	with open(filePath+"ionicapps/"+ptitle+"/src/app/app.module.ts") as f:
		lines = f.readlines()
		#print lines
		imp = lines.index("import { HomePage } from '../pages/home/home';\n")
		try:
			if lines.index("import { "+fileName.capitalize()+"Page } from '../pages/"+fileName+"/"+fileName+"';\n"):
				i = lines.index("import { "+fileName.capitalize()+"Page } from '../pages/"+fileName+"/"+fileName+"';\n")

		except:
			lines.insert(imp+1, "import { "+fileName.capitalize()+"Page } from '../pages/"+fileName+"/"+fileName+"';\n")
			dec = lines.index( '  declarations: [\n')
			lines.insert(dec+2, "    "+fileName.capitalize()+"Page,\n")
			ent = lines.index( '  entryComponents: [\n')
			lines.insert(ent+2, "    "+fileName.capitalize()+"Page,\n")
			#print imp

	with open(filePath+"ionicapps/"+ptitle+"/src/app/app.module.ts","w") as file:
		for tslines in lines:
			file.write(tslines)

	return lines


def scssFile(fileName,ptitle):
	filePath = settings.MEDIA_ROOT
	with open(filePath+"static/ionicsrc/transaction/transaction.scss") as f:
		with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".scss", "w") as f1:
			for line in f:
				f1.write(line)

	with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".scss", "r") as file :
		filedata = file.read()

	# Replace the target string
	filedata = filedata.replace('page-transaction', 'page-'+fileName)
	# Write the file out again
	with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".scss", "w") as file:
		file.write(filedata)

	return filedata


def typeofView(formhtml,viewtype,ptitle,label_cr):
	conthtml =""
	fileName = formhtml['idt'].lower().replace(" ","")
	conthtml = formhtml['cont_meta']

	if conthtml[0]['ctype'] == 'card':
		cardhtml = card(conthtml[0],viewtype,fileName,ptitle,label_cr)
		bodyhtml =cardhtml

	if conthtml[0]['ctype'] == 'list':
		listhtml = lists(conthtml[0],viewtype,fileName,ptitle,label_cr)
		bodyhtml =listhtml

	if conthtml[0]['ctype'] == 'grid':
		idt = conthtml[0]['idt']
		gridhtml = grid(conthtml[0],viewtype,fileName+idt,ptitle,label_cr)
		bodyhtml = gridhtml

	return bodyhtml


def fab(fabbutton,header_color,home):
	try:
		fab_postion =""
		if home:
			if home[0].menutype == "sidemenu":
				if home[0].sidemenu == "right":
					fab_postion = """top left"""
				else:
					fab_postion = """top right"""
			else:
				fab_postion = """top right"""

		fab_class = 'class="fab_color_no"'
		if header_color =="yes":
			fab_class = 'class="fab_color_yes"'

		fabhtml = ""
		fabstart =""
		fabend=""
		fablist =""
		fabstart="""<div *ngIf="!viewMode"><ion-fab """+fab_postion+"""><button ion-fab mini style="margin:0px;" """+fab_class+"""><ion-icon name="star"></ion-icon></button><ion-fab-list side="bottom" style="margin:44px -8px">"""
		for fab  in fabbutton:
			if fab['at'] ==  'Save':
				save = fab['save']
				if save:
					fablist += """<button ion-fab form="form_id" (click)="save($event)" class="save_fab" data-modetype="normal" data-exp=\""""+save['exp']+"""\" data-pos=\""""+save['pos']+"""\"><ion-icon name=\""""+save['icls']+"""\"></ion-icon><ion-label>Save</ion-label></button>"""
				else:
					fablist+=""""""

			if fab['at'] == 'Cancel':
				cancel = fab['cancel']
				if cancel:
					fablist += """<button ion-fab (click)="cancel()"  class="cancel_fab" data-exp=\""""+cancel['exp']+"""\" data-pos=\""""+cancel['pos']+"""\""><ion-icon name=\""""+cancel['icls']+"""\" ></ion-icon><ion-label>Cancle</ion-label></button>"""
				else:
					fablist+=""""""

			if fab['at'] == 'New':
				new = fab['new']
				if new:
					fablist += """<button ion-fab (click)="new()"  class="new_fab" data-exp=\""""+new['exp']+"""\" data-pos=\""""+new['pos']+"""\"><ion-icon name=\""""+new['icls']+"""\"></ion-icon><ion-label>New</ion-label></button>"""
				else:
					fablist+=""""""

			if fab['at'] == 'Delete':
				delete = fab['delete']
				if delete:
					fablist += """<button ion-fab (click)="delete()"  class="delete_fab" data-exp=\""""+delete['exp']+"""\" data-pos=\""""+delete['pos']+"""\"><ion-icon name=\""""+delete['icls']+"""\" ></ion-icon><ion-label>Delete</ion-label></button>"""
				else:
					fablist+=""""""

			if fab['at'] == 'Search':
				sfield =""
				search = fab['search']
				if search:
					if search['sf'] ==None:
						sfield =""
					else:
						sfield = search['sf']
					fablist += """<button ion-fab (click)="search($event)" class="search_fab"  data-sorttype=\""""+search['st']+"""\"  data-sortfield=\""""+sfield+"""\" data-chunksize=\""""+search['cs']+"""\" data-page_size=\""""+search['ps']+"""\" data-copytxview=\""""+search['c_tx']+"""\"><ion-icon name=\""""+search['icls']+"""\"></ion-icon><ion-label>Search</ion-label></button>"""
		    	else:
					fablist+=""""""

			if fab['at'] == 'PrintFormat':
				pf = fab['printformat']
				if pf:
					fablist += """<button ion-fab (click)="printPreview($event)" class="print_fab" data-exp=\""""+pf['exp']+"""\"><ion-icon name=\""""+pf['icls']+"""\" ></ion-icon><ion-label>Print</ion-label></button>"""
				else:
					fablist+=""""""


		fabend="""</ion-fab-list></ion-fab></div>"""
		fabhtml=fabstart+fablist+fabend
		return fabhtml
	except Exception as e:
		raise Exception("Action Configuration Error.Please Check!")

def card(card,vtype,fileName,ptitle,label_cr):
	cardbody=""
	childrenhtml=""
	headerhtml="""<ion-header><ion-navbar><ion-title>Ionic Blank</ion-title></ion-navbar></ion-header>"""
	cardstart ="""<ion-card class="card_list_padding">"""
	cardend="""</ion-card>"""
	if len(card['comp_meta'])>0:
		card_sorted = sorted(card['comp_meta'],key = itemgetter('do'))
		for comp in card_sorted:
			try:
				if comp['wt'] == 'text':
					cardbody += text(comp,card['itype'],label_cr)

				if comp['wt'] =='email':
					cardbody += email(comp,card['itype'],label_cr)

				if comp['wt'] =='password':
					cardbody +=	password(comp,card['itype'],label_cr)

				if comp['wt'] =='textarea':
					cardbody += textarea(comp,card['itype'],label_cr)

				if comp['wt'] == 'select':
					cardbody +=	select(comp,card['itype'],label_cr)

				if comp['wt'] == 'button':
					cardbody +=button(comp,card['itype'])

				if comp['wt'] =='date':
					cardbody +=date(comp,card['itype'],label_cr)

				if comp['wt'] =='time':
					cardbody +=time(comp,card['itype'],label_cr)

				if comp['wt'] =='number':
					cardbody +=number(comp,card['itype'],label_cr)

				if comp['wt'] =='radio':
					cardbody +=radiobox(comp,card['itype'],label_cr)

				if comp['wt'] =='check':
					cardbody +=checkbox(comp,card['itype'],label_cr)

				if comp['wt'] =='scan':
					cardbody +=scan(comp,card['itype'],label_cr)

				if comp['wt'] =='stot':
					cardbody +=stot(comp,card['itype'],label_cr)

				if comp['wt'] =='upload':
					cardbody +=upload(comp,card['itype'],label_cr)
				
				if comp['wt'] =='dpop':
					cardbody +=dynamic_popup(comp,card['itype'],label_cr)

				if comp['wt'] == None:
					raise Exception("{"+comp['tt']+"} Widget Type Not Found")

			except Exception as ed:
				print ed
				raise Exception("{"+comp['tt']+"} Field Configuration Error.Please Check.")


	else:
		cardbody=""""""

	if card['children']:
		children_sorted = sorted(card['children'],key = itemgetter('do'))
		for childrens in children_sorted:
			childrenhtml +=children(childrens,fileName,ptitle,label_cr)
	else:
		childrenhtml=""""""

	if vtype == 'carousel':
		cardhtml=cardstart+cardbody+cardend
	else:
		cardhtml=cardstart+cardbody+childrenhtml+cardend

	return cardhtml


def lists(lists,vtype,fileName,ptitle,label_cr):
	listbody=""
	childrenhtml=""
	liststart ="""<ion-list class="card_list_padding">"""
	listend="""</ion-list>"""

	if len(lists['comp_meta'])>0:
		lists_sorted = sorted(lists['comp_meta'],key = itemgetter('do'))
		for comp in lists_sorted:
			try:
				if comp['wt'] == 'text':
					listbody += text(comp,lists['itype'],label_cr)

				if comp['wt'] =='email':
					listbody += email(comp,lists['itype'],label_cr)

				if comp['wt'] =='password':
					listbody +=	password(comp,lists['itype'],label_cr)

				if comp['wt'] =='textarea':
					listbody +=textarea(comp,lists['itype'],label_cr)

				if comp['wt'] == 'select':
					listbody +=	select(comp,lists['itype'],label_cr)

				if comp['wt'] == 'button':
					listbody +=button(comp,lists['itype'])

				if comp['wt'] =='date':
					listbody +=date(comp,lists['itype'],label_cr)

				if comp['wt'] =='time':
					listbody +=time(comp,lists['itype'],label_cr)

				if comp['wt'] =='number':
					listbody +=number(comp,lists['itype'],label_cr)

				if comp['wt'] =='radio':
					listbody +=radiobox(comp,lists['itype'],label_cr)

				if comp['wt'] =='check':
					listbody +=checkbox(comp,lists['itype'],label_cr)

				if comp['wt'] =='scan':
					listbody +=scan(comp,lists['itype'],label_cr)

				if comp['wt'] =='stot':
					listbody +=stot(comp,lists['itype'],label_cr)

				if comp['wt'] =='upload':
					listbody +=upload(comp,lists['itype'],label_cr)

				if comp['wt'] =='dpop':
					listbody +=dynamic_popup(comp,lists['itype'],label_cr)

				if comp['wt'] == None:
					raise Exception("{"+comp['tt']+"} Widget Type Not Found")

			except Exception as ed:
				print ed
				raise Exception("{"+comp['tt']+"} Field Configuration Error.Please Check.")


	else:
		listbody=""""""

	if lists['children']:
		children_sorted = sorted(lists['children'],key = itemgetter('do'))
		for childrens in children_sorted:
			childrenhtml +=children(childrens,fileName,ptitle,label_cr)
	else:
		childrenhtml=""""""

	if vtype =='carousel':
		listhtml=liststart+listbody+listend
	else:
		listhtml=liststart+listbody+childrenhtml+listend

	return listhtml


def grid(grid,vtype,fileName,ptitle,label_cr):
	gridstart =""
	gridheader =""
	tablestart =""
	tableend =""
	headerbody =""
	tbodystart =""
	gridend =""
	childrenhtml =""
	modelStart =""
	modelEnd =""
	modelHtml =""
	hide =""
	table=""
	gridstart = """<div class="container"><ion-row><h3 style="padding:1rem;">"""+grid['cap'].capitalize()+"""</h3></ion-row><ion-row>
	                   <ion-col>
						   <button ion-button small outline color="secondary" (click)="presentModal(\'"""+grid['idt']+"""\')"><ion-icon name="add"></ion-icon>Add
						   </button>
					   </ion-col>
					   <ion-col>
						   <button ion-button small outline color="secondary" (click)="editModal(\'"""+grid['idt']+"""\')" > <ion-icon name="create"></ion-icon>Edit
						   </button>
					   </ion-col>
					   <ion-col>
						   <button ion-button small outline color="secondary" (click)="togglecolumn(\'"""+grid['idt']+"""\')"><ion-icon name="grid"></ion-icon>Toggle
						   </button>
					   </ion-col>
				   </ion-row>
				 <ion-list class="scroll">"""
	gridend ="""</table></div></ion-list></div>"""
	if len(grid['comp_meta'])>0:
		grid_sorted = sorted(grid['comp_meta'],key = itemgetter('do'))
		tablestart ="""<div *ngIf="!viewMode"><table class="table table-striped table-sm" id ="""+grid['idt']+""" name="""+grid['idt']+""" data-db="""+grid['db']+"""><thead><tr>"""
		ed_tableid = grid['idt']+"_ET"
		ed_tablestart ="""</table></div><div *ngIf="viewMode"><table class="table table-striped table-sm" id ="""+ed_tableid+""" name="""+ed_tableid+""" data-db="""+grid['db']+"""><thead><tr>"""
		for comp in grid_sorted:
			try:
				if comp['ih'] == 'True':
					hide = "hidden"
					dhide = "true"
				else:
					hide= ""
					dhide = "false"

				headerbody+="""<th """+hide+""" data-hidden="""+dhide+""" id="""+comp['idt']+"_"+grid['db']+""" name="""+comp['idt']+"_"+grid['db']+""" data-elementId="""+comp['idt']+""" data-type="""+comp['wt']+""" >"""+comp['cap']+"""</th>"""

			except Exception as e:
				raise Exception("{"+comp['tt']+"} Filed Configuration Error.Please Check.")

		tableend = """</thead><tbody></tbody>"""

		table = tablestart+headerbody+tableend+ed_tablestart+headerbody+tableend


		listhtml = lists(grid,'carousel',fileName,ptitle,label_cr)
		modelStart = """<ion-header><ion-toolbar color="primary"><ion-row><ion-col><ion-title style="margin:10px 0 0 0">"""+grid['cap']+"""</ion-title></ion-col><ion-col><button ion-button small clear color="secondary" (click)="dismiss()">cancel</button><button ion-button small clear color="secondary" (click)="submit()">submit</button></ion-col></ion-row></ion-toolbar></ion-header><ion-content><form id="modelForm" name="modelForm">"""
		modelEnd = """</form></ion-content>"""
		modelHtml = modelStart+listhtml+modelEnd
		filePath = settings.MEDIA_ROOT
		if not os.path.exists(filePath+"static/ionicmeta/"+ptitle+"/"+fileName+"modal"):
			os.makedirs(filePath+"static/ionicmeta/"+ptitle+"/"+fileName+"modal")

		Html_file= open(filePath+"static/ionicmeta/"+ptitle+"/"+fileName+"modal/"+fileName+"modal.html","w")
		Html_file.write(modelHtml)
		Html_file.close()


	#gridhtml = gridstart+gridheader+gridbody+gridend
	if grid['children']:
		children_sorted = sorted(grid['children'],key = itemgetter('do'))
		for childrens in children_sorted:
			childrenhtml +=children(childrens,fileName,ptitle,label_cr)
	else:
		childrenhtml=""""""

	if vtype =='carousel':
		gridhtml = gridstart+table+gridend
	else:
		gridhtml = gridstart+table+gridend+childrenhtml

	return gridhtml

def modeltsfile(fileName,ptitle):
	filePath = settings.MEDIA_ROOT
	with open(filePath+"static/ionicsrc/modal/modal.ts") as f:
		with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".ts", "w") as f1:
			for line in f:
				f1.write(line)

	with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".ts", "r") as file :
		filedata = file.read()

	# Replace the target string
	filedata = filedata.replace('page-modal', 'page-'+fileName)
	filedata = filedata.replace('modal.html', fileName+'.html')
	filedata = filedata.replace('ModalPage', fileName.capitalize()+'Page')
	# Write the file out again
	with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".ts", "w") as file:
		file.write(filedata)

	appincludeTs(fileName,ptitle)
	scssPage = modelscssFile(fileName,ptitle)


def modelscssFile(fileName,ptitle):
	filePath = settings.MEDIA_ROOT
	with open(filePath+"static/ionicsrc/modal/modal.scss") as f:
		with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".scss", "w") as f1:
			for line in f:
				f1.write(line)

	with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".scss", "r") as file :
		filedata = file.read()

	# Replace the target string
	filedata = filedata.replace('page-modal', 'page-'+fileName)
	# Write the file out again
	with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".scss", "w") as file:
		file.write(filedata)

	return filedata


def gbody(grid_sorted):
	bodystart=""
	bodyend=""
	body=""
	bodystart="""<ion-row *ngFor="let row of rows">"""
	for grid in grid_sorted:
		if grid['wt'] == 'date':
			body+= griddate(grid)

		elif grid['wt'] == 'text':
			body+= gridtext(grid)


		elif grid['wt'] == 'select':
			body += gridselect(grid)


	bodyend="""</ion-row>"""
	gridbody = bodystart+body+bodyend
	return gridbody

def gridtext(gtext):
	readonly =False
	hide=""
 	if gtext['sql'] == None:
 		sql =""
 	else:
 		sql = gtext['sql']

 	if gtext['exp'] == None:
 		exp = ""
 	else:
 		exp = gtext['exp']

 	if gtext['vep']	== None:
 		vep =""
 	else:
 		vep	=gtext['vep']

 	if gtext['ih'] == 'True':
 		hide = "hidden"
 	else:
 		hide=""

	gtexthtml="""<ion-col><ion-item """+hide+"""><ion-input placeholder=\""""+gtext['cap']+"""\" data-readonly=\""""+gtext['iro']+"""\" data-required=\""""+gtext['ire']+"""\" data-allowduplicate=\""""+gtext['ad']+"""\" data-hidden=\""""+gtext['ih']+"""\" data-sql=\'"""+sql+"""\' data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" data-id=\""""+gtext['idt']+"""\" readonly=\""""+gtext['iro']+"""\" """+hide+"""></ion-input></ion-item></ion-col>"""
	return gtexthtml

def griddate(gdate):
	readonly =False
	hide=""
 	if gdate['sql'] == None:
 		sql =""
 	else:
 		sql = gdate['sql']

 	if gdate['exp'] == None:
 		exp = ""
 	else:
 		exp = gdate['exp']

 	if gdate['vep']	== None:
 		vep =""
 	else:
 		vep	=gdate['vep']

 	if gdate['ih'] == 'True':
 		hide = "hidden"
 	else:
 		hide=""

 	griddate ="""<ion-col><ion-item """+hide+"""><ion-datetime displayFormat="MM/DD/YYYY" data-readonly=\""""+gdate['iro']+"""\" data-required=\""""+gdate['ire']+"""\" data-allowduplicate=\""""+gdate['ad']+"""\" data-hidden=\""""+gdate['ih']+"""\" data-sql=\'"""+sql+"""\' data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" data-id=\""""+gdate['idt']+"""\" readonly=\""""+gdate['iro']+"""\" """+hide+"""></ion-datetime></ion-item></ion-col>"""
 	return griddate


def gridselect(gselect):
	readonly =False
	hide=""
 	if gselect['sql'] == None:
 		sql =""
 	else:
 		sql = gselect['sql']

 	if gselect['exp'] == None:
 		exp = ""
 	else:
 		exp = gselect['exp']

 	if gselect['vep']	== None:
 		vep =""
 	else:
 		vep	=gselect['vep']

 	if gselect['ih'] == 'True':
 		hide = "hidden"
 	else:
 		hide=""

 	gridselect = """<ion-col><ion-item """+hide+"""><ion-label>"""+gselect['cap']+"""</ion-label><ion-select data-readonly=\""""+gselect['iro']+"""\" data-required=\""""+gselect['ire']+"""\" data-allowduplicate=\""""+gselect['ad']+"""\" data-hidden=\""""+gselect['ih']+"""\" data-sql=\'"""+sql+"""\' data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" data-id=\""""+gselect['idt']+"""\" readonly=\""""+gselect['iro']+"""\" """+hide+"""></ion-select></ion-item></ion-col>"""
 	return gridselect

def text(text,inputtype,label_cr):
	texthtml =""""""
 	readonly =False
	hide=""

 	if text['sql'] == None or text['sql'] == "":
		sqlDict = {}
		sqlDict['Sql'] = ""
		sqlDict['sqlDbType'] = ""
		sqlDict['key'] = ""
		sqlDict['value'] = ""

 	else:
 		sql = text['sql']
		sqlDict =  json.loads(sql)

	if text['exp'] == None:
 		exp = ""
 	else:
 		exp = text['exp']

 	if text['vep']	== None:
 		vep =""
 	else:
 		vep	=text['vep']

 	if text['ih'] == 'True':
 		hide = "hidden"
 	else:
 		hide= ""

	if text['tid'] != None:
		tx_view_id = text['tid']
		tx_view_title = Transactionview.objects.get(pk=tx_view_id)
		project_id = tx_view_title.projectid_id

	else:
		tx_view_id = ""

	if text['do'] == None:
 		do = ""
 	else:
 		do = text['do']


 	if 	text['iro'] == 'True':
 		disable ="disabled"
 	else:
 		 disable =""

 	if inputtype == 'placeholder':
 		texthtml = """<ion-item """+hide+""" name=\""""+text['idt']+"""item\" ><ion-input type=\""""+text['wt']+"""\" placeholder=\""""+text['cap']+"""\" class="input_border" data-id=\""""+text['idt']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+text['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" data-readonly=\""""+text['iro']+"""\" data-required=\""""+text['ire']+"""\" data-allowduplicate=\""""+text['ad']+"""\" data-hidden=\""""+text['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+text['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" data-displayorder=\""""+str(do)+"""\" id=\""""+text['idt']+"""\" name=\""""+text['idt']+"""\" readonly=\""""+text['iro']+"""\" data-modeOfEntry=\""""+text['moe']+"""\" data-suggestive=\""""+text['sug']+"""\" """+hide+"""  data-referjson=\'"""+text['cjson']+"""\' [(ngModel)]=\"preset_value."""+text['idt']+"""\"  (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)" required></ion-input></ion-item>"""

	elif inputtype =='boxed':
 		texthtml = """<ion-item """+hide+""" name=\""""+text['idt']+"""item\"><ion-label color=\""""+label_cr+"""\" class="content_padding" stacked>"""+text['cap']+"""</ion-label><ion-input type=\""""+text['wt']+"""\" placeholder=\""""+text['cap']+"""\" class="input_for_boxed" data-id=\""""+text['idt']+"""\" placeholder=\""""+text['cap']+"""\" data-readonly=\""""+text['iro']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+text['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" data-required=\""""+text['ire']+"""\" data-allowduplicate=\""""+text['ad']+"""\" data-hidden=\""""+text['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+text['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" id=\""""+text['idt']+"""\" name=\""""+text['idt']+"""\" readonly=\""""+text['iro']+"""\" data-modeOfEntry=\""""+text['moe']+"""\" data-displayorder=\""""+str(do)+"""\" data-suggestive=\""""+text['sug']+"""\" data-referjson=\'"""+text['cjson']+"""\' """+hide+""" """+disable+""" [(ngModel)]=\"preset_value."""+text['idt']+"""\" (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)"></ion-input></ion-item>"""
 	else:
		if inputtype =='floating':
			placeholder = ""
		else:
			placeholder = """placeholder=\""""+text['cap']+"""\""""
 		texthtml = """<ion-item """+hide+""" name=\""""+text['idt']+"""item\"><ion-label color=\""""+label_cr+"""\" """+inputtype+""" """+hide+""">"""+text['cap']+"""</ion-label><ion-input type=\""""+text['wt']+"""\" """+placeholder+""" class="input_border" data-label=\""""+text['cap']+"""\" data-id=\""""+text['idt']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+text['idt']+"""\" """+disable+""" data-eformid=\""""+str(tx_view_title)+"""\" data-readonly=\""""+text['iro']+"""\" data-required=\""""+text['ire']+"""\" data-allowduplicate=\""""+text['ad']+"""\" data-hidden=\""""+text['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+text['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" data-displayorder=\""""+str(do)+"""\" id=\""""+text['idt']+"""\" name=\""""+text['idt']+"""\" readonly=\""""+text['iro']+"""\" data-modeOfEntry=\""""+text['moe']+"""\" data-suggestive=\""""+text['sug']+"""\" """+hide+""" data-referjson=\'"""+text['cjson']+"""\' [(ngModel)]=\"preset_value."""+text['idt']+"""\" (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)" required></ion-input></ion-item>"""

	return texthtml


def email(email,inputtype,label_cr):
	emailhtml =""""""
	readonly =False
 	if email['sql'] == None or email['sql'] == "":
		sqlDict = {}
		sqlDict['Sql'] = ""
		sqlDict['sqlDbType'] = ""
		sqlDict['key'] = ""
		sqlDict['value'] = ""

 	else:
 		sql = email['sql']
		sqlDict =  json.loads(sql)

 	if email['exp'] == None:
 		exp = ""
 	else:
 		exp = email['exp']

 	if email['vep']	== None:
 		vep =""
 	else:
 		vep	=email['vep']

 	if email['ih'] == 'True':
 		hide = "hidden"
 	else:
 		hide=""

	if email['tid'] != None:
		tx_view_id = email['tid']
		tx_view_title = Transactionview.objects.get(pk=tx_view_id)
		project_id = tx_view_title.projectid_id

	else:
		tx_view_id = ""

	if email['iro'] == 'True':
 		disable ="disabled"
 	else:
 		 disable =""

	if email['do'] == None:
 		do = ""
 	else:
 		do = email['do']


 	if inputtype == 'placeholder':
 		emailhtml = """<ion-item """+hide+""" name=\""""+email['idt']+"""item\"><ion-input type=\""""+email['wt']+"""\" placeholder=\""""+email['cap']+"""\" class="input_border"  data-readonly=\""""+email['iro']+"""\" data-required=\""""+email['ire']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+email['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" data-id=\""""+email['idt']+"""\" data-allowduplicate=\""""+email['ad']+"""\" data-hidden=\""""+email['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+email['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" data-displayorder=\""""+str(do)+"""\" id=\""""+email['idt']+"""\" name=\""""+email['idt']+"""\" readonly=\""""+email['iro']+"""\" data-modeOfEntry=\""""+email['moe']+"""\" data-suggestive=\""""+email['sug']+"""\" data-referjson=\'"""+email['cjson']+"""\' """+hide+"""  """+disable+""" [(ngModel)]=\"preset_value."""+email['idt']+"""\" (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)"></ion-input></ion-item>"""

	elif inputtype =='boxed':
		emailhtml = """<ion-item """+hide+""" name=\""""+email['idt']+"""item\"><ion-label color=\""""+label_cr+"""\" class="content_padding" stacked>"""+email['cap']+"""</ion-label><ion-input type=\""""+email['wt']+"""\" placeholder=\""""+email['cap']+"""\" class="input_for_boxed" data-label=\""""+email['cap']+"""\" data-id=\""""+email['idt']+"""\" data-readonly=\""""+email['iro']+"""\" data-required=\""""+email['ire']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+email['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" data-allowduplicate=\""""+email['ad']+"""\" data-hidden=\""""+email['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+email['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" id=\""""+email['idt']+"""\" name=\""""+email['idt']+"""\" readonly=\""""+email['iro']+"""\" data-modeOfEntry=\""""+email['moe']+"""\" data-suggestive=\""""+email['sug']+"""\" data-referjson=\'"""+email['cjson']+"""\' data-displayorder=\""""+str(do)+"""\" """+hide+""" [(ngModel)]=\"preset_value."""+email['idt']+"""\" (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)"></ion-input></ion-item>"""

 	else:
		if inputtype =='floating':
			placeholder = ""
		else:
			placeholder = """placeholder=\""""+email['cap']+"""\""""
 		emailhtml = """<ion-item """+hide+""" name=\""""+email['idt']+"""item\"><ion-label color=\""""+label_cr+"""\" """+inputtype+""">"""+email['cap']+"""</ion-label><ion-input type=\""""+email['wt']+"""\" class="input_border" data-label=\""""+email['cap']+"""\" data-id=\""""+email['idt']+"""\" """+placeholder+""" data-readonly=\""""+email['iro']+"""\" """+disable+""" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+email['idt']+"""\" """+disable+""" data-eformid=\""""+str(tx_view_title)+"""\" data-required=\""""+email['ire']+"""\" data-allowduplicate=\""""+email['ad']+"""\" data-hidden=\""""+email['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+email['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" id=\""""+email['idt']+"""\" name=\""""+email['idt']+"""\" readonly=\""""+email['iro']+"""\" data-modeOfEntry=\""""+email['moe']+"""\" data-suggestive=\""""+email['sug']+"""\" data-referjson=\'"""+email['cjson']+"""\' data-displayorder=\""""+str(do)+"""\" """+hide+""" [(ngModel)]=\"preset_value."""+email['idt']+"""\" (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)"></ion-input></ion-item>"""

	return emailhtml


def password(password,inputtype,label_cr):
	passwordhtml =""""""
	readonly =False
 	if password['sql'] == None or password['sql'] == "":
		sqlDict = {}
		sqlDict['Sql'] = ""
		sqlDict['sqlDbType'] = ""
		sqlDict['key'] = ""
		sqlDict['value'] = ""

 	else:
 		sql = password['sql']
		sqlDict =  json.loads(sql)

 	if password['exp'] == None:
 		exp = ""
 	else:
 		exp = password['exp']

 	if password['vep']	== None:
 		vep =""
 	else:
 		vep	=password['vep']

 	if password['ih'] == 'True':
 		hide = "hidden"
 	else:
 		hide=""

 	if password['iro'] == 'True':
 		disable ="disabled"
 	else:
 		 disable =""

	if password['do'] == None:
 		do = ""
 	else:
 		do = password['do']


 	if inputtype == 'placeholder':
 		passwordhtml = """<ion-item """+hide+""" name=\""""+password['idt']+"""item\"><ion-input type=\""""+password['wt']+"""\" placeholder=\""""+password['cap']+"""\" class="input_border" data-readonly=\""""+password['iro']+"""\" data-required=\""""+password['ire']+"""\" data-id=\""""+password['idt']+"""\" data-name=\""""+password['idt']+"""\" name=\""""+password['idt']+"""\" data-allowduplicate=\""""+password['ad']+"""\" data-hidden=\""""+password['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+password['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" id=\""""+password['idt']+"""\" readonly=\""""+password['iro']+"""\" data-modeOfEntry=\""""+password['moe']+"""\" data-suggestive=\""""+password['sug']+"""\" data-referjson=\'"""+password['cjson']+"""\' data-displayorder=\""""+str(do)+"""\"  """+hide+""" """+disable+""" [(ngModel)]=\"preset_value."""+password['idt']+"""\"  (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)"></ion-input></ion-item>"""

	elif inputtype =='boxed':
		passwordhtml = """<ion-item """+hide+""" name=\""""+password['idt']+"""item\"><ion-label color=\""""+label_cr+"""\" class="content_padding" stacked>"""+password['cap']+"""</ion-label><ion-input type=\""""+password['wt']+"""\" placeholder=\""""+password['cap']+"""\" class="input_for_boxed"  data-label=\""""+password['cap']+"""\" data-id=\""""+password['idt']+"""\" data-name=\""""+password['idt']+"""\" name=\""""+password['idt']+"""\" placeholder=\""""+password['cap']+"""\" data-readonly=\""""+password['iro']+"""\" data-required=\""""+password['ire']+"""\" data-allowduplicate=\""""+password['ad']+"""\" data-hidden=\""""+password['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+password['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" id=\""""+password['idt']+"""\" readonly=\""""+password['iro']+"""\" data-modeOfEntry=\""""+password['moe']+"""\" data-suggestive=\""""+password['sug']+"""\" data-referjson=\'"""+password['cjson']+"""\' data-displayorder=\""""+str(do)+"""\" """+hide+""" """+disable+""" [(ngModel)]=\"preset_value."""+password['idt']+"""\" (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)"></ion-input></ion-item>"""
 	else:
		if inputtype =='floating':
			placeholder = ""
		else:
			placeholder = """placeholder=\""""+password['cap']+"""\""""

 		passwordhtml = """<ion-item """+hide+""" name=\""""+password['idt']+"""item\"><ion-label color=\""""+label_cr+"""\" """+inputtype+""">"""+password['cap']+"""</ion-label><ion-input type=\""""+password['wt']+"""\" class="input_border"  data-label=\""""+password['cap']+"""\" data-id=\""""+password['idt']+"""\" data-name=\""""+password['idt']+"""\" name=\""""+password['idt']+"""\" """+placeholder+""" data-readonly=\""""+password['iro']+"""\" data-required=\""""+password['ire']+"""\" data-allowduplicate=\""""+password['ad']+"""\" data-hidden=\""""+password['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+password['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" id=\""""+password['idt']+"""\" readonly=\""""+password['iro']+"""\" data-modeOfEntry=\""""+password['moe']+"""\" data-suggestive=\""""+password['sug']+"""\" data-referjson=\'"""+password['cjson']+"""\' data-displayorder=\""""+str(do)+"""\" """+hide+""" """+disable+""" [(ngModel)]=\"preset_value."""+password['idt']+"""\" (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)"></ion-input></ion-item>"""

	return passwordhtml

def textarea(txarea,inputtype,label_cr):
	textareahtml =""""""
	readonly =False
 	if txarea['sql'] == None or txarea['sql'] == "":
		sqlDict = {}
		sqlDict['Sql'] = ""
		sqlDict['sqlDbType'] = ""
		sqlDict['key'] = ""
		sqlDict['value'] = ""

 	else:
 		sql = txarea['sql']
		sqlDict =  json.loads(sql)

 	if txarea['exp'] == None:
 		exp = ""
 	else:
 		exp = txarea['exp']

 	if txarea['vep']	== None:
 		vep =""
 	else:
 		vep	=txarea['vep']

 	if txarea['ih'] == 'True':
 		hide = "hidden"
 	else:
 		hide=""

	if txarea['tid'] != None:
		tx_view_id = txarea['tid']
		tx_view_title = Transactionview.objects.get(pk=tx_view_id)
		project_id = tx_view_title.projectid_id

	else:
		tx_view_id = ""

	if txarea['iro'] == 'True':
 		disable ="disabled"
 	else:
 		 disable =""

	if txarea['do'] == None:
 		do = ""
 	else:
 		do = txarea['do']


 	if inputtype == 'placeholder':
 		textareahtml ="""<ion-item """+hide+""" name=\""""+txarea['idt']+"""item\" ><ion-textarea placeholder=\""""+txarea['cap']+"""\" class="input_border textarea_placeholder" data-id=\""""+txarea['idt']+"""\" data-readonly=\""""+txarea['iro']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+txarea['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" data-required=\""""+txarea['ire']+"""\" data-allowduplicate=\""""+txarea['ad']+"""\" data-hidden=\""""+txarea['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+txarea['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" id=\""""+txarea['idt']+"""\" readonly=\""""+txarea['iro']+"""\" data-modeOfEntry=\""""+txarea['moe']+"""\" data-suggestive=\""""+txarea['sug']+"""\" data-referjson=\'"""+txarea['cjson']+"""\'  name=\""""+txarea['idt']+"""\" data-displayorder=\""""+str(do)+"""\" """+hide+"""  """+disable+""" [(ngModel)]=\"preset_value."""+txarea['idt']+"""\" (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)"></ion-textarea></ion-item>"""

 	elif inputtype == 'floating':
 		textareahtml = """<ion-item """+hide+""" name=\""""+txarea['idt']+"""item\"><ion-label color=\""""+label_cr+"""\" """+inputtype+""">"""+txarea['cap']+"""</ion-label><ion-textarea class="input_border" data-readonly=\""""+txarea['iro']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+txarea['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" data-label=\""""+txarea['cap']+"""\" data-id=\""""+txarea['idt']+"""\" data-required=\""""+txarea['ire']+"""\" data-allowduplicate=\""""+txarea['ad']+"""\" data-hidden=\""""+txarea['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+txarea['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" id=\""""+txarea['idt']+"""\" readonly=\""""+txarea['iro']+"""\" data-modeOfEntry=\""""+txarea['moe']+"""\" data-suggestive=\""""+txarea['sug']+"""\" name=\""""+txarea['idt']+"""\" data-referjson=\'"""+txarea['cjson']+"""\' data-displayorder=\""""+str(do)+"""\" """+hide+""" """+disable+""" [(ngModel)]=\"preset_value."""+txarea['idt']+"""\" (onFocus)="onFocus($event)" (ionBlur)="checkBlur($event)"></ion-textarea></ion-item>"""

	elif inputtype == 'boxed':
 		textareahtml = """<ion-item """+hide+""" name=\""""+txarea['idt']+"""item\"><ion-label color=\""""+label_cr+"""\" class="content_padding" stacked>"""+txarea['cap']+"""</ion-label><ion-textarea placeholder=\""""+txarea['cap']+"""\" class="input_for_boxed" data-readonly=\""""+txarea['iro']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+txarea['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" data-label=\""""+txarea['cap']+"""\" data-id=\""""+txarea['idt']+"""\" data-required=\""""+txarea['ire']+"""\" data-allowduplicate=\""""+txarea['ad']+"""\" data-hidden=\""""+txarea['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+txarea['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" id=\""""+txarea['idt']+"""\" readonly=\""""+txarea['iro']+"""\" data-modeOfEntry=\""""+txarea['moe']+"""\" data-suggestive=\""""+txarea['sug']+"""\" name=\""""+txarea['idt']+"""\" data-referjson=\'"""+txarea['cjson']+"""\' data-displayorder=\""""+str(do)+"""\" """+hide+""" """+disable+""" [(ngModel)]=\"preset_value."""+txarea['idt']+"""\" (onFocus)="onFocus($event)" (ionBlur)="checkBlur($event)"></ion-textarea></ion-item>"""

 	else:
 		textareahtml = """<ion-item """+hide+""" name=\""""+txarea['idt']+"""item\"><ion-label color=\""""+label_cr+"""\" """+inputtype+""">"""+txarea['cap']+"""</ion-label><ion-textarea placeholder=\""""+txarea['cap']+"""\" class="input_border" data-readonly=\""""+txarea['iro']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+txarea['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" data-label=\""""+txarea['cap']+"""\" data-id=\""""+txarea['idt']+"""\" data-required=\""""+txarea['ire']+"""\" data-allowduplicate=\""""+txarea['ad']+"""\" data-hidden=\""""+txarea['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+txarea['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" id=\""""+txarea['idt']+"""\" readonly=\""""+txarea['iro']+"""\" data-modeOfEntry=\""""+txarea['moe']+"""\" name=\""""+txarea['idt']+"""\" data-suggestive=\""""+txarea['sug']+"""\" data-referjson=\'"""+txarea['cjson']+"""\' data-displayorder=\""""+str(do)+"""\" """+hide+""" """+disable+""" [(ngModel)]=\"preset_value."""+txarea['idt']+"""\" (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)"></ion-textarea></ion-item>"""

 	return textareahtml

def button(button,inputtype):
	readonly =False
 	if button['sql'] == None or button['sql'] == "":
		sqlDict = {}
		sqlDict['Sql'] = ""
		sqlDict['sqlDbType'] = ""
		sqlDict['key'] = ""
		sqlDict['value'] = ""
	
 	else:
 		sql = button['sql']
		sqlDict =  json.loads(sql)

 	if button['exp'] == None:
 		exp = ""
 	else:
 		exp = button['exp']

 	if button['vep']	== None:
 		vep =""
 	else:
 		vep	=button['vep']

 	if button['ih'] == 'True':
 		hide = "hidden"
 	else:
 		hide=""


 	buttonhtml = """<ion-item """+hide+"""><button ion-button block (click)="buttonClick($event)" data-readonly=\""""+button['iro']+"""\" data-label=\""""+button['cap']+"""\" data-id=\""""+button['idt']+"""\" data-required=\""""+button['ire']+"""\" data-allowduplicate=\""""+button['ad']+"""\" data-hidden=\""""+button['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+button['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" data-modeOfEntry=\""""+button['moe']+"""\" data-suggestive=\""""+button['sug']+"""\" id=\""""+button['idt']+"""\" data-referjson=\'"""+button['cjson']+"""\'>"""+button['cap']+"""</button></ion-item>"""
 	return buttonhtml

def date(date,inputtype,label_cr):
	datehtml=""""""
 	readonly =False
 	if date['sql'] == None or date['sql'] == "":
		sqlDict = {}
		sqlDict['Sql'] = ""
		sqlDict['sqlDbType'] = ""
		sqlDict['key'] = ""
		sqlDict['value'] = ""

 	else:
 		sql = date['sql']
		sqlDict =  json.loads(sql)


 	if date['exp'] == None:
 		exp = ""
 	else:
 		exp = date['exp']

 	if date['vep']	== None:
 		vep =""
 	else:
 		vep	=date['vep']

 	if date['ih'] == 'True':
 		hide = "hidden"
 	else:
 		hide=""

 	if 	date['iro'] == 'True':
 		disable ="disabled"
	else:
 		 disable =""

	if date['tid'] != None:
		tx_view_id = date['tid']
		tx_view_title = Transactionview.objects.get(pk=tx_view_id)
		project_id = tx_view_title.projectid_id

	else:
		tx_view_id = ""

	if date['do'] == None:
 		do = ""
 	else:
 		do = date['do']


 	if inputtype == 'placeholder':
 		datehtml="""<ion-item """+hide+""" name=\""""+date['idt']+"""item\"><ion-datetime displayFormat="DD/MM/YYYY" placeholder=\""""+date['cap']+"""\" class="input_border date_placeholer" data-id=\""""+date['idt']+"""\" data-readonly=\""""+date['iro']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+date['idt']+"""\" date-eformid=\""""+str(tx_view_title)+"""\" data-required=\""""+date['ire']+"""\" data-allowduplicate=\""""+date['ad']+"""\" data-hidden=\""""+date['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+date['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" id=\""""+date['idt']+"""\" name=\""""+date['idt']+"""\" readonly=\""""+date['iro']+"""\" data-modeOfEntry=\""""+date['moe']+"""\" data-displayorder=\""""+str(do)+"""\" data-suggestive=\""""+date['sug']+"""\" data-referjson=\'"""+date['cjson']+"""\' """+hide+""" """+disable+""" data-format="date" [(ngModel)]=\"preset_value."""+date['idt']+"""\" (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)"></ion-datetime></ion-item>"""

 	elif inputtype =='floating':
 		datehtml="""<ion-item """+hide+""" name=\""""+date['idt']+"""item\"><ion-label color=\""""+label_cr+"""\" """+inputtype+""">"""+date['cap']+"""</ion-label><ion-datetime displayFormat="DD/MM/YYYY" class="input_border" data-readonly=\""""+date['iro']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+date['idt']+"""\" date-eformid=\""""+str(tx_view_title)+"""\" data-label=\""""+date['cap']+"""\" data-id=\""""+date['idt']+"""\" data-required=\""""+date['ire']+"""\" data-allowduplicate=\""""+date['ad']+"""\" data-hidden=\""""+date['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+date['isdep']+"""\" data-expression=\""""+exp+"""\" data-displayorder=\""""+str(do)+"""\" data-validateexp=\""""+vep+"""\" id=\""""+date['idt']+"""\" name=\""""+date['idt']+"""\" readonly=\""""+date['iro']+"""\" data-modeOfEntry=\""""+date['moe']+"""\" data-suggestive=\""""+date['sug']+"""\" data-referjson=\'"""+date['cjson']+"""\' """+hide+""" """+disable+""" data-format="date" [(ngModel)]=\"preset_value."""+date['idt']+"""\" (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)"></ion-datetime></ion-item>"""

	elif inputtype =='boxed':
 		datehtml="""<ion-item """+hide+""" name=\""""+date['idt']+"""item\"><ion-label color=\""""+label_cr+"""\" class="content_padding" stacked>"""+date['cap']+"""</ion-label><ion-datetime displayFormat="DD/MM/YYYY" class="input_for_boxed" placeholder=\""""+date['cap']+"""\" data-readonly=\""""+date['iro']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+date['idt']+"""\" date-eformid=\""""+str(tx_view_title)+"""\" data-label=\""""+date['cap']+"""\" data-id=\""""+date['idt']+"""\" data-required=\""""+date['ire']+"""\" data-allowduplicate=\""""+date['ad']+"""\" data-hidden=\""""+date['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+date['isdep']+"""\" data-expression=\""""+exp+"""\" data-displayorder=\""""+str(do)+"""\" data-validateexp=\""""+vep+"""\" id=\""""+date['idt']+"""\" name=\""""+date['idt']+"""\" readonly=\""""+date['iro']+"""\" data-modeOfEntry=\""""+date['moe']+"""\" data-suggestive=\""""+date['sug']+"""\" data-referjson=\'"""+date['cjson']+"""\' """+hide+""" """+disable+""" data-format="date" [(ngModel)]=\"preset_value."""+date['idt']+"""\" (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)"></ion-datetime></ion-item>"""

 	else:
 		datehtml="""<ion-item """+hide+""" name=\""""+date['idt']+"""item\"><ion-label color=\""""+label_cr+"""\" """+inputtype+""">"""+date['cap']+"""</ion-label><ion-datetime displayFormat="DD/MM/YYYY" placeholder=\""""+date['cap']+"""\" class="input_border" data-readonly=\""""+date['iro']+"""\" data-label=\""""+date['cap']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+date['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" data-id=\""""+date['idt']+"""\" data-required=\""""+date['ire']+"""\" data-allowduplicate=\""""+date['ad']+"""\" data-hidden=\""""+date['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+date['isdep']+"""\" data-displayorder=\""""+str(do)+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" id=\""""+date['idt']+"""\" name=\""""+date['idt']+"""\" readonly=\""""+date['iro']+"""\" data-modeOfEntry=\""""+date['moe']+"""\" data-suggestive=\""""+date['sug']+"""\" data-referjson=\'"""+date['cjson']+"""\' """+hide+""" """+disable+""" data-format="date" [(ngModel)]=\"preset_value."""+date['idt']+"""\" (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)"></ion-datetime></ion-item>"""

	return datehtml


def number(num,inputtype,label_cr):
	texthtml =""""""
	readonly =False
 	if num['sql'] == None or num['sql'] == "":
		sqlDict = {}
		sqlDict['Sql'] = ""
		sqlDict['sqlDbType'] = ""
		sqlDict['key'] = ""
		sqlDict['value'] = ""

 	else:
 		sql = num['sql']
		sqlDict =  json.loads(sql)

 	if num['exp'] == None:
 		exp = ""
 	else:
 		exp = num['exp']

 	if num['vep']	== None:
 		vep =""
 	else:
 		vep	=num['vep']

 	if num['ih'] == 'True':
 		hide = "hidden"
 	else:
 		hide=""

	if num['tid'] != None:
		tx_view_id = num['tid']
		tx_view_title = Transactionview.objects.get(pk=tx_view_id)
		project_id = tx_view_title.projectid_id

	else:
		tx_view_id = ""

	if 	num['iro'] == 'True':
 		disable ="disabled"
 	else:
 		 disable =""

	if num['do'] == None:
 		do = ""
 	else:
 		do = num['do']


 	if inputtype == 'placeholder':
 		texthtml = """<ion-item """+hide+""" name=\""""+num['idt']+"""item\"><ion-input type=\""""+num['wt']+"""\" class="input_border" data-id=\""""+num['idt']+"""\" placeholder=\""""+num['cap']+"""\" data-readonly=\""""+num['iro']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+num['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" data-required=\""""+num['ire']+"""\" data-allowduplicate=\""""+num['ad']+"""\" data-hidden=\""""+num['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+num['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" id=\""""+num['idt']+"""\" name=\""""+num['idt']+"""\" readonly=\""""+num['iro']+"""\" data-modeOfEntry=\""""+num['moe']+"""\" data-displayorder=\""""+str(do)+"""\" data-suggestive=\""""+num['sug']+"""\" data-referjson=\'"""+num['cjson']+"""\' """+hide+""" """+disable+""" [(ngModel)]=\"preset_value."""+num['idt']+"""\" (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)" ></ion-input></ion-item>"""

	elif inputtype =='boxed':
		texthtml = """<ion-item """+hide+""" name=\""""+num['idt']+"""item\"><ion-label color=\""""+label_cr+"""\" class="content_padding" stacked>"""+num['cap']+"""</ion-label><ion-input type=\""""+num['wt']+"""\" class="input_for_boxed" data-id=\""""+num['idt']+"""\" placeholder=\""""+num['cap']+"""\" data-readonly=\""""+num['iro']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+num['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" data-required=\""""+num['ire']+"""\" data-allowduplicate=\""""+num['ad']+"""\" data-hidden=\""""+num['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+num['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" id=\""""+num['idt']+"""\" name=\""""+num['idt']+"""\" readonly=\""""+num['iro']+"""\" data-modeOfEntry=\""""+num['moe']+"""\" data-displayorder=\""""+str(do)+"""\" data-suggestive=\""""+num['sug']+"""\" data-referjson=\'"""+num['cjson']+"""\' """+hide+""" """+disable+""" [(ngModel)]=\"preset_value."""+num['idt']+"""\" (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)"></ion-input></ion-item>"""

 	else:
 		texthtml = """<ion-item """+hide+""" name=\""""+num['idt']+"""item\"><ion-label color=\""""+label_cr+"""\" """+inputtype+""">"""+num['cap']+"""</ion-label><ion-input type=\""""+num['wt']+"""\" placeholder=\""""+num['cap']+"""\"  data-id=\""""+num['idt']+"""\" placeholder=\""""+num['cap']+"""\" class="input_border" data-readonly=\""""+num['iro']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+num['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" data-required=\""""+num['ire']+"""\" data-allowduplicate=\""""+num['ad']+"""\" data-hidden=\""""+num['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+num['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" id=\""""+num['idt']+"""\" name=\""""+num['idt']+"""\" readonly=\""""+num['iro']+"""\" data-modeOfEntry=\""""+num['moe']+"""\" data-displayorder=\""""+str(do)+"""\" data-suggestive=\""""+num['sug']+"""\" data-referjson=\'"""+num['cjson']+"""\' """+hide+""" """+disable+""" [(ngModel)]=\"preset_value."""+num['idt']+"""\" (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)"></ion-input></ion-item>"""

	return texthtml

def time(time,inputtype,label_cr):
	timehtml = """"""
 	readonly = False

 	if time['sql'] == None or time['sql'] == "":
		sqlDict = {}
		sqlDict['Sql'] = ""
		sqlDict['sqlDbType'] = ""
		sqlDict['key'] = ""
		sqlDict['value'] = ""

 	else:
 		sql = time['sql']
		sqlDict =  json.loads(sql)

 	if time['exp'] == None:
 		exp = ""
 	else:
 		exp = time['exp']

 	if time['vep']	== None:
 		vep =""
 	else:
 		vep	=time['vep']

 	if time['ih'] == 'True':
 		hide = "hidden"
 	else:
 		hide=""

	if time['cjson']:
		timeJson = json.loads(time['cjson'])

	else:
		timeJson = ""

	if time['tid'] != None:
		tx_view_id = time['tid']
		tx_view_title = Transactionview.objects.get(pk=tx_view_id)
		project_id = tx_view_title.projectid_id
	else:
		tx_view_id = ""

	if time['do'] == None:
 		do = ""
 	else:
 		do = time['do']


	if time['iro'] == 'True':
 		disable ="disabled"
	else:
 		 disable =""

 	if inputtype == 'placeholder':
 		timehtml="""<ion-item """+hide+""" name=\""""+time['idt']+"""item\"><ion-datetime displayFormat="hh:mm a" class="input_border date_placeholer" data-id=\""""+time['idt']+"""\" placeholder=\""""+time['cap']+"""\" data-readonly=\""""+time['iro']+"""\" data-required=\""""+time['ire']+"""\" data-allowduplicate=\""""+time['ad']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+time['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" data-hidden=\""""+time['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+time['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" data-id=\""""+time['idt']+"""\" data-displayorder=\""""+str(do)+"""\" readonly=\""""+time['iro']+"""\" data-modeOfEntry=\""""+time['moe']+"""\" data-suggestive=\""""+time['sug']+"""\" """+hide+"""  id=\""""+time['idt']+"""\" name=\""""+time['idt']+"""\" data-referjson=\'"""+time['cjson']+"""\' data-wt=\""""+time['wt']+"""\" """+disable+""" data-format="time" [(ngModel)]=\"preset_value."""+time['idt']+"""\" (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)"></ion-datetime></ion-item>"""

 	elif inputtype =='floating':
 		timehtml="""<ion-item """+hide+""" name=\""""+time['idt']+"""item\"><ion-label color=\""""+label_cr+"""\" """+inputtype+""">"""+time['cap']+"""</ion-label><ion-datetime displayFormat="hh:mm a" class="input_border" data-label=\""""+time['cap']+"""\" data-id=\""""+time['idt']+"""\" data-readonly=\""""+time['iro']+"""\" data-required=\""""+time['ire']+"""\" data-allowduplicate=\""""+time['ad']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+time['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" data-hidden=\""""+time['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+time['isdep']+"""\" data-displayorder=\""""+str(do)+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" data-id=\""""+time['idt']+"""\" readonly=\""""+time['iro']+"""\" data-modeOfEntry=\""""+time['moe']+"""\" data-suggestive=\""""+time['sug']+"""\" data-referjson=\'"""+time['cjson']+"""\' data-wt=\""""+time['wt']+"""\" """+hide+"""  id=\""""+time['idt']+"""\" name=\""""+time['idt']+"""\" data-format="time"  [(ngModel)]=\"preset_value."""+time['idt']+"""\" (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)"></ion-datetime></ion-item>"""

	elif inputtype =='boxed':
 		timehtml="""<ion-item """+hide+""" name=\""""+time['idt']+"""item\"><ion-label color=\""""+label_cr+"""\" class="content_padding" stacked>"""+time['cap']+"""</ion-label><ion-datetime displayFormat="hh:mm a" placeholder=\""""+time['cap']+"""\" class="input_for_boxed" data-label=\""""+time['cap']+"""\" data-id=\""""+time['idt']+"""\" data-readonly=\""""+time['iro']+"""\" data-required=\""""+time['ire']+"""\" data-allowduplicate=\""""+time['ad']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+time['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" data-hidden=\""""+time['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+time['isdep']+"""\" data-displayorder=\""""+str(do)+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" data-id=\""""+time['idt']+"""\" readonly=\""""+time['iro']+"""\" data-modeOfEntry=\""""+time['moe']+"""\" data-suggestive=\""""+time['sug']+"""\" data-referjson=\'"""+time['cjson']+"""\' data-wt=\""""+time['wt']+"""\" """+hide+"""  id=\""""+time['idt']+"""\" name=\""""+time['idt']+"""\" data-format="time"  [(ngModel)]=\"preset_value."""+time['idt']+"""\" (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)"></ion-datetime></ion-item>"""

 	else:
 		timehtml="""<ion-item """+hide+""" name=\""""+time['idt']+"""item\"><ion-label color=\""""+label_cr+"""\" """+inputtype+""">"""+time['cap']+"""</ion-label><ion-datetime type="datetime-local" displayFormat="hh:mm a" class="input_border" data-label=\""""+time['cap']+"""\" data-id=\""""+time['idt']+"""\" placeholder=\""""+time['cap']+"""\" data-readonly=\""""+time['iro']+"""\" data-required=\""""+time['ire']+"""\" data-allowduplicate=\""""+time['ad']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+time['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" data-hidden=\""""+time['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+time['isdep']+"""\" data-displayorder=\""""+str(do)+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" data-id=\""""+time['idt']+"""\" readonly=\""""+time['iro']+"""\" data-referjson=\'"""+time['cjson']+"""\' data-wt=\""""+time['wt']+"""\" """+hide+""" id=\""""+time['idt']+"""\" name=\""""+time['idt']+"""\" data-format="time"  [(ngModel)]=\"preset_value."""+time['idt']+"""\" (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)"></ion-datetime></ion-item>"""

	return timehtml

def select(select,inputtype,label_cr):
	readonly =False
	selectlabel = ""
	selectoptions =""

	if select['sql'] == None:
		sqlDict = {}
		sqlDict['Sql'] = ""
		sqlDict['sqlDbType'] = ""
		sqlDict['key'] = ""
		sqlDict['value'] = ""

 	else:
 		sql = select['sql']
		sqlDict =  json.loads(sql)

 	if select['exp'] == None:
 		exp = ""
 	else:
 		exp = select['exp']

 	if select['vep']	== None:
 		vep =""
 	else:
 		vep	=select['vep']

 	if select['ih'] == 'True':
 		hide = "hidden"
 	else:
 		hide=""

 	if select['iro'] == 'True':
 		disable ="disabled"
 	else:
 		 disable =""

	if select['do'] == None:
 		do = ""
 	else:
 		do = select['do']

	if inputtype =='placeholder':
		selectlabel = """"""
		input_class='class="select_input_border"'

	elif inputtype =='boxed':
 		selectlabel = """<ion-label color=\""""+label_cr+"""\" class="content_padding" stacked>"""+select['cap']+"""</ion-label>"""
		input_class ='class="input_for_boxed"'

	else:
		selectlabel = """<ion-label color=\""""+label_cr+"""\" """+inputtype+""">"""+select['cap']+"""</ion-label> """
		input_class ='class="select_input_border"'

	if select['cjson']:

		if select['tid'] != None:
			tx_view_id = select['tid']
			tx_view_title = Transactionview.objects.get(pk=tx_view_id)
			project_id = tx_view_title.projectid_id

		else:
			tx_view_id = ""
			project_id = ""

		selectJson = json.loads(select['cjson'])
		try:
			enum = selectJson['enum_meta']
		except Exception as e:
			enum = ""


		if enum:
			for item in enum:
				selectoptions+= """<ion-option value=\""""+item['value']+"""\">"""+item['key']+""" </ion-option>"""
			selecthtml = """<ion-select placeholder=\""""+select['cap']+"""\"  """+input_class+""" [(ngModel)]=\"preset_value."""+select['idt']+"""\"  (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)" (ionChange)="checkChange($event,\'"""+select['idt']+"""\')" data-readonly=\""""+select['iro']+"""\" data-label=\""""+select['cap']+"""\" data-id=\""""+select['idt']+"""\" data-required=\""""+select['ire']+"""\" data-allowduplicate=\""""+select['ad']+"""\" data-hidden=\""""+select['ih']+"""\"
			data-sql=\"\" data-sqldbtype=\"\" data-sqlvaluedependent=\"\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" data-projectid=\""""+str(project_id)+"""\" data-widgettype=\""""+select['wt']+"""\" data-fieldname=\""""+select['idt']+"""\" data-eformid=\""""+str(tx_view_title.identifiers)+"""\" data-modeOfEntry=\""""+select['moe']+"""\" data-suggestive=\""""+select['sug']+"""\"  id=\""""+select['idt']+"""\" name=\""""+select['idt']+"""\" data-displayorder=\""""+str(do)+"""\" data-referjson=\'"""+select['cjson']+"""\'> """+selectoptions+"""</ion-select>"""

		else:
			selecthtml =  """<ion-select placeholder=\""""+select['cap']+"""\" """+input_class+""" [(ngModel)]=\"preset_value."""+select['idt']+"""\" (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)" (ionChange)="checkChange($event,\'"""+select['idt']+"""\')" data-readonly=\""""+select['iro']+"""\" data-label=\""""+select['cap']+"""\" data-id=\""""+select['idt']+"""\" data-required=\""""+select['ire']+"""\" data-allowduplicate=\""""+select['ad']+"""\" data-hidden=\""""+select['ih']+"""\" data-sql=\'"""+sqlDict['Sql']+"""\' data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+select['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" data-projectid=\""""+str(project_id)+"""\" data-widgettype=\""""+select['wt']+"""\" data-fieldname=\""""+select['idt']+"""\" data-eformid=\""""+str(tx_view_title.identifiers)+"""\" data-modeOfEntry=\""""+select['moe']+"""\" data-suggestive=\""""+select['sug']+"""\"  id=\""""+select['idt']+"""\" name=\""""+select['idt']+"""\" data-displayorder=\""""+str(do)+"""\" data-referjson=\'"""+select['cjson']+"""\' data-componenttype=\""""+select['ct']+"""\" >
								<ng-container *ngIf="optionsJson[\'"""+select['idt']+"""\'] != null ">
									<ion-option *ngFor="let item of optionsJson[\'"""+select['idt']+"""\']" value="{{item[\'"""+sqlDict['value']+"""\']}}"> {{item[\'"""+sqlDict['key']+"""\']}} </ion-option>
								</ng-container>
							</ion-select> """


	wholeSelectHtml = """<ion-item """+hide+""" name=\""""+select['idt']+"""item\">"""+selectlabel+selecthtml+"""</ion-item>"""

	return wholeSelectHtml

def radiobox(radiobox,inputtype,label_cr):
	readonly = False

	radioitems = ""

	if radiobox['sql'] == None:
		sqlDict = {}
		sqlDict['Sql'] = ""
		sqlDict['sqlDbType'] = ""
		sqlDict['key'] = ""
		sqlDict['value'] = ""
 	else:
 		sql = radiobox['sql']
		sqlDict =  json.loads(sql)

 	if radiobox['exp'] == None:
 		exp = ""
 	else:
 		exp = radiobox['exp']

 	if radiobox['vep']	== None:
 		vep =""
 	else:
 		vep	=radiobox['vep']

 	if radiobox['ih'] == 'True':
 		hide = "hidden"
		disabled = 'disabled="True"'
 	else:
 		hide=""
		disabled=""

	if radiobox['do'] == None:
 		do = ""
 	else:
 		do = radiobox['do']

	if radiobox['tid'] != None:
		tx_view_id = radiobox['tid']
		tx_view_title = Transactionview.objects.get(pk=tx_view_id)
		project_id = tx_view_title.projectid_id
	else:
		tx_view_id = ""


	if radiobox['cjson']:

		radioJson = json.loads(radiobox['cjson'])

		try:
			enum = radioJson['enum_meta']
		except Exception as e:
			enum = ""

		if enum:
			for item in enum:
				radioitems+= """<ion-item>
										<ion-label>"""+item['key']+""" </ion-label>
										<ion-radio value=\""""+item['value']+"""\"> </ion-radio>
								</ion-item>"""
			radiohtml = """<ion-list radio-group class="radio-group list_group" [(ngModel)]=\"preset_value."""+radiobox['idt']+"""\" (ionChange)="checkChange($event,\'"""+radiobox['idt']+"""\')" id=\""""+radiobox['idt']+"""\" name=\""""+radiobox['idt']+"""\" data-readonly=\""""+radiobox['iro']+"""\" data-required=\""""+radiobox['ire']+"""\" data-allowduplicate=\""""+radiobox['ad']+"""\" data-hidden=\""""+radiobox['ih']+"""\" data-sql=\"\" data-sqldbtype=\"\" data-sqlvalue=\"\" data-sqlvaluedependent=\"\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" data-id=\""""+radiobox['idt']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+radiobox['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" readonly=\""""+radiobox['iro']+"""\" """+hide+""" data-modeOfEntry=\""""+radiobox['moe']+"""\" data-displayorder=\""""+str(do)+"""\" data-suggestive=\""""+radiobox['sug']+"""\" data-referjson=\'"""+radiobox['cjson']+"""\' """+disabled+""">

								<ion-item>
									<ion-label color=\""""+label_cr+"""\">"""+radiobox['cap']+"""</ion-label>
								</ion-item>"""+radioitems+ """</ion-list>"""

			return radiohtml
		else:
			radiohtml =  """<ion-list  radio-group class="radio-group list_group" [(ngModel)]=\"preset_value."""+radiobox['idt']+"""\" (ionChange)="checkChange($event,\'"""+radiobox['idt']+"""\')" id=\""""+radiobox['idt']+"""\" name=\""""+radiobox['idt']+"""\" data-readonly=\""""+radiobox['iro']+"""\" data-required=\""""+radiobox['ire']+"""\" data-allowduplicate=\""""+radiobox['ad']+"""\" data-hidden=\""""+radiobox['ih']+"""\" data-sql=\'"""+sqlDict['Sql']+"""\' data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+radiobox['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" data-id=\""""+radiobox['idt']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+radiobox['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" readonly=\""""+radiobox['iro']+"""\" """+hide+""" data-modeOfEntry=\""""+radiobox['moe']+"""\" data-displayorder=\""""+str(do)+"""\" data-suggestive=\""""+radiobox['sug']+"""\" data-referjson=\'"""+radiobox['cjson']+"""\' """+disabled+""">

								<ion-item>
									<ion-label color=\""""+label_cr+"""\">"""+radiobox['cap']+"""</ion-label>
								</ion-item>
								<ng-container *ngIf="optionsJson[\'"""+radiobox['idt']+"""\'] != null ">
									<ion-item *ngFor="let item of optionsJson[\'"""+radiobox['idt']+"""\']">
										<ion-label>{{item[\'"""+sqlDict['key']+"""\']}}</ion-label>
										<ion-radio value="{{item[\'"""+sqlDict['value']+"""\']}}"></ion-radio>
									</ion-item>
								</ng-container>
							</ion-list>"""
			return radiohtml



def checkbox(checkbox,inputtype,label_cr):
	readonly = False

	checkitems = ""

	if checkbox['sql'] == None:
 		sqlDict = {}
		sqlDict['Sql'] = ""
		sqlDict['sqlDbType'] = ""
		sqlDict['key'] = ""
		sqlDict['value'] = ""
		
 	else:
 		sql = checkbox['sql']
		sqlDict =  json.loads(sql)
		

 	if checkbox['exp'] == None:
 		exp = ""
 	else:
 		exp = checkbox['exp']

 	if checkbox['vep']	== None:
 		vep =""
 	else:
 		vep	=checkbox['vep']

 	if checkbox['ih'] == 'True':
 		hide = "hidden"
 	else:
 		hide=""

	if checkbox['do'] == None:
 		do = ""
 	else:
 		do = checkbox['do']

	if checkbox['tid'] != None:
		tx_view_id = checkbox['tid']
		tx_view_title = Transactionview.objects.get(pk=tx_view_id)
		project_id = tx_view_title.projectid_id
	else:
		tx_view_id = ""


	if checkbox['cjson']:
		checkJson = json.loads(checkbox['cjson'])

		try:
			enum = checkJson['enum_meta']
		except Exception as e:
			enum = ""



		if enum:
			for item in enum:
				checkitems+= """<ion-item>
									<ion-label>""" +item['key']+ """</ion-label>
									<ion-checkbox data-value=\""""+item['value']+"""\" data-key=\""""+item['key']+"""\" data-readonly=\""""+checkbox['iro']+"""\" data-required=\""""+checkbox['ire']+"""\" data-allowduplicate=\""""+checkbox['ad']+"""\" data-hidden=\""""+checkbox['ih']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" data-id=\""""+checkbox['idt']+"""\" readonly=\""""+checkbox['iro']+"""\" """+hide+"""   id=\""""+checkbox['idt']+"""_"""+item['key']+"""\" name=\""""+checkbox['idt']+"""_"""+item['key']+"""\" data-modeOfEntry=\""""+checkbox['moe']+"""\" data-displayorder=\""""+str(do)+"""\" data-suggestive=\""""+checkbox['sug']+"""\" """+hide+""" data-referjson=\'"""+checkbox['cjson']+"""\' (ionChange)="checkChange($event,\'"""+checkbox['idt']+"""\')\" [(ngModel)]=\"preset_value."""+checkbox['idt']+"""_"""+item['key']+"""\"></ion-checkbox>
								</ion-item>"""
			checkhtml = """<ion-list class ="input_border" role="checkgroup"  id=\""""+checkbox['idt']+"""\" name=\""""+checkbox['idt']+"""\" data-readonly=\""""+checkbox['iro']+"""\" data-required=\""""+checkbox['ire']+"""\" data-allowduplicate=\""""+checkbox['ad']+"""\" data-hidden=\""""+checkbox['ih']+"""\" data-sql=\"\" data-sqldbtype=\"\" data-sqlvalue=\"\" data-sqlvaluedependent=\"\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" data-id=\""""+checkbox['idt']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+checkbox['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" readonly=\""""+checkbox['iro']+"""\" """+hide+"""  data-modeOfEntry=\""""+checkbox['moe']+"""\" data-displayorder=\""""+str(do)+"""\" data-suggestive=\""""+checkbox['sug']+"""\" """+hide+""" data-referjson=\'"""+checkbox['cjson']+"""\' ngDefaultControl>
								<ion-item>	<ion-label color=\""""+label_cr+"""\">"""+checkbox['cap']+"""</ion-label>
								</ion-item>"""+ checkitems+"""</ion-list>"""

			return checkhtml
		else:

			checkhtml = """<ion-list class ="input_border" role="checkgroup" id=\""""+checkbox['idt']+"""\" name=\""""+checkbox['idt']+"""\" data-readonly=\""""+checkbox['iro']+"""\" data-required=\""""+checkbox['ire']+"""\" data-allowduplicate=\""""+checkbox['ad']+"""\" data-hidden=\""""+checkbox['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\"  data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+checkbox['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" data-id=\""""+checkbox['idt']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+checkbox['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" readonly=\""""+checkbox['iro']+"""\" """+hide+"""  data-modeOfEntry=\""""+checkbox['moe']+"""\" data-displayorder=\""""+str(do)+"""\" data-suggestive=\""""+checkbox['sug']+"""\" """+hide+""" data-referjson=\'"""+checkbox['cjson']+"""\' ngDefaultControl>
								<ion-item><ion-label color=\""""+label_cr+"""\">"""+checkbox['cap']+"""</ion-label></ion-item>
								<ng-container *ngIf="optionsJson[\'"""+checkbox['idt']+"""\'] != null ">
									<ion-item *ngFor="let item of optionsJson[\'"""+checkbox['idt']+"""\']">
										<ion-label>{{item[\'"""+sqlDict['value']+"""\']}}</ion-label>
										<ion-checkbox (ionChange)=\"checkChange($event,\'"""+checkbox['idt']+"""\')\" id=\""""+checkbox['idt']+"""_"""+item['key']+"""\" name=\""""+checkbox['idt']+"""_"""+item['key']+"""\" [(ngModel)]=\"preset_value."""+checkbox['idt']+"""_"""+item['key']+"""\" data-value=\""""+item['value']+"""\" data-key=\""""+item['key']+"""\"></ion-checkbox>
									</ion-item>
								</ng-container>
							</ion-list>"""

			return checkhtml

def scan(scan,inputtype,label_cr):
	readonly = False
	if scan['sql'] == None:
		sqlDict = {}
		sqlDict['Sql'] = ""
		sqlDict['sqlDbType'] = ""
		sqlDict['key'] = ""
		sqlDict['value'] = ""
	
	else:
		sql = select['sql']
		sqlDict =  json.loads(sql)
		
	if scan['exp'] == None:
		exp = ""
 	else:
 		exp = scan['exp']

 	if scan['vep']	== None:
 		vep =""
 	else:
 		vep	=scan['vep']

 	if scan['ih'] == 'True':
 		hide = "hidden"
 	else:
 		hide=""

	if scan['cjson']:
		timeJson = json.loads(scan['cjson'])

	else:
		timeJson = ""

	if scan['tid'] != None:
		tx_view_id = scan['tid']
		tx_view_title = Transactionview.objects.get(pk=tx_view_id)
		project_id = tx_view_title.projectid_id
	else:
		tx_view_id = ""

	if scan['do'] == None:
 		do = ""
 	else:
 		do = scan['do']

	if scan['iro'] == 'True':
 		disable ="disabled"
	else:
 		 disable =""

	scanhtml =""
	if inputtype == "placeholder":
		labelhtml = """"""
		inputhtml ="""<ion-input type=\""""+scan['wt']+"""\" placeholder=\""""+scan['cap']+"""\" class="input_border" data-id=\""""+scan['idt']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+scan['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" data-readonly=\""""+scan['iro']+"""\" data-required=\""""+scan['ire']+"""\" data-allowduplicate=\""""+scan['ad']+"""\" data-hidden=\""""+scan['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+scan['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" data-displayorder=\""""+str(do)+"""\" id=\""""+scan['idt']+"""\" name=\""""+scan['idt']+"""\" [(ngModel)]=\"preset_value."""+scan['idt']+"""\"  disabled="true" data-modeOfEntry=\""""+scan['moe']+"""\" data-suggestive=\""""+scan['sug']+"""\" """+hide+"""  data-referjson=\'"""+scan['cjson']+"""\'></ion-input>"""
	else:
		if inputtype =='boxed':
			labelclass = 'class="content_padding"'
			inputclass ='class = "input_for_boxed"'
			inputstyle = 'stacked'
			placeholder= """placeholder=\""""+scan['cap']+"""\""""
		elif inputtype == 'stacked' or inputtype =='floating':
			inputstyle = 'stacked'
			labelclass = ''
			inputclass ='class = "input_border"'
			placeholder= """placeholder=\""""+scan['cap']+"""\""""
		else:
			inputstyle = inputtype
			labelclass = ''
			inputclass ='class = "input_border"'
			placeholder= """placeholder=\""""+scan['cap']+"""\""""


		labelhtml = """<ion-item><ion-label color=\""""+label_cr+"""\" """+labelclass+""" """+inputstyle+""">""" +scan['cap']+ """</ion-label></ion-item>"""
		inputhtml ="""<ion-input """+inputclass+""" type=\""""+scan['wt']+"""\" """+placeholder+"""  data-id=\""""+scan['idt']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+scan['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" data-readonly=\""""+scan['iro']+"""\" data-required=\""""+scan['ire']+"""\" data-allowduplicate=\""""+scan['ad']+"""\" data-hidden=\""""+scan['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+scan['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" data-displayorder=\""""+str(do)+"""\" id=\""""+scan['idt']+"""\" name=\""""+scan['idt']+"""\" [(ngModel)]=\"preset_value."""+scan['idt']+"""\"  disabled="true" data-modeOfEntry=\""""+scan['moe']+"""\" data-suggestive=\""""+scan['sug']+"""\" """+hide+"""  data-referjson=\'"""+scan['cjson']+"""\'></ion-input>"""

	if inputtype == 'fixed':
		labelhtml = """<ion-label color=\""""+label_cr+"""\" """+labelclass+""" """+inputstyle+""">""" +scan['cap']+ """</ion-label>"""
		scanhtml ="""<ion-list class="list_group"><ion-row><ion-col col-10><ion-item>"""+labelhtml+inputhtml+"""</ion-item></ion-col><ion-thumbnail item-end><button ion-button outline icon-only color="secondary" (click)="scan($event,\'"""+scan['idt']+"""\')"><ion-icon name="barcode"></ion-icon></button></ion-thumbnail></ion-row></ion-list>"""
	else:
		scanhtml ="""<ion-list class="list_group">"""+labelhtml+"""<ion-row><ion-col col-10>"""+inputhtml+"""</ion-col><ion-thumbnail item-end><button ion-button outline icon-only color="secondary" (click)="scan($event,\'"""+scan['idt']+"""\')"><ion-icon name="barcode"></ion-icon></button></ion-thumbnail></ion-row></ion-list>"""

	return scanhtml


def upload(upload,inputtype,label_cr):
	readonly = False
	if upload['sql'] == None:
		sqlDict = {}
		sqlDict['Sql'] = ""
		sqlDict['sqlDbType'] = ""
		sqlDict['key'] = ""
		sqlDict['value'] = ""
	else:
		sql = upload['sql']
		sqlDict =  json.loads(sql)

	if upload['exp'] == None:
		exp = ""
 	else:
 		exp = upload['exp']

 	if upload['vep']	== None:
 		vep =""
 	else:
 		vep	=upload['vep']

 	if upload['ih'] == 'True':
 		hide = "hidden"
 	else:
 		hide=""

	if upload['cjson']:
		timeJson = json.loads(upload['cjson'])

	else:
		timeJson = ""

	if upload['tid'] != None:
		tx_view_id = upload['tid']
		tx_view_title = Transactionview.objects.get(pk=tx_view_id)
		project_id = tx_view_title.projectid_id
	else:
		tx_view_id = ""

	if upload['do'] == None:
 		do = ""
 	else:
 		do = upload['do']

	if upload['iro'] == 'True':
 		disable ="disabled"
	else:
 		 disable =""

	if inputtype == "placeholder":
		labelhtml = """"""
		inputhtml ="""<ion-input type="number" class="input_border" [(ngModel)]="fileCount" placeholder=\""""+upload['cap']+"""\" readonly data-id=\""""+upload['idt']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+upload['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" data-readonly=\""""+upload['iro']+"""\" data-required=\""""+upload['ire']+"""\" data-allowduplicate=\""""+upload['ad']+"""\" data-hidden=\""""+upload['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" data-displayorder=\""""+str(do)+"""\" id=\""""+upload['idt']+"""\" name=\""""+upload['idt']+"""\"  disabled="true" data-modeOfEntry=\""""+upload['moe']+"""\" data-suggestive=\""""+upload['sug']+"""\" """+hide+"""  [(ngModel)]=\"preset_value."""+upload['idt']+"""\" data-referjson=\'"""+upload['cjson']+"""\'></ion-input>"""
	else:
		if inputtype =='boxed':
			labelclass = 'class="content_padding"'
			inputclass ='class = "input_for_boxed"'
			inputstyle = 'stacked'
			placeholder= """placeholder=\""""+upload['cap']+"""\""""
		elif inputtype == 'stacked' or inputtype =='floating':
			inputstyle = 'stacked'
			labelclass = ''
			inputclass ='class = "input_border"'
			placeholder= """placeholder=\""""+upload['cap']+"""\""""
		else:
			inputstyle = inputtype
			labelclass = ''
			inputclass ='class = "input_border"'
			placeholder= """placeholder=\""""+upload['cap']+"""\""""


		labelhtml = """<ion-item><ion-label color=\""""+label_cr+"""\" """+labelclass+""" """+inputstyle+""">""" +upload['cap']+ """</ion-label></ion-item>"""
		inputhtml ="""<ion-input type="number" """+inputclass+""" [(ngModel)]="fileCount" """+placeholder+""" readonly data-id=\""""+upload['idt']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+upload['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" data-readonly=\""""+upload['iro']+"""\" data-required=\""""+upload['ire']+"""\" data-allowduplicate=\""""+upload['ad']+"""\" data-hidden=\""""+upload['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+upload['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" data-displayorder=\""""+str(do)+"""\" id=\""""+upload['idt']+"""\" name=\""""+upload['idt']+"""\"  disabled="true" data-modeOfEntry=\""""+upload['moe']+"""\" data-suggestive=\""""+upload['sug']+"""\" """+hide+"""  [(ngModel)]=\"preset_value."""+upload['idt']+"""\" data-referjson=\'"""+upload['cjson']+"""\'></ion-input>"""

	uploadhtml =""
	if inputtype == 'fixed':
		labelhtml = """<ion-label color=\""""+label_cr+"""\">""" +upload['cap']+ """</ion-label>"""
		uploadhtml ="""<ion-list><ion-row><ion-col col-10><ion-item>"""+labelhtml+inputhtml+"""</ion-item></ion-col><ion-thumbnail item-end><button ion-button outline icon-only color="secondary" (click)=\"upload($event)\" """+hide+"""><ion-icon name="attach"></ion-icon></button>
		</ion-thumbnail></ion-row></ion-list>"""
	else:
		uploadhtml ="""<ion-list>"""+labelhtml+"""<ion-row><ion-col col-10>"""+inputhtml+"""</ion-col><ion-thumbnail item-end><button ion-button outline icon-only color="secondary" (click)=\"upload($event)\" """+hide+"""><ion-icon name="attach"></ion-icon></button>
		</ion-thumbnail></ion-row></ion-list>"""

	return uploadhtml


def stot(stot,inputtype,label_cr):
	readonly = False
	if stot['sql'] == None:
		sqlDict = {}
		sqlDict['Sql'] = ""
		sqlDict['sqlDbType'] = ""
		sqlDict['key'] = ""
		sqlDict['value'] = ""
		
	else:
		sql = stot['sql']
		sqlDict =  json.loads(sql)

	if stot['exp'] == None:
		exp = ""
 	else:
 		exp = stot['exp']

 	if stot['vep']	== None:
 		vep =""
 	else:
 		vep	=stot['vep']

 	if stot['ih'] == 'True':
 		hide = "hidden"
 	else:
 		hide=""

	if stot['cjson']:
		timeJson = json.loads(stot['cjson'])

	else:
		timeJson = ""

	if stot['tid'] != None:
		tx_view_id = stot['tid']
		tx_view_title = Transactionview.objects.get(pk=tx_view_id)
		project_id = tx_view_title.projectid_id
	else:
		tx_view_id = ""

	if stot['do'] == None:
 		do = ""
 	else:
 		do = stot['do']

	if stot['iro'] == 'True':
 		disable ="disabled"
	else:
 		 disable =""

	if inputtype == "placeholder":
		labelhtml = """"""
		inputhtml ="""<ion-input type="text" [(ngModel)]="speech" placeholder=\""""+stot['cap']+"""\" readonly data-id=\""""+stot['idt']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+stot['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" data-readonly=\""""+stot['iro']+"""\" data-required=\""""+stot['ire']+"""\" data-allowduplicate=\""""+stot['ad']+"""\" data-hidden=\""""+stot['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+stot['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" data-displayorder=\""""+str(do)+"""\" id=\""""+stot['idt']+"""\" name=\""""+stot['idt']+"""\"  disabled="true" data-modeOfEntry=\""""+stot['moe']+"""\" data-suggestive=\""""+stot['sug']+"""\" """+hide+""" [(ngModel)]=\"preset_value."""+stot['idt']+"""\" data-referjson=\'"""+stot['cjson']+"""\'></ion-input>"""
	else:
		if inputtype =='boxed':
			labelclass = 'class="content_padding"'
			inputclass ='class = "input_for_boxed"'
			inputstyle = 'stacked'
			placeholder= """placeholder=\""""+stot['cap']+"""\""""
		elif inputtype == 'stacked' or inputtype =='floating':
			inputstyle = 'stacked'
			labelclass = ''
			inputclass ='class = "input_border"'
			placeholder= """placeholder=\""""+stot['cap']+"""\""""
		else:
			inputstyle = inputtype
			labelclass = ''
			inputclass ='class = "input_border"'
			placeholder= """placeholder=\""""+upload['cap']+"""\""""


		labelhtml = """<ion-item><ion-label color=\""""+label_cr+"""\">""" +stot['cap']+ """</ion-label></ion-item>"""
		inputhtml ="""<ion-input type="text" [(ngModel)]="speech" """+inputclass+""" placeholder=\""""+stot['cap']+"""\" readonly data-id=\""""+stot['idt']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+stot['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" data-readonly=\""""+stot['iro']+"""\" data-required=\""""+stot['ire']+"""\" data-allowduplicate=\""""+stot['ad']+"""\" data-hidden=\""""+stot['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" data-displayorder=\""""+str(do)+"""\" id=\""""+stot['idt']+"""\" name=\""""+stot['idt']+"""\"  disabled="true" data-modeOfEntry=\""""+stot['moe']+"""\" data-suggestive=\""""+stot['sug']+"""\" """+hide+""" [(ngModel)]=\"preset_value."""+stot['idt']+"""\" data-referjson=\'"""+stot['cjson']+"""\'></ion-input>"""

	stothtml =""
	if inputtype =='fixed':
		stothtml ="""<ion-list><ion-row><ion-col col-10>"""+labelhtml+inputhtml+"""</ion-col><ion-thumbnail item-end><button ion-button outline icon-only color="secondary" (click)=\"mic($event)\" """+hide+"""> <ion-icon md="md-mic"></ion-icon></button></ion-thumbnail></ion-row></ion-list>"""
	else:
		stothtml ="""<ion-list>"""+labelhtml+"""<ion-row><ion-col col-10>"""+inputhtml+"""</ion-col><ion-thumbnail item-end><button ion-button outline icon-only color="secondary" (click)=\"mic($event)\" """+hide+"""> <ion-icon md="md-mic"></ion-icon></button></ion-thumbnail></ion-row></ion-list>"""

	return stothtml


def dynamic_popup(dpop,inputtype,label_cr):
	dynamic_popuphtml =""""""
 	readonly =False
	hide=""

 	if dpop['sql'] == None or dpop['sql'] == "":
		sqlDict = {}
		sqlDict['Sql'] = ""
		sqlDict['sqlDbType'] = ""
		sqlDict['key'] = ""
		sqlDict['value'] = ""

 	else:
 		sql = dpop['sql']
		sqlDict =  json.loads(sql)

	if dpop['exp'] == None:
 		exp = ""
 	else:
 		exp = dpop['exp']

 	if dpop['vep']	== None:
 		vep =""
 	else:
 		vep	=dpop['vep']

 	if dpop['ih'] == 'True':
 		hide = "hidden"
 	else:
 		hide= ""

	if dpop['tid'] != None:
		tx_view_id = dpop['tid']
		tx_view_title = Transactionview.objects.get(pk=tx_view_id)
		project_id = tx_view_title.projectid_id

	else:
		tx_view_id = ""

	if dpop['do'] == None:
 		do = ""
 	else:
 		do = dpop['do']


 	if 	dpop['iro'] == 'True':
 		disable ="disabled"
 	else:
 		 disable =""

 	if inputtype == 'placeholder':
 		dynamic_popuphtml = """<ion-item """+hide+""" name=\""""+dpop['idt']+"""item\" ><ion-input type=\""""+dpop['wt']+"""\" placeholder=\""""+dpop['cap']+"""\" class="input_border" data-id=\""""+dpop['idt']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+dpop['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" data-readonly=\""""+dpop['iro']+"""\" data-required=\""""+dpop['ire']+"""\" data-allowduplicate=\""""+dpop['ad']+"""\" data-hidden=\""""+dpop['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+dpop['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" data-displayorder=\""""+str(do)+"""\" id=\""""+dpop['idt']+"""\" name=\""""+dpop['idt']+"""\" readonly=\""""+dpop['iro']+"""\" data-modeOfEntry=\""""+dpop['moe']+"""\" data-suggestive=\""""+dpop['sug']+"""\" """+hide+"""  data-referjson=\'"""+dpop['cjson']+"""\' [(ngModel)]=\"preset_value."""+dpop['idt']+"""\"  (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)" required></ion-input></ion-item>"""

	elif inputtype =='boxed':
 		dynamic_popuphtml = """<ion-item """+hide+""" name=\""""+dpop['idt']+"""item\"><ion-label color=\""""+label_cr+"""\" class="content_padding" stacked>"""+dpop['cap']+"""</ion-label><ion-input type=\""""+dpop['wt']+"""\" placeholder=\""""+dpop['cap']+"""\" class="input_for_boxed" data-id=\""""+dpop['idt']+"""\" placeholder=\""""+dpop['cap']+"""\" data-readonly=\""""+dpop['iro']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+dpop['idt']+"""\" data-eformid=\""""+str(tx_view_title)+"""\" data-required=\""""+dpop['ire']+"""\" data-allowduplicate=\""""+dpop['ad']+"""\" data-hidden=\""""+dpop['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+dpop['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" id=\""""+dpop['idt']+"""\" name=\""""+dpop['idt']+"""\" readonly=\""""+dpop['iro']+"""\" data-modeOfEntry=\""""+dpop['moe']+"""\" data-displayorder=\""""+str(do)+"""\" data-suggestive=\""""+dpop['sug']+"""\" data-referjson=\'"""+dpop['cjson']+"""\' """+hide+""" """+disable+""" [(ngModel)]=\"preset_value."""+dpop['idt']+"""\" (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)"></ion-input></ion-item>"""
 	else:
		if inputtype =='floating':
			placeholder = ""
		else:
			placeholder = """placeholder=\""""+dpop['cap']+"""\""""
 		dynamic_popuphtml = """<ion-item """+hide+""" name=\""""+dpop['idt']+"""item\"><ion-label color=\""""+label_cr+"""\" """+inputtype+""" """+hide+""">"""+dpop['cap']+"""</ion-label><ion-input type=\""""+dpop['wt']+"""\" """+placeholder+""" class="input_border" data-label=\""""+dpop['cap']+"""\" data-id=\""""+dpop['idt']+"""\" data-projectid=\""""+str(project_id)+"""\" data-fieldname=\""""+dpop['idt']+"""\" """+disable+""" data-eformid=\""""+str(tx_view_title)+"""\" data-readonly=\""""+dpop['iro']+"""\" data-required=\""""+dpop['ire']+"""\" data-allowduplicate=\""""+dpop['ad']+"""\" data-hidden=\""""+dpop['ih']+"""\" data-sql=\""""+sqlDict['Sql']+"""\" data-sqldbtype=\""""+sqlDict['sqlDbType']+"""\" data-sqlvalue=\""""+sqlDict['value']+"""\" data-sqlvaluedependent=\""""+dpop['isdep']+"""\" data-expression=\""""+exp+"""\" data-validateexp=\""""+vep+"""\" data-displayorder=\""""+str(do)+"""\" id=\""""+dpop['idt']+"""\" name=\""""+dpop['idt']+"""\" readonly=\""""+dpop['iro']+"""\" data-modeOfEntry=\""""+dpop['moe']+"""\" data-suggestive=\""""+dpop['sug']+"""\" """+hide+""" data-referjson=\'"""+dpop['cjson']+"""\' [(ngModel)]=\"preset_value."""+dpop['idt']+"""\" (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)" required></ion-input></ion-item>"""

	return dynamic_popuphtml


def children(childrens,fileName,ptitle,label_cr):
	if childrens['ctype'] == 'card':
		cardhtml = card(childrens,"",fileName,ptitle,label_cr)
		childrenhtml = cardhtml

	if childrens['ctype'] == 'list':
		listhtml = lists(childrens,"",fileName,ptitle,label_cr)
		childrenhtml = listhtml

	if childrens['ctype'] == 'grid':
		idt = childrens['idt']
		gridhtml = grid(childrens,"",fileName+idt,ptitle,label_cr)
		childrenhtml = gridhtml

	return childrenhtml

@csrf_exempt
def updateSqlInDb(request,txviewid):
	db_error =[]
	errors = dbconnection(request,txviewid)
	if len(errors) > 0:
		for error in errors:
			db_error.append(str(error))
		return HttpResponse(json.dumps(db_error))
	else:
		return HttpResponse("SUCCESS")
