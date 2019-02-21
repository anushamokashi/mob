# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from Mobilebuilder.decorators import myuser_login_required 
from .models import Role,ViewsForRole
from .forms import RoleForm,RoleViewForm
from .serializers import RoleSerializer,ViewsForRoleSerializer
from project.models import Project, Projectwiseusersetup
from authentication.models import userprofile
from transactionview.models import Transactionview
from reportview.models import Report
from rolesetup.models import Role
from hometemplate.models import Homepage,Menu
import json


# Create your views here.

@myuser_login_required
def roleindex(request):
	loginModel = userprofile.objects.get(is_user = True ,id = request.session['userid'])
	element =Projectwiseusersetup.objects.get(userid=loginModel.id,project_id_id = request.session['projectid'] )
	projectselect =Projectwiseusersetup.objects.filter(userid =request.session['userid'])
	project_title = element.project_id.title
	projectid = request.session['projectid']

	roleObj = Role.objects.all()
	role_serializer = RoleSerializer(instance=roleObj,many=True)
	role_serializer_json = json.dumps(role_serializer.data)
	print role_serializer_json
	role_serializer_json_obj = json.loads(role_serializer_json)


	roledata = Role.objects.filter(projectid_id = projectid)
	return render(request, 'roleindex.html', locals())

def rolesave(request):
	projectid = request.session['projectid']
	if request.method == 'POST':
		roleform = RoleForm(request.POST)
		
		if roleform.is_valid():
			newRole = roleform.save()
			
			return HttpResponse("Success")
		else:
			print roleform.errors
			return HttpResponse("Failure")
		
		
	else:
		roleform = RoleForm()
		return render(request,'rolemodal.html',locals())

def roleedit(request,roleid):
	roleObj = Role.objects.get(id=roleid)
	
	if request.method == 'POST':
		roleform = RoleForm(request.POST,instance=roleObj)
		
		if roleform.is_valid():
			newRole = roleform.save()
			
			return HttpResponse("Success")
		else:
			print roleform.errors
			return HttpResponse("Failure")
		
		
	else:
		roleform = RoleForm(instance=roleObj)
		return render(request,'roleeditmodal.html',locals())

def roledelete(request,roleid):
	projectid = request.session['projectid']
	try:
		query = Role.objects.get(id=roleid)
	except Role.DoesNotExist:
		query = None
    
	if query:
		query.delete()
		
	return HttpResponseRedirect('/rolesetup/roleindex/') 

@csrf_exempt
def assignview(request,roleid):
	projectid = request.session['projectid']
	txViewList= []
	reportViewList = []

	roleObj = Role.objects.get(id=roleid)
	
	try:
		roleViewObj = ViewsForRole.objects.get(role = roleObj.id)
		
	except ViewsForRole.DoesNotExist:
		roleViewObj = None
	
	print "ROLEVIEWOBJ", roleViewObj
	
	if request.method == 'POST':

		try:
			txViewUniList  = request.POST.getlist("txview")
			for x in txViewUniList:
				txViewList.append(x.encode('UTF8'))
		except Exception as e:
			txViewList = []

		try:
			reportViewUniList  = request.POST.getlist("reportview")
			for x in reportViewUniList:
				reportViewList.append(x.encode('UTF8'))
		except Exception as e:
			reportViewList = []
		
		
		if roleViewObj:
			roleViewObj.txview = json.dumps(txViewList)
			roleViewObj.reportview = json.dumps(reportViewList)
			roleViewObj.save()
			return HttpResponse("Success")
		else:
			roleview = ViewsForRole()
			roleview.role = roleObj
			roleview.txview = json.dumps(txViewList)
			roleview.reportview = json.dumps(reportViewList)
			roleview.save()	
			return HttpResponse("Success")	
		
	else:
		txViewObjs = []
		reportViewObjs = []
		selectedTxview = []
		selectedReportView = []
		
		try:
			homeObj = Homepage.objects.get(project_id_id=projectid)
		except Homepage.DoesNotExist:
			homeObj=None

		if homeObj:
			try:
				homeTxViews = Menu.objects.filter(homepageid_id=homeObj.id,typeofview="transactionview",createpage=True)
			except Menu.DoesNotExist:
				homeTxViews = None
			
			try:
				homeReportViews = Menu.objects.filter(homepageid_id=homeObj.id,typeofview="reportview",createpage=True)
			except Menu.DoesNotExist:
				homeReportViews = None

		
		

		# txViewObjs = Transactionview.objects.filter(projectid_id=projectid)
		# reportViewObjs = Report.objects.filter(project_id=projectid)
		
		
		if roleViewObj:
			selectedTxviewJson = roleViewObj.txview  #list as a unicode
			selectedReportViewJson = roleViewObj.reportview		
			selectedTxviewUnicode = json.loads(selectedTxviewJson) #list of unicodes			
			selectedReportViewUnicode = json.loads(selectedReportViewJson)
			for x in selectedTxviewUnicode:
				selectedTxview.append(long(x))
			for y in selectedReportViewUnicode:
				selectedReportView.append(long(y))		
		else:
			selectedTxview = None
			selectedReportView = None

	

	return render(request,'viewsetup.html',locals())
