from __future__ import unicode_literals
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse ,HttpResponseBadRequest
from .models import Project, Projectwiseusersetup ,IonicImages,IonicFonts,IonicServices,IonicNotification,EmailConfiguration,GoogleAPISetup,GeolocationSetup
from schema.models import Db_profile
from .forms import ProjectForm, ProjectwiseusersetupForm ,IonicProjectConfig,IonicImagesForm,IonicFontsForm,IonicServicesForm,IonicNotificationForm,EmailConfigurationForm,GoogleAPISetupForm,GeolocationSetupForm
from authentication.models import userprofile
from django.views.decorators.csrf import csrf_exempt
from Mobilebuilder.decorators import myadmin_login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from transaction.models import Transaction,Txtabledetails,Txtablecomponentdetails
from transactionview.views import pagemeta
from logintemplate.views import generateLoginpage
from reportview.views import reppagemeta
from hometemplate.views import homehtml
from hometemplate.models import Homepage,Menu
from hometemplate.serializers import HomepageSerializer
from logintemplate.models import Login,GeneralInfo
from eventconfiguration.models import TxnMappingForEvent
from django.template.defaultfilters import slugify
from smssetup.models import SMSServer,SMSAttributes
from smssetup.forms import SMSServerForm,SMSAttributesForm
from update_sms_in_db import update_sms_setup
from update_email_config import update_email_setup
from django.forms.models import modelformset_factory
from django.db.models import Q
import subprocess
import os 
import json
import zipfile
import StringIO
import sqlite3
import MySQLdb
import shutil

# Create your views here
filePath = settings.MEDIA_ROOT

#Display Project List
@myadmin_login_required
def projectindex(request):
	adminid = request.session['loggedinuserid']
	adminname = userprofile.objects.get(pk=adminid)
	#print adminid
	project = Project.objects.filter(admin_id = adminid )
	context = {'project':project}
	return render(request, 'projectindex.html', locals())

#New Project Creation
@myadmin_login_required
def projectcreation(request):
	adminid = request.session['loggedinuserid']
	adminname = userprofile.objects.get(pk=adminid)
	#print request.POST
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		#print form.is_valid()
		#print form.errors
		if form.is_valid():
			new_project = form.save(commit=False)
			new_project.admin_id = userprofile.objects.get(pk=request.session['loggedinuserid'])
			new_project.slug = slugify(new_project.title).replace("-","_")
			new_project.save()
			create_sqlitedb(new_project.slug)
			create_muserTxn(new_project.id)

			return HttpResponseRedirect('/project/projectindex/')
	else:
		form = ProjectForm() #An Unbound Form

	return render(request, 'projectcreation.html', locals())


def create_sqlitedb(slug):
	try:
		if not os.path.exists(filePath+"static/ionicmeta/"+slug):
			os.makedirs(filePath+"static/ionicmeta/"+slug)
			os.makedirs(filePath+"static/ionicmeta/"+slug+"/db")

		con = sqlite3.connect(filePath+"static/ionicmeta/"+slug+"/db/"+slug+".db")

	except Exception as e:
		print e
		pass

	return "success"

def create_muserTxn(id):
	txnObj = Transaction.objects.create(txname="Muser",txdescription="Muser",projectid_id=id)
	tableObj = Txtabledetails.objects.create(title="Muser",
								tablename="muser",
								description="muser",
								relationshiptype="one-to-many",
								transactionid_id = txnObj.id,
								projectid_id = id,
								isprimary = True,
								table_slug = "muser",
								db_type = "both",
								status = "new",
								)
	Txtablecomponentdetails.objects.create(title='first_name',txtabledetailid_id = tableObj.id,columnname='first_name',datatype='CharField',maxlength=50,no_of_decimal_digits=0,field_slug='first_name', isdbfield=True, isnull= False, is_system_component = False, db_type=tableObj.db_type,status="new")
	Txtablecomponentdetails.objects.create(title='last_name',txtabledetailid_id = tableObj.id,columnname='last_name',datatype='CharField',maxlength=50,no_of_decimal_digits=0,field_slug='last_name', isdbfield=True, isnull= True, is_system_component = False, db_type=tableObj.db_type,status="new")
	Txtablecomponentdetails.objects.create(title='mobile_number',txtabledetailid_id = tableObj.id,columnname='mobile_number',datatype='IntegerField',maxlength=30,no_of_decimal_digits=0,field_slug='mobile_number', isdbfield=True, isnull= False, is_system_component = False, db_type=tableObj.db_type,status="new")
	Txtablecomponentdetails.objects.create(title='email_id',txtabledetailid_id = tableObj.id,columnname='email_id',datatype='CharField',maxlength=40,no_of_decimal_digits=0,field_slug='email_id', isdbfield=True, isnull= False, is_system_component = False, db_type=tableObj.db_type,status="new")
	Txtablecomponentdetails.objects.create(title='pwd',txtabledetailid_id = tableObj.id,columnname='pwd',datatype='CharField',maxlength=40,no_of_decimal_digits=0,field_slug='pwd', isdbfield=True, isnull= False, is_system_component = False, db_type=tableObj.db_type,status="new")
	Txtablecomponentdetails.objects.create(title='confirm_password',txtabledetailid_id = tableObj.id,columnname='confirm_password',datatype='CharField',maxlength=40,no_of_decimal_digits=0,field_slug='confirm_password', isdbfield=True, isnull= False, is_system_component = False, db_type=tableObj.db_type,status="new")
	Txtablecomponentdetails.objects.create(title='role',txtabledetailid_id = tableObj.id,columnname='role',datatype='CharField',maxlength=20,no_of_decimal_digits=0,field_slug='role', isdbfield=True, isnull= True, is_system_component = False, db_type=tableObj.db_type,status="new")
	Txtablecomponentdetails.objects.create(title='onesignalplayer_id',txtabledetailid_id = tableObj.id,columnname='onesignalplayer_id',datatype='CharField',maxlength=70,no_of_decimal_digits=0,field_slug='onesignalplayer_id', isdbfield=True, isnull= True, is_system_component = False, db_type=tableObj.db_type,status="new")
	Txtablecomponentdetails.objects.create(title='is_active',txtabledetailid_id = tableObj.id,columnname='is_active',datatype='BooleanField',maxlength=10,no_of_decimal_digits=0,field_slug='is_active', isdbfield=True, isnull= True, is_system_component = False, db_type=tableObj.db_type,status="new")
	Txtablecomponentdetails.objects.create(title='imei_no',txtabledetailid_id = tableObj.id,columnname='imei_no',datatype='IntegerField',maxlength=50,no_of_decimal_digits=0,field_slug='imei_no', isdbfield=True, isnull= True, is_system_component = False, db_type=tableObj.db_type,status="new")
	
	Txtablecomponentdetails.objects.create(title='is cancelled',txtabledetailid_id = tableObj.id,columnname='is cancelled',datatype='CharField',maxlength=100,no_of_decimal_digits=0,field_slug='is_cancelled', isdbfield=True, isnull= True, is_system_component = True, db_type=tableObj.db_type,status="new")
	Txtablecomponentdetails.objects.create(title='unique id field',txtabledetailid_id = tableObj.id,columnname='unique id field',datatype='UUIDField',maxlength=100,no_of_decimal_digits=0,field_slug='unique_id_field', isdbfield=True, isnull= True, is_system_component = True, db_type=tableObj.db_type,status="new")
	Txtablecomponentdetails.objects.create(title='created on',txtabledetailid_id = tableObj.id,columnname='created on',datatype='DateTimeField',maxlength=100,no_of_decimal_digits=0,field_slug='created_on', isdbfield=True, isnull= True, is_system_component = True, db_type=tableObj.db_type,status="new")
	Txtablecomponentdetails.objects.create(title='created by',txtabledetailid_id = tableObj.id,columnname='created by',datatype='CharField',maxlength=100,no_of_decimal_digits=0,field_slug='created_by', isdbfield=True, isnull= True, is_system_component = True, db_type=tableObj.db_type,status="new")
	Txtablecomponentdetails.objects.create(title='modified on',txtabledetailid_id = tableObj.id,columnname='modified on',datatype='DateTimeField',maxlength=100,no_of_decimal_digits=0,field_slug='modified_on', isdbfield=True, isnull= True, is_system_component = True, db_type=tableObj.db_type,status="new")
	Txtablecomponentdetails.objects.create(title='modified by',txtabledetailid_id = tableObj.id,columnname='modified by',datatype='CharField',maxlength=100,no_of_decimal_digits=0,field_slug='modified_by', isdbfield=True, isnull= True, is_system_component = True, db_type=tableObj.db_type,status="new")
	Txtablecomponentdetails.objects.create(title='upstream_txview_ref_id',txtabledetailid_id = tableObj.id,columnname='upstream_txview_ref_id',datatype='IntegerField',maxlength=100,no_of_decimal_digits=0,field_slug='upstream_txview_ref_id', isdbfield=True, isnull= True, is_system_component = True, db_type=tableObj.db_type,status="new")
	Txtablecomponentdetails.objects.create(title='post_tx_title',txtabledetailid_id = tableObj.id,columnname='post_tx_title',datatype='CharField',maxlength=100,no_of_decimal_digits=0,field_slug='post_tx_title', isdbfield=True, isnull= True, is_system_component = True, db_type=tableObj.db_type,status="new")
	Txtablecomponentdetails.objects.create(title='userid',txtabledetailid_id = tableObj.id,columnname='userid',datatype='CharField',maxlength=100,no_of_decimal_digits=0,field_slug='userid', isdbfield=True, isnull= True, is_system_component = True, db_type=tableObj.db_type,status="new")
	Txtablecomponentdetails.objects.create(title='projectid',txtabledetailid_id = tableObj.id,columnname='projectid',datatype='CharField',maxlength=100,no_of_decimal_digits=0,field_slug='projectid', isdbfield=True, isnull= True, is_system_component = True, db_type=tableObj.db_type,status="new")
	Txtablecomponentdetails.objects.create(title='ipadd',txtabledetailid_id = tableObj.id,columnname='ipadd',datatype='CharField',maxlength=100,no_of_decimal_digits=0,field_slug='ipadd', isdbfield=True, isnull= True, is_system_component = True, db_type=tableObj.db_type,status="new")
	Txtablecomponentdetails.objects.create(title='recid',txtabledetailid_id = tableObj.id,columnname='recid',datatype='IntegerField',maxlength=100,no_of_decimal_digits=0,field_slug='recid', isdbfield=True, isnull= True, is_system_component = True, db_type=tableObj.db_type,status="new")
	Txtablecomponentdetails.objects.create(title='versionid',txtabledetailid_id = tableObj.id,columnname='versionid',datatype='CharField',maxlength=100,no_of_decimal_digits=0,field_slug='versionid', isdbfield=True, isnull= True, is_system_component = True, db_type=tableObj.db_type,status="new")
	Txtablecomponentdetails.objects.create(title='roleid',txtabledetailid_id = tableObj.id,columnname='roleid',datatype='CharField',maxlength=100,no_of_decimal_digits=0,field_slug='roleid', isdbfield=True, isnull= True, is_system_component = True, db_type=tableObj.db_type,status="new")               
	Txtablecomponentdetails.objects.create(title='objectid',txtabledetailid_id = tableObj.id,columnname='objectid',datatype='CharField',maxlength=100,no_of_decimal_digits=0,field_slug='objectid', isdbfield=True, isnull= True, is_system_component = True, db_type=tableObj.db_type,status="new")               


#Delete Project
@myadmin_login_required
def pdelete(request, projectid):
    query = Project.objects.get(id = projectid)
    query.delete()
    return HttpResponseRedirect('/project/projectindex/')

#Edit Project
@myadmin_login_required
def pedit(request, projectid):
	adminid = request.session['loggedinuserid']
	adminname = userprofile.objects.get(pk=adminid)
	#print request.POST
	query = Project.objects.get(id = projectid)
	if request.method == 'POST':
		form = ProjectForm(request.POST, instance=query)
		if form.is_valid():
			new_project = form.save(commit = False)
			new_project.slug = slugify(new_project.title).replace("-","_")
			new_project.save()
			return HttpResponseRedirect('/project/projectindex/')
	else:
		form = ProjectForm(instance=query) #An Unbound Form
	return render(request, 'pedit.html', locals())

#Project Getin
@myadmin_login_required
def getin(request, projectid):
	adminid = request.session['loggedinuserid']
	adminname = userprofile.objects.get(pk=adminid)
	projectselect = Project.objects.filter(admin_id_id =adminid)
	#print request.POST
	loggedinuserid = request.session['loggedinuserid']
	users = userprofile.objects.filter(adminuserid=loggedinuserid)
	projectInstance = Project.objects.get(id = projectid)
	currentProject = projectInstance.id
	ptitle = projectInstance.title
	request.session['currentProject'] = projectInstance.id
	form = ProjectForm(instance=projectInstance)
	tform = ProjectwiseusersetupForm()
	objs = Projectwiseusersetup.objects.filter(project_id=projectInstance)
	objsprofile = Project.objects.all()
	return render(request, 'getin.html', locals())

#Project Wise User Setup
@csrf_exempt
def setUserInDB(request):
	adminid = request.session['loggedinuserid']
	adminname = userprofile.objects.get(pk=adminid)
	if request.method=="POST":
		if request.POST.get('pname','u_id'):
			pname = request.POST.get('pname')
			u_id = request.POST.get('u_id')
			user = userprofile.objects.get(pk=u_id)
			pid = Project.objects.get(title=pname)
		else:
			u_id = None
			pname = None

		if request.POST.get('db_id','chkbox'):
			db_id = request.POST.get('db_id')
			db = Db_profile.objects.get(pk=db_id)
			chkbox = request.POST.get('chkbox')
		else:
			db_id = None
			chkbox = None

	try:
		projectuser = Projectwiseusersetup.objects.get(userid_id = user.pk, project_id_id = pid.pk)
	except Projectwiseusersetup.DoesNotExist:
	    projectuser= None

	if projectuser:
		return HttpResponse ('Data already exist!!!:-:1')
	else:
		try:
			obj = Projectwiseusersetup.objects.get(userid=user,setasdefaultproject = True)
		except Projectwiseusersetup.DoesNotExist:
			obj= None

		if obj:

			if chkbox == "True":
				obj.setasdefaultproject = False;
				obj.save();
				projectWiseInstance = Projectwiseusersetup()
				projectWiseInstance.project_id_id = pid.pk
				projectWiseInstance.setasdefaultproject = chkbox
				projectWiseInstance.userid_id = user.id
				projectWiseInstance.db_profileid_id = db.pk
				projectWiseInstance.save();

			else:
				projectWiseInstance = Projectwiseusersetup()
				projectWiseInstance.project_id_id = pid.pk
				projectWiseInstance.setasdefaultproject = chkbox
				projectWiseInstance.userid_id = user.id
				projectWiseInstance.db_profileid_id = db.pk
				projectWiseInstance.save();


		else:
			projectWiseInstance = Projectwiseusersetup();
			projectWiseInstance.project_id_id = pid.pk
			projectWiseInstance.setasdefaultproject = True
			projectWiseInstance.userid_id = user.id
			projectWiseInstance.db_profileid_id = db.pk
			projectWiseInstance.save();
		return HttpResponse ('Added Successfully:-:0')

	return render(request, 'projectindex.html')


#Edit Project Wise User Setup
@myadmin_login_required
def editUserInDB(request,transactionid):
	loggedinuserid = request.session['loggedinuserid']
	users = userprofile.objects.filter(adminuserid=loggedinuserid)
	recvid = Projectwiseusersetup.objects.get(pk=transactionid)
	form = ProjectwiseusersetupForm(instance=recvid)
	form.fields["userid"].queryset = userprofile.objects.filter(adminuserid=loggedinuserid)
	return render(request,'edit.html', locals())

#Save the Edited Pojectwiseusersetup data
@csrf_exempt
def saveUserInDB(request):
	a=False
	#print "box val %s " % (request.POST)
	if request.method=="POST":
		if request.POST.get('tableid','userid'):
			tid = request.POST.get('tableid')
			uid = request.POST.get('userid')
			user = userprofile.objects.get(pk=uid)
		if request.POST.get('db_profileid','project_id'):
			dbid= request.POST.get('db_profileid')
			db = Db_profile.objects.get(pk=dbid)
			pname = request.POST.get('project_id')
			pid = Project.objects.get(title=pname)
		if request.POST.get('setasdefaultproject'):
			boxval = request.POST.get('setasdefaultproject')

			if boxval:
				a = True
			else:
				a = False
		try:
			tabid = Projectwiseusersetup.objects.get(pk=tid)
			#print "exist table %s" % (tabid.project_id_id)
		except Projectwiseusersetup.DoesNotExist:
			tabid = None

		try:
			projectuser = Projectwiseusersetup.objects.get(userid_id = user.pk, project_id_id = pid.pk)
			#print "already u with p %s" % (projectuser.pk)
		except Projectwiseusersetup.DoesNotExist:
			projectuser = None

		try:
			obj1 = Projectwiseusersetup.objects.get(userid=user,setasdefaultproject = True)
			#print "setdefault already %s" % (obj1.pk)
		except Projectwiseusersetup.DoesNotExist:
			obj1 = None

		if projectuser:
			if projectuser == tabid:
				if projectuser.setasdefaultproject == a and projectuser.db_profileid_id == db.pk :
					return HttpResponse ('You didnt change anything!!:-:2')

				elif projectuser.setasdefaultproject == a and projectuser.db_profileid_id != db.pk :
					tabid.db_profileid_id = db.pk
					tabid.save();
					return HttpResponse ("Edited Sucessfully:-:0")

				elif projectuser.setasdefaultproject != a and projectuser.db_profileid_id == db.pk :
					if obj1:
						if a == True:
							obj1.setasdefaultproject = False;
							obj1.save();
							tabid.setasdefaultproject = a
							tabid.save();
							return HttpResponse ("Edited Sucessfully:-:0")
						else:
							if tabid == obj1:
								return HttpResponse ("You can't do this:-:2")
					else:
						tabid.setasdefaultproject = True;
						tabid.save();
						return HttpResponse ("Edited Sucessfully:-:0")

				else:
					if obj1:
						if a == True:
							obj1.setasdefaultproject = False;
							obj1.save();
							tabid.setasdefaultproject = a
							tabid.db_profileid_id = db.pk
							tabid.save();
							return HttpResponse ("Edited Sucessfully:-:0")
						else:
							if tabid == obj1:
								tabid.db_profileid_id = db.pk
								tabid.save();
								return HttpResponse ('This is default project for user. you cannot make un-default!! Other details are saved successfully:-:2')
					else:
						tabid.setasdefaultproject = True;
						tabid.db_profileid_id = db.pk
						tabid.save();
						return HttpResponse ("Edited Sucessfully:-:0")

			else:
				return HttpResponse ("Same data already exist:-:2")
		else:
			if obj1:
				if a == True:
					obj1.setasdefaultproject = False;
					obj1.save();
					tabid.project_id_id = pid.pk
					tabid.setasdefaultproject = a
					tabid.userid_id = user.id
					tabid.db_profileid_id = db.pk
					tabid.save();
					return HttpResponse ("Edited Sucessfully:-:0")
				else:
					#print "false"
					#print user.id
					tabid.project_id_id = pid.pk
					tabid.setasdefaultproject = a
					tabid.userid_id = user.id
					tabid.db_profileid_id = db.pk
					tabid.save();
					return HttpResponse ("This is default project for user. you cannot make un-default!! Other details are saved successfully:-:2")
			else:
				tabid.project_id_id = pid.pk
				tabid.setasdefaultproject = True
				tabid.userid_id = user.id
				tabid.db_profileid_id = db.pk
				tabid.save();
				return HttpResponse ("This is default project for user. you cannot make un-default!! Other details are saved successfully:-:2")


	return render(request, 'edit.html')

# Delete Project Wise User Setup
@myadmin_login_required
def deleteUserInDB(request, projectwiseusersetupid):
	tabinstance = Projectwiseusersetup.objects.get(pk=projectwiseusersetupid)
	#print tabinstance.project_id_id
	tabinstance.delete();
	return HttpResponseRedirect('/project/getin/%s' % tabinstance.project_id_id)

@csrf_exempt
def createIonic(request,projectid):
	currentProject = Project.objects.get(pk = projectid)
	Ptname = currentProject.slug
	pid = currentProject.id
	cmd = os.popen("pgrep -f ionic").readlines()
	#print cmd
	if not os.path.exists(Ptname):
		if len(cmd) <= 2:
			itype = IonicProjectConfig.objects.create(itype="Blank",project_id_id = pid)
			os.chdir(filePath+"ionicapps")
			os.system("ionic start "+Ptname+" blank")
			try:
				os.chdir(filePath+"ionicapps/"+Ptname+"/")
				os.system("ionic generate provider txservice")
				os.system("ionic generate provider loginservice")
				os.system("ionic generate provider singleton")
				os.system("ionic generate provider expression")
				os.system("ionic generate provider cmservice")
				os.system("ionic generate provider notify")
				os.system("ionic generate provider pagenav")
				os.chdir(filePath)
				return HttpResponse("Ionic Project "+Ptname+" created")
			except:
				os.chdir(filePath)
				return HttpResponseBadRequest("Problem in creation of Ionic App")
		else:
			return HttpResponseBadRequest("Already Ionic Process Running.Please Try Again After Sometime")

	else:
		os.chdir(filePath)
		return HttpResponse("Ionic Project "+Ptname+" already exist")

@csrf_exempt
def ionicPlatform(request,projectid):
	iontype = request.POST.get('itype')
	currentProject = Project.objects.get(pk = projectid)
	Ptname = currentProject.slug
	pid = currentProject.id
	cmd = os.popen("pgrep -f ionic").readlines()
	#print cmd
	try:
		if len(cmd) <= 2:
			os.chdir(filePath+"ionicapps/"+Ptname+"/")
			if not os.path.exists(filePath+"ionicapps/"+Ptname+"/platforms/"):
				os.system("ionic cordova platform add "+iontype)
				os.chdir(filePath)
				return HttpResponse("Platform "+iontype+" added to project "+Ptname)
			elif os.path.exists(filePath+"ionicapps/"+Ptname+"/platforms/"+iontype+"/"):
				return HttpResponse("Platform "+iontype+" already exist")
			else:
				os.system("ionic cordova platform add "+iontype)
				os.chdir(filePath)
				return HttpResponse("Platform "+iontype+" added to project "+Ptname)

		else:
			return HttpResponseBadRequest("Already Ionic Process Running.Please Try Again After Sometime")
	except Exception as e:
		print e
		return HttpResponseBadRequest("Error In Installing Platform")


@csrf_exempt
def ionicPlugin(request,projectid):
	mylist = ["sqlite","porter","newtork","file","transfer","toast","status","locnot","scan","camera","imagepicker","filechooser","filepath","base64","SpeechRecognition","onesignal","razorpay","htmltopdf","diagnostic","imei","androidpermission"]

	iontype = request.POST.get('itype')
	currentProject = Project.objects.get(pk = projectid)
	Ptname = currentProject.slug
	pid = currentProject.id
	cmd = os.popen("pgrep -f ionic").readlines()
	start = 'default plugins\n'
	end = 'default end'
	with open(filePath+"static/ionicsrc/plugin/defaultplugin.json") as data_file:
		data = json.load(data_file)
		#print data['plugins']['sqlite']
		try:
			if len(cmd) <= 2:
				os.chdir(filePath+"ionicapps/"+Ptname+"/")
				for lists in mylist:
					os.system(data['plugins'][lists]['plugin'])
					if data['plugins'][lists]['npm'] != "":
						os.system(data['plugins'][lists]['npm'])

				appinclude = appincludeTs(filePath,Ptname,start,end)
				provider = includeProv(filePath,Ptname,start,end)
				module = includemodule(filePath,Ptname)
				payment = paymentgateway(filePath,Ptname)
				os.chdir(filePath)
				return HttpResponse("Default Plugin Installed")
			else:
				return HttpResponseBadRequest("Already Ionic Process Running.Please Try Again After Sometime")

		except Exception as e:
			print e
			os.chdir(filePath)
			return HttpResponseBadRequest("Error In Installing Plugin")

def appincludeTs(filePath,Ptname,start,end):
	with open(filePath+"ionicapps/"+Ptname+"/src/app/app.module.ts") as f:
		lines = f.readlines()
		imp = lines.index("import { SplashScreen } from '@ionic-native/splash-screen';\n")

		with open(filePath+"static/ionicsrc/plugin/import.txt") as f:
				imports = f.readlines()
				start = imports.index(start)
				try:
					end = imports.index(end+'\n')
				except:
					end = imports.index(end)

				for i in range(start+1,end):
					try:
						if lines.index(imports[i]):
							i = lines.index(imports[i])
					except:
						lines.insert(imp+1,imports[i])



	with open(filePath+"ionicapps/"+Ptname+"/src/app/app.module.ts","w") as file:
		for tslines in lines:
			file.write(tslines)

	return lines

def includeProv(filePath,Ptname,start,end):
	with open(filePath+"ionicapps/"+Ptname+"/src/app/app.module.ts") as f:
		lines = f.readlines()
		app_prov = lines.index('    SplashScreen,\n')

		with open(filePath+"static/ionicsrc/plugin/provider.txt") as f1:
					prov = f1.readlines()
					start = prov.index(start)
					try:
						end = prov.index(end+'\n')
					except:
						end = prov.index(end)

					for i in range(start+1,end):
						try:
							if lines.index(prov[i]):
								i = lines.index(prov[i])

						except:
							lines.insert(app_prov+1,prov[i])

	with open(filePath+"ionicapps/"+Ptname+"/src/app/app.module.ts","w") as file:
		for tslines in lines:
			file.write(tslines)

	return lines


def includemodule(filePath,Ptname):
	with open(filePath+"ionicapps/"+Ptname+"/src/app/app.module.ts") as f:
		lines = f.readlines()
		module = lines.index('    BrowserModule,\n')

		with open(filePath+"static/ionicsrc/plugin/module.txt") as f2:
				mod = f2.readlines()
				print mod
				mod.remove('end')
				for modimp in mod:
					try:
						if lines.index(modimp):
							i = lines.index(modimp)

					except:
						lines.insert(module+1,modimp)

	with open(filePath+"ionicapps/"+Ptname+"/src/app/app.module.ts","w") as file:
		for tslines in lines:
			file.write(tslines)

	return lines

def paymentgateway(filePath,Ptname):
	try:
		razorpay_declaration = ["declare module '*';\n", '\n', 'declare var RazorpayCheckout: any;\n']

		with open(filePath+"ionicapps/"+Ptname+"/src/declarations.d.ts","w") as file:
			for lines in razorpay_declaration:
				file.write(lines)

		with open(filePath+"ionicapps/"+Ptname+"/config.xml") as f:
			lines = f.readlines()
			sdk_version = lines.index('    <preference name="android-minSdkVersion" value="16" />\n')
			lines.insert(sdk_version+1,'    <preference name="android-minSdkVersion" value="19" />\n')
			lines.remove('    <preference name="android-minSdkVersion" value="16" />\n')

		with open(filePath+"ionicapps/"+Ptname+"/config.xml","w") as file:
			for tslines in lines:
				file.write(tslines)
	except Exception as e:
		print "razor_pay"
		print e


def alreadyIonic(request,projectid):
	currentProject = Project.objects.get(id = projectid)
	Ptname = currentProject.slug
	os.chdir(filePath+"ionicapps/")
	if os.path.exists(Ptname+"/src/index.html"):
		if os.path.exists(Ptname+"/platforms"):
				return HttpResponse("Platform exist")
		else:
			return HttpResponse("exist")
	else:
		return HttpResponse("not exist")


@myadmin_login_required
def ionicProject(request,projectid):
	adminid = request.session['loggedinuserid']
	adminname = userprofile.objects.get(pk=adminid)
	projectselect = Project.objects.filter(admin_id_id =adminid)
	projectInstance = Project.objects.get(id = projectid)
	currentProject = projectInstance.id
	ptitle = projectInstance.title
	slug = projectInstance.slug
	SMSAttributesFormSet = modelformset_factory(SMSAttributes,form = SMSAttributesForm,can_delete=True,extra=1,can_order=True)
	try:
		query = IonicServices.objects.get(project_id_id = projectid)
		form = IonicServicesForm(instance = query)
	except:
		form = IonicServicesForm()

	try:
		notify = IonicNotification.objects.get(project_id_id = projectid)
		nform = IonicNotificationForm(instance = notify)
	except:
		nform = IonicNotificationForm()


	try:
		sms = SMSServer.objects.get(projectid_id = projectid)
		smsAttr = SMSAttributes.objects.filter(smsserver_id=sms.id)
		smsform =  SMSServerForm(instance = sms)
		formset = SMSAttributesFormSet(queryset=smsAttr)
	except:
		smsform = SMSServerForm()
		formset = SMSAttributesFormSet(queryset=SMSAttributes.objects.none())

	try:
		emailObj = EmailConfiguration.objects.get(project_id_id = projectid)
		eform = EmailConfigurationForm(instance=emailObj)
	except:
		eform = EmailConfigurationForm()

	try:
		googleAPISetupObj = GoogleAPISetup.objects.get(project_id_id = projectid)
		gform = GoogleAPISetupForm(instance=googleAPISetupObj)
	except Exception as e:
		print e
		gform = GoogleAPISetupForm()

	location = GeolocationSetup.objects.filter(project_id_id = projectid)
	if location:
		location_value = GeolocationSetup.objects.get(project_id_id = projectid)
		loc_form = GeolocationSetupForm(instance = location_value)
	else:
		loc_form = GeolocationSetupForm()


	if os.path.exists(filePath+"ionicapps/"+slug+"/package.json"):
		with open(filePath+"ionicapps/"+slug+"/package.json") as f:
			summary = f.readlines()
	else:
		data ="No Package Json Found"


	return render(request, 'ionicprojectcreation.html', locals())

@csrf_exempt
def ionicService(request,projectid):
	try:
		service = IonicServices.objects.filter(project_id_id = projectid)
		if service:
			query = IonicServices.objects.get(project_id_id = projectid)
			serviceform = IonicServicesForm(request.POST,instance = query)
			editform = serviceform.save(commit = False)
			editform.serviceurl = editform.protocol+editform.host+":"+editform.port+"/"+editform.context+"/"
			editform.save()
		else:
			serviceform = IonicServicesForm(request.POST)
			if serviceform.is_valid():
				newform = serviceform.save(commit = False)
				newform.serviceurl = newform.protocol+newform.host+":"+newform.port+"/"+newform.context+"/"
				newform.project_id_id = projectid
				newform.save()
		return HttpResponse("success")
	except Exception as e:
		print e
		return HttpResponseBadRequest("error")

@csrf_exempt
def geolocation(request,projectid):
	try:
		service = GeolocationSetup.objects.filter(project_id_id = projectid)
		if service:
			location = GeolocationSetup.objects.get(project_id_id = projectid)
			serviceform = GeolocationSetupForm(request.POST or None,instance = location)
		else:
			serviceform = GeolocationSetupForm(request.POST or None)

		if serviceform.is_valid():
			newform = serviceform.save(commit = False)
			newform.project_id_id = projectid
			newform.save()
			return HttpResponse("success")
		else:
			return HttpResponseBadRequest("error")
	except Exception as e:
		print e
		return HttpResponseBadRequest("error")
@csrf_exempt
def geolocationplugins(request,projectid):
	print "geolocationplugins"
	mylist = ["native","geolocation","backgroundgeo"]
	currentProject = Project.objects.get(pk = projectid)
	Ptname = currentProject.slug
	pid = currentProject.id
	cmd = os.popen("pgrep -f ionic").readlines()
	with open(filePath+"static/ionicsrc/plugin/defaultplugin.json") as data_file:
		data = json.load(data_file)
		#print data['plugins']['sqlite']
		try:
			if len(cmd) <= 2:
				os.chdir(filePath+"ionicapps/"+Ptname+"/")
				for lists in mylist:
					os.system(data['plugins'][lists]['plugin'])
					if data['plugins'][lists]['npm'] != "":
						os.system(data['plugins'][lists]['npm'])

				start ='geolocation plugins\n'
				end ='geolocation end'
				appinclude = appincludeTs(filePath,Ptname,start,end)
				provider = includeProv(filePath,Ptname,start,end)
			return HttpResponse('success')
		except Exception as e:
			print e
			return HttpResponseBadRequest('error')


@csrf_exempt
def ionicNotify(request,projectid):
	try:
		notify = IonicNotification.objects.filter(project_id_id = projectid)
		if notify:
			query = IonicNotification.objects.get(project_id_id = projectid)
			notifyform = IonicNotificationForm(request.POST,instance = query)
			editform = notifyform.save(commit = False)
			editform.save()
		else:
			notifyform = IonicNotificationForm(request.POST)
			if notifyform.is_valid():
				newform = notifyform.save(commit = False)
				newform.project_id_id = projectid
				newform.save()
		return HttpResponse("success")
	except Exception as e:
		print e
		return HttpResponseBadRequest("error")

@csrf_exempt
def ionicSMSSave(request,projectid):
	userid = request.session['userid']
	print "USERID",userid
	SMSAttributesFormSet = modelformset_factory(SMSAttributes,form = SMSAttributesForm,can_delete=True)
	smsServerId  = ""
	try:
		sms = SMSServer.objects.get(projectid_id = projectid)
	except Exception as e:
		sms = None
	
	if sms:
		smsServerId = sms.id
		smsform = SMSServerForm(request.POST,instance = sms)

		if smsform.is_valid():
			sFrom = smsform.save(commit=False)
			if sms.db_status != "new":
				sFrom.db_status = "edited"
			sFrom.save()

			formsets = SMSAttributesFormSet(data=request.POST)
			
			for form in formsets:
				if form.is_valid() and form.cleaned_data.get('DELETE') and form.instance.pk:
					print "************DELETE*******************"
					print form.instance.pk
					form.instance.delete()
				elif form.is_valid() and form.cleaned_data:
					print "************VALID*********************"
					smsAttr = form.save(commit=False)
					smsAttr.smsserver = SMSServer.objects.get(id=sms.id)
					smsAttr.save()
					print smsAttr.id
				else:
					print "*****FORMSET ERRORS*******"
					print form.cleaned_data
					print form.errors
		else:
			print smsform.errors
			return HttpResponseBadRequest("error")
	
	else:
		smsform = SMSServerForm(request.POST)
		if smsform.is_valid():
			sms = smsform.save(commit=False)
			sms.db_status = 'new'
			sms.save()
			smsServerId = sms.id
	
			formsets = SMSAttributesFormSet(data=request.POST)
			for form in formsets:

				if form.is_valid() and form.cleaned_data.get('DELETE') and form.instance.pk:
					print "************DELETE*******************"
					print form.instance.pk
					form.instance.delete()
				elif form.is_valid() and form.cleaned_data:
					print "************VALID*********************"
					smsAttr = form.save(commit=False)
					smsAttr.smsserver = SMSServer.objects.get(id=smsServerId )
					smsAttr.save()
				else:
					print "*****FORMSET ERRORS*******"
					print form.errors
		else:
			print smsform.errors
			return HttpResponseBadRequest("error")
		
		
	query = SMSAttributes.objects.filter(smsserver_id=smsServerId)
	formset = SMSAttributesFormSet(queryset=query)	
	hh = update_sms_setup(request,userid,projectid)
	return render(request,'smsAttrTable.html',locals())

@csrf_exempt
def googleAPISetup(request,projectid):
	try:
		try:
			apisetup = GoogleAPISetup.objects.get(project_id_id = projectid)
			apisetupform = GoogleAPISetupForm(request.POST,instance = apisetup)
		except GoogleAPISetup.DoesNotExist:
			apisetup = None
			apisetupform = GoogleAPISetupForm(request.POST)
		
		if apisetupform.is_valid():
			newform = apisetupform.save(commit = False)
			newform.project_id_id = projectid
			newform.save()
		return HttpResponse("success")
	except Exception as e:
		print e
		return HttpResponseBadRequest("error")
	

@csrf_exempt
def emailConfig(request,projectid):
	userid = request.session['userid']
	try:
		email = EmailConfiguration.objects.get(project_id_id = projectid)
	except EmailConfiguration.DoesNotExist:
		email = None
	
	if email:
		
		eform = EmailConfigurationForm(request.POST,instance = email)
		newemailform = eform.save(commit=False)
		if email.db_status != "new":
			newemailform.db_status = "edited"
		newemailform.save()
	else:
		eform = EmailConfigurationForm(request.POST)
		if eform.is_valid():
			newform = eform.save(commit = False)
			newform.project_id_id = projectid
			newform.db_status = "new"
			newform.save()
	
	update_email_setup(request,userid,projectid)
	return HttpResponse("success")
	# except Exception as e:
	# 	print e
	# 	return HttpResponseBadRequest("error")			


@myadmin_login_required
def ionicBuild(request,projectid):
	adminid = request.session['loggedinuserid']
	adminname = userprofile.objects.get(pk=adminid)
	projectselect = Project.objects.filter(admin_id_id =adminid)
	projectInstance = Project.objects.get(id = projectid)
	currentProject = projectInstance.id
	ptitle = projectInstance.title
	return render(request, 'ionicbuild.html', locals())

@csrf_exempt
def ionicPages(request,projectid):
	projectInstance = Project.objects.get(id = projectid)
	currentProjectid = projectInstance.id
	Ptname = projectInstance.slug
	try:
		lpage = Login.objects.filter(project_id_id = projectid)
		if lpage:
			try:
				login = generateLoginpage(currentProjectid)
			except Exception as e:
				raise Exception("Login Page Configuration Error!Please Check.")

		hpage = Homepage.objects.filter(project_id_id = projectid)
		search = searchModal(Ptname,projectid)
		if hpage:
			homepage = homehtml(currentProjectid)
			home = Homepage.objects.get(project_id_id = currentProjectid)
			menu = Menu.objects.filter(homepageid = home.id ,createpage = True)

		try:
			provider = providerpages(Ptname,projectInstance,lpage)
			theme = customtheme(Ptname,projectid)
			extjs = externalJs(Ptname)
			root = rootPage(Ptname,projectid)
			notify = notification(Ptname,projectid)
			event = eventJson(Ptname,projectid)
			for lists in menu:
				if lists.typeofview == "transactionview":
					pages = pagemeta(lists.transactionview_id,Ptname)
				elif lists.typeofview == "reportview":
					pages = reppagemeta(lists.reportview_id,Ptname)
				

		except Exception as e:
			raise e

		try:
			lpage = Login.objects.filter(project_id_id = projectid)
			if lpage:
				sync = syncmasteradd(Ptname,projectid,home)
				sqlite = dbtosql(Ptname,projectid)
				
		except Exception as e:
			raise e

		return HttpResponse("Success!.Ready For Build.")
	except Exception as e:
		print e
		return HttpResponse(e)
		


def providerpages(ptitle,project,login):
	try:
		location = GeolocationSetup.objects.filter(project_id_id = project.id)
		myprovider = ["txservice","loginservice","singleton","expression","cmservice","notify","pagenav","location"]

		for prov in myprovider:
			file = prov
			if prov == 'location':
				if location:
					pass
				else:
					file = prov+"_nr"

			with open(filePath+"static/ionicsrc/providers/"+prov+"/"+file+".ts") as f:
				with open(filePath+"ionicapps/"+ptitle+"/src/providers/"+prov+"/"+prov+".ts", "w") as f1:
					for line in f:
						f1.write(line)
	except Exception as e:
		raise Exception("Providers Not Created Properly!.Please Check.")

	try:
		singlepr = singleton(ptitle,project)
		pagnav = pagenav(ptitle,project,login)
	except Exception as e:
		raise e
    	
	return line

def singleton(ptitle,project):
	with open(filePath+"static/ionicsrc/providers/singleton/singleton.ts") as pro:
		lines = pro.readlines()
	try:
		con = lines.index('export class SingletonProvider {\n')
		service = IonicServices.objects.get(project_id_id = project.id)
		
		lines.insert(con+1,'  public PID = "";\n')
		lines.insert(con+2,'  public userid = "";\n')
		lines.insert(con+3,'  public resturl = "'+str(service.serviceurl)+'";\n')
		lines.insert(con+4,'  public dynamicresturl = "";\n')
		lines.insert(con+5,'  public projectname = "'+str(project.slug)+'";\n')
		lines.insert(con+6,'  public ismultitenant = "'+str(project.ismultitenant)+'";\n')
		lines.insert(con+7,'  public table_underscore = "'+str(project.table_append_by_underscore)+'";\n')
		lines.insert(con+8,'  public imei_based_login = "'+str(project.imei_based_login)+'";\n')
		lines.insert(con+9,'  public role = "";\n')
		try:
			notify = IonicNotification.objects.get(project_id_id = project.id)
			lines.insert(con+10,'  public apikey = "'+notify.apikey+'";\n')
			lines.insert(con+11,'  public senderid = "'+notify.senderid+'";\n')
		except Exception as e:
			lines.insert(con+10,'  public apikey = "";\n')
			lines.insert(con+11,'  public senderid = "";\n')
			print e
		
		try:
			googleSetup = GoogleAPISetup.objects.get(project_id_id = project.id)
			lines.insert(con+12,'  public googleapikey = "'+googleSetup.apikey+'";\n')
			lines.insert(con+13,'  public googleclientid = "'+googleSetup.clientid+'";\n')
		except Exception as e:
			lines.insert(con+12,'  public googleapikey = "";\n')
			lines.insert(con+13,'  public googleclientid = "";\n')
        try:
			location = GeolocationSetup.objects.get(project_id_id = project.id)
			lines.insert(con+12,'  public tracking = "'+location.tracking+'";\n')
			lines.insert(con+13,'  public trackInterval = "'+location.time_interval+'";\n')
		except Exception as e:
			lines.insert(con+12,'  public tracking = "false";\n')
			lines.insert(con+13,'  public trackInterval = "";\n')
			print e

	except Exception as e:
		print e
		raise Exception('Ionic Service Setup Error!Please Check.')


	with open(filePath+"ionicapps/"+ptitle+"/src/providers/singleton/singleton.ts","w") as file:
		for tslines in lines:
			file.write(tslines)

	return "success"

def pagenav(ptitle,project,login):
	with open(filePath+"static/ionicsrc/providers/pagenav/pagenav.ts") as f:
		pagenav_lines = f.readlines()

	nav = pagenav_lines.index("import { Injectable } from '@angular/core';\n")
	index = pagenav_lines.index('export class PagenavProvider {\n')
	pagenav_lines.insert(index+1,"      public pages = [\n")
	pagenav_lines.insert(index+2,"      ];\n")

	home = Homepage.objects.filter(project_id_id = project.id)
	homemenu_serializer = HomepageSerializer(instance=home,many=True)
	home = homemenu_serializer.data[0]

	for menu in home['home_menu']:
		title =""
		title = menu['title'].lower()
		if menu['typeofview'] == 'transactionview':
			pagetitle = menu['transactionview'].lower().replace(" ","")
		elif menu['typeofview'] == 'reportview':
			pagetitle = menu['reportview'].lower().replace(" ","")

		pagenav_lines.insert(nav+1, "import { "+pagetitle.capitalize()+"Page } from '../../pages/"+pagetitle+"/"+pagetitle+"';\n")
		page = pagenav_lines.index("      public pages = [\n")
		pagenav_lines.insert(page+1,"      { id :'"+pagetitle+"',component: "+pagetitle.capitalize()+"Page},\n")

	if home['menutype'] == 'grid':
		pagenav_lines.insert(nav+1, "import { GridPage } from '../../pages/grid/grid';\n")
		page = pagenav_lines.index("      public pages = [\n")
		pagenav_lines.insert(page+1,"      { id :'menupage',component: GridPage},\n")
	else:
		pagenav_lines.insert(nav+1, "import { SidemenuPage } from '../../pages/sidemenu/sidemenu';\n")
		page = pagenav_lines.index("      public pages = [\n")
		pagenav_lines.insert(page+1,"      { id :'menupage',component: SidemenuPage},\n")

	if login:
		pagenav_lines.insert(nav+1, "import { LoginPage } from '../../pages/login/login';\n")
		page = pagenav_lines.index("      public pages = [\n")
		pagenav_lines.insert(page+1,"      { id :'login',component: LoginPage},\n")


	with open(filePath+"ionicapps/"+ptitle+"/src/providers/pagenav/pagenav.ts", "w") as f1:
		for gline in pagenav_lines:
			f1.write(gline)



	return "success"



def externalJs(ptitle):
	if not os.path.exists(filePath+"ionicapps/"+ptitle+"/src/assets/js"):
		os.makedirs(filePath+"ionicapps/"+ptitle+"/src/assets/js")

	with open(filePath+"static/ionicsrc/js/expr.js") as f:
		with open(filePath+"ionicapps/"+ptitle+"/src/assets/js/expr.js", "w") as f1:
			for line in f:
				f1.write(line)

	with open(filePath+"static/ionicsrc/js/mustache.js") as f2:
		with open(filePath+"ionicapps/"+ptitle+"/src/assets/js/mustache.js", "w") as f3:
			for line in f2:
				f3.write(line)

	with open(filePath+"ionicapps/"+ptitle+"/src/index.html") as ind:
		lines = ind.readlines()	

	scrpit = lines.index('</head>\n',)
	
	try:
		exprIndexNo = lines.index('  <script src="assets/js/expr.js" type="text/javascript"></script>\n') 
	except:
		lines.insert(scrpit-1, '  <script src="assets/js/expr.js" type="text/javascript"></script>\n')
	
	try:
		mustacheIndexNo = lines.index('  <script src="assets/js/mustache.js" type="text/javascript"></script>\n')
	except:
		lines.insert(scrpit-1, '  <script src="assets/js/mustache.js" type="text/javascript"></script>\n')		
	
	try:
		googleIndexNo = lines.index('  <script src="https://apis.google.com/js/client.js"></script>\n')
	except:		
		lines.insert(scrpit-1, '  <script src="https://apis.google.com/js/client.js"></script>\n')		


	with open(filePath+"ionicapps/"+ptitle+"/src/index.html","w") as file:
		for tslines in lines:
			file.write(tslines)			

	return "success"		


def rootPage(ptitle,pid):
	try:
		login = Login.objects.get(project_id_id = pid)
		if login:
			appcomp = rootinclude(ptitle,"login")

	except Exception as e:
		print e
		home = Homepage.objects.filter(project_id_id = pid)
		if home:
			appcomp = rootinclude(ptitle,home[0].menutype)
		else:
			print "no login,no home"

def rootinclude(ptitle,fileName):
	with open(filePath+"ionicapps/"+ptitle+"/src/app/app.component.ts", "r") as file :
		filedata = file.read()

	# Replace the target string
	#filedata = filedata.replace('page-transaction', 'page-'+fileName)
	#filedata = filedata.replace('transaction.html', fileName+'.html')
	filedata = filedata.replace('HomePage', fileName.capitalize()+'Page')
	filedata = filedata.replace('home', fileName)
	# Write the file out again
	with open(filePath+"ionicapps/"+ptitle+"/src/app/app.component.ts", "w") as file:
		file.write(filedata)
	return "success"


@csrf_exempt
def ionicapk(request,projectid):
	projectInstance = Project.objects.get(id = projectid)
	currentProjectid = projectInstance.id
	Ptname = projectInstance.slug
	os.chdir(filePath+"/ionicapps/"+Ptname+"/")
	try:
		os.system("ionic cordova build --prod android")
		return HttpResponse("success")
		
	except Exception as e:	
		print e
		return HttpResponse("failure")


def apkdownload(request,projectid):
	try:
		projectInstance = Project.objects.get(id = projectid)
		currentProjectid = projectInstance.id
		Ptname = projectInstance.slug
		filenames = [filePath+"ionicapps/"+Ptname+"/platforms/android/app/build/outputs/apk/debug/app-debug.apk"]
		# Folder name in ZIP archive which contains the above files
		# E.g [thearchive.zip]/somefiles/file2.txt
		# FIXME: Set this to something better
		zip_subdir = "apk"
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
	except Exception as e:
		print e
		return HttpResponseBadRequest("Error In Building app")


@csrf_exempt
def theming(request,projectid):
	adminid = request.session['loggedinuserid']
	adminname = userprofile.objects.get(pk=adminid)
	projectselect = Project.objects.filter(admin_id_id =adminid)
	projectInstance = Project.objects.get(id = projectid)
	currentProject = projectInstance.id
	ptitle = projectInstance.slug
	primary = projectInstance.prmcolor
	secondary = projectInstance.seccolor
	dark = projectInstance.dark
	font = IonicFonts.objects.filter(project_id_id = projectid)
	print "font"
	print font
	if font:
		font_name = font[0].fontname
		font_file = font[0].fontfile
	if request.POST:
		if request.POST.get('prm'):
			projectInstance.prmcolor = request.POST.get('prm')
			projectInstance.seccolor = request.POST.get('sec')
			projectInstance.dark = request.POST.get('dark')
			projectInstance.save()
			return HttpResponse("success")
		else:
			return HttpResponse("failure")
	else:
		return render(request, 'ionictheme.html', locals())

def customtheme(ptitle,projectid):
	project = Project.objects.get(id = projectid)
	try:
		with open(filePath+"ionicapps/"+ptitle+"/src/theme/variables.scss") as file :
			lines = file.readlines()

		theme = lines.index('$colors: (\n')
		del lines[theme+5]
		del lines[theme+1]
		del lines[theme+1]
		lines.insert(theme+1,'  primary:    '+project.prmcolor+',\n')
		lines.insert(theme+2,'  secondary:  '+project.seccolor+',\n',)
		lines.insert(theme+5,'  dark:       '+project.dark+',\n',)

		font = IonicFonts.objects.filter(project_id_id = projectid)
		if font:
			try:
				font_delete = lines.index('  @font-face{\r\n')
				for index in range(8):
					del lines[font_delete]
			except Exception as e:
				pass
			fontfilename = font[0].fontname
			fontfile = font[0].fontfile

			with open(filePath+"/"+str(fontfile), "r") as file1 :
				filedata1 = file1.read()

			if not os.path.exists(filePath+"ionicapps/"+ptitle+"/src/assets/fonts"):
				os.makedirs(filePath+"ionicapps/"+ptitle+"/src/assets/fonts")

			with open(filePath+"ionicapps/"+ptitle+"/src/assets/fonts/"+fontfilename+".woff2", "w") as file:
				file.write(filedata1)

			font = lines.index('$font-path: "../assets/fonts";\n')
			lines.insert(font+1,'  @font-face{\r\n')
			lines.insert(font+2,'font-family: '+fontfilename+';\r\n')
			lines.insert(font+3,"src: url('../assets/fonts/"+fontfilename+".woff2') format('woff2');\r\n")
			lines.insert(font+4,'}\r\n')
			lines.insert(font+5,' \r\n')
			lines.insert(font+6,'*{\r\n')
			lines.insert(font+7,'font-family: '+fontfilename+';\r\n')
			lines.insert(font+8,'}\r\n')
		else:
			try:
				font_delete = lines.index('  @font-face{\r\n')
				for index in range(8):
					del lines[font_delete]
			except Exception as e:
				pass


		with open(filePath+"ionicapps/"+ptitle+"/src/theme/variables.scss", "w") as f1:
			for gline in lines:
				f1.write(gline)

		return "success"
	except Exception as e:
		print e

def ionicsplash(request,projectid):
	adminid = request.session['loggedinuserid']
	adminname = userprofile.objects.get(pk=adminid)
	projectselect = Project.objects.filter(admin_id_id =adminid)
	projectInstance = Project.objects.get(id = projectid)
	currentProject = projectInstance.id
	ptitle = projectInstance.slug
	primary = projectInstance.prmcolor
	secondary = projectInstance.seccolor
	fonts = IonicFonts.objects.filter(project_id_id = projectid)
	print fonts
	if fonts:
		font_name = fonts[0].fontname
	try:
		image = IonicImages.objects.get(project_id_id = projectid)
	
		if image:
			if request.method == 'POST':
				form = IonicImagesForm(request.POST,request.FILES,instance=image)
				if form.is_valid():
					
					image = form.save(commit = False)
					image.save()
					messages.add_message(request, messages.SUCCESS, 'File Uploaded Sucessfully.')
				
			else:
				messages.add_message(request, messages.SUCCESS, 'File Uploaded Failed.')
				

	except Exception as e:
		print e	
		if request.method == "POST":
			form = IonicImagesForm(request.POST,request.FILES)
		
			if form.is_valid():
				splash = form.save(commit = False)
				splash.project_id_id = projectid
				splash.save()
				messages.add_message(request, messages.SUCCESS, 'File Uploaded Sucessfully.')
			else:
				form = IonicImagesForm()

	return render(request, 'ionictheme.html', locals())

def fontfile(request,projectid):
		adminid = request.session['loggedinuserid']
		adminname = userprofile.objects.get(pk=adminid)
		projectselect = Project.objects.filter(admin_id_id =adminid)
		projectInstance = Project.objects.get(id = projectid)
		currentProject = projectInstance.id
		ptitle = projectInstance.slug
		primary = projectInstance.prmcolor
		secondary = projectInstance.seccolor
		try:
			font = IonicFonts.objects.get(project_id_id = projectid)
			if font:
				form = IonicFontsForm(request.POST,request.FILES,instance=font)

		except Exception as e:
			print e
			form = IonicFontsForm(request.POST,request.FILES )

		print form.errors
		print form.is_valid()
		if form.is_valid():
			if request.FILES:
				print "yes"
				font_file = form.save(commit = False)
				font_file.project_id_id = projectid
				font_file.save()
				messages.add_message(request, messages.SUCCESS, 'File Uploaded Sucessfully.')
				return HttpResponseRedirect('/project/theming/%s' %projectid )
			else:
				messages.add_message(request, messages.WARNING, 'No File To upload.')
				return HttpResponseRedirect('/project/theming/%s' %projectid )
		else:
			form = IonicImagesForm()
			messages.add_message(request, messages.SUCCESS, 'File Uploaded Failed.')
			return HttpResponseRedirect('/project/theming/%s' %projectid )

		return render(request, 'ionictheme.html', locals())

@csrf_exempt
def fontfile_delete(request,projectid):
	try:
		query = IonicFonts.objects.get(project_id_id = projectid)
		query.delete()
		return HttpResponse("success")
	except Exception as e:
		return HttpResponseBadRequest("failure")



@csrf_exempt
def generatesplash(request,projectid):
	projectInstance = Project.objects.get(id = projectid)
	currentProject = projectInstance.id
	ptitle = projectInstance.slug
	try:
		image = IonicImages.objects.get(project_id_id = projectid)
		if image.splashimg:
			with open(filePath+"/"+str(image.splashimg), "r") as file :
				filedata = file.read()

			with open(filePath+"ionicapps/"+ptitle+"/resources/splash.png", "w") as file:
				file.write(filedata)

		if image.iconimg:
			with open(filePath+"/"+str(image.iconimg), "r") as file1 :
				filedata1 = file1.read()

			with open(filePath+"ionicapps/"+ptitle+"/resources/icon.png", "w") as file:
				file.write(filedata1)

		os.chdir(filePath+"ionicapps/"+ptitle+"/")
		os.system("ionic cordova resources android")		
		return HttpResponse("Splash and Icon added successfully")
	except Exception as e:
		print e
		os.system("ionic cordova resources android")
		return HttpResponse("Splash and Icon added successfully")


def dbtosql(ptitle,pid):
	pro = Project.objects.get(id = pid)
	ptitle = pro.slug
	con = sqlite3.connect(filePath+"static/ionicmeta/"+ptitle+"/db/"+ptitle+".db")
	# os.popen("mysqldump -u %s -p%s -h %s --no-data -e --opt -c %s > %s.sql" % ("auvitapp","mysql$","192.168.125.96","crm",filePath+"sample"))
	with open(filePath+"/ionicapps/"+ptitle+"/src/assets/db.sql", 'w') as f:
		for line in con.iterdump():
			f.write('%s\n' % line)

	with open(filePath+"/ionicapps/"+ptitle+"/src/assets/db.sql") as f:
		sqllines = f.readlines()
		sqllines.remove('BEGIN TRANSACTION;\n')
		sqllines.remove('COMMIT;\n')

	with open(filePath+"/ionicapps/"+ptitle+"/src/assets/db.sql", "w") as f1:
		for sline in sqllines:
			f1.write(sline)					

	return "success"

def syncmasteradd(ptitle,pid,home):
	menu = home.menutype
	imp = menu.capitalize()
	if not os.path.exists(filePath+"ionicapps/"+ptitle+"/src/pages/syncmaster"):
		os.makedirs(filePath+"ionicapps/"+ptitle+"/src/pages/syncmaster")

	with open(filePath+"static/ionicsrc/syncmaster/syncmaster.html") as f:
		with open(filePath+"ionicapps/"+ptitle+"/src/pages/syncmaster/syncmaster.html", "w") as f1:
			for line in f:
				f1.write(line)

	with open(filePath+"static/ionicsrc/syncmaster/syncmaster.scss") as scss:
		with open(filePath+"ionicapps/"+ptitle+"/src/pages/syncmaster/syncmaster.scss", "w") as sccs1:
			for line in scss:
				sccs1.write(line)

	with open(filePath+"static/ionicsrc/syncmaster/syncmaster.ts") as ts:
		with open(filePath+"ionicapps/"+ptitle+"/src/pages/syncmaster/syncmaster.ts", "w") as ts1:
			for line in ts:
				ts1.write(line)

	with open(filePath+"ionicapps/"+ptitle+"/src/pages/syncmaster/syncmaster.ts", "r") as file :
		filedata = file.read()

	# Replace the target string
	filedata = filedata.replace('HomePage', imp+'Page')
	filedata = filedata.replace('home', menu)
	# Write the file out again
	with open(filePath+"ionicapps/"+ptitle+"/src/pages/syncmaster/syncmaster.ts", "w") as file:
		file.write(filedata)			

	include = syncappincludeTs("syncmaster",ptitle)
	return "success"											

def syncappincludeTs(fileName,ptitle):
	if fileName == 'popover':
		foldername = "searchmodal"
	else:
		foldername = fileName
	with open(filePath+"ionicapps/"+ptitle+"/src/app/app.module.ts") as sy:
		lines = sy.readlines()
		#print lines
		imp = lines.index("import { HomePage } from '../pages/home/home';\n")
		try:
			if lines.index("import { "+fileName.capitalize()+"Page } from '../pages/"+foldername+"/"+fileName+"';\n"):
				i = lines.index("import { "+fileName.capitalize()+"Page } from '../pages/"+foldername+"/"+fileName+"';\n")

		except:
			lines.insert(imp+1, "import { "+fileName.capitalize()+"Page } from '../pages/"+foldername+"/"+fileName+"';\n")
			dec = lines.index( '  declarations: [\n')
			lines.insert(dec+2, "    "+fileName.capitalize()+"Page,\n")
			ent = lines.index( '  entryComponents: [\n')
			lines.insert(ent+2, "    "+fileName.capitalize()+"Page,\n")
			#print imp 

	with open(filePath+"ionicapps/"+ptitle+"/src/app/app.module.ts","w") as file:
		for tslines in lines:
			file.write(tslines)

	return lines

def notification(ptname,projectid):
	try:
		gInfo = GeneralInfo.objects.get(key = 'notification',project_id_id = projectid)
		notifyvalue = gInfo.value.lower()
	except Exception as e:
		print e
		notifyvalue =""

	if (notifyvalue == "true"):
		if not os.path.exists(filePath+"ionicapps/"+ptname+"/src/pages/notification"):
			os.makedirs(filePath+"ionicapps/"+ptname+"/src/pages/notification")

		with open(filePath+"static/ionicsrc/notification/notification.html") as f:
			with open(filePath+"ionicapps/"+ptname+"/src/pages/notification/notification.html", "w") as f1:
				for line in f:
					f1.write(line)

		with open(filePath+"static/ionicsrc/notification/notification.scss") as scss:
			with open(filePath+"ionicapps/"+ptname+"/src/pages/notification/notification.scss", "w") as sccs1:
				for line in scss:
					sccs1.write(line)

		with open(filePath+"static/ionicsrc/notification/notification.ts") as ts:
			with open(filePath+"ionicapps/"+ptname+"/src/pages/notification/notification.ts", "w") as ts1:
				for line in ts:
					ts1.write(line)

		include = syncappincludeTs("notification",ptname)


		if not os.path.exists(filePath+"static/ionicmeta/"+ptname+"/Notification/notification.json"):
			raise Exception("If You Have Configure Notification, Please give Generate Process")
		else:
			if not os.path.exists(filePath+"ionicapps/"+ptname+"/src/assets/json"):
				os.makedirs(filePath+"ionicapps/"+ptname+"/src/assets/json")

			with open(filePath+"static/ionicmeta/"+ptname+"/Notification/notification.json") as json:
				with open(filePath+"ionicapps/"+ptname+"/src/assets/json/notification.json", "w") as json1:
					for line in json:
						json1.write(line)

			return "success"

def searchModal(ptname,projectid):
	try:
		path = filePath+"ionicapps/"+ptname+"/src"
		src = filePath+"static/ionicsrc/searchmodal"
		if os.path.exists(path+"/pages/searchmodal"):
			shutil.rmtree(path+"/pages/searchmodal", ignore_errors=False, onerror=None)

		shutil.copytree(src, path+"/pages/searchmodal")
		appincludeTs = syncappincludeTs("searchmodal",ptname)
		appincludeTs = syncappincludeTs("popover",ptname)
	except Exception as e:
		raise e

def eventJson(ptname,projectid):
	try:
		eventObj = TxnMappingForEvent.objects.get(project_id = projectid)
	except TxnMappingForEvent.DoesNotExist:
		eventObj = None
	
	if eventObj:
		try:
			if not os.path.exists(filePath+"ionicapps/"+ptname+"/src/assets/json/"):
					os.makedirs(filePath+"ionicapps/"+ptname+"/src/assets/json/")

			with open(filePath+"static/ionicmeta/"+ptname+"/calendareventjson/calendarevent.json") as json:
				with open(filePath+"ionicapps/"+ptname+"/src/assets/json/calendarevent.json", "w") as json1:
					for line in json:
						json1.write(line)
		except Exception as e:
			print e


def resetapp(request,projectid):
	projectselect = Project.objects.get(id =projectid)
	ptitle = projectselect.slug
	path = filePath+"ionicapps/"+ptitle+"/src"
	src = filePath+"static/ionicsrc/reset"
	try:
		shutil.rmtree(path+"/app", ignore_errors=False, onerror=None)
		shutil.rmtree(path+"/pages", ignore_errors=False, onerror=None)
		shutil.rmtree(path+"/assets", ignore_errors=False, onerror=None)
		shutil.copytree(src+"/pages", path+"/pages")
		shutil.copytree(src+"/app", path+"/app")
		shutil.copytree(src+"/assets", path+"/assets")
		start = 'default plugins\n'
		end = 'default end'
		appinclude = appincludeTs(filePath,ptitle,start,end)
		provider = includeProv(filePath,ptitle,start,end)
		module = includemodule(filePath,ptitle)
		external = externalJs(ptitle)
		location = GeolocationSetup.objects.filter(project_id_id = projectid)
		if location:
			start ='geolocation plugins\n'
			end ='geolocation end'
			appinclude = appincludeTs(filePath,ptitle,start,end)
			provider = includeProv(filePath,ptitle,start,end)

		return HttpResponse("App Reseted Successfully")
	except Exception as e:
		print e
		return HttpResponseBadRequest("App Reset Failure")


@csrf_exempt
def deleteapp(request,projectid):
	projectselect = Project.objects.get(id =projectid)
	ptitle = projectselect.slug
	print ptitle
	try:

		if os.path.exists(filePath+"ionicapps/"+ptitle+"/"):
			os.chdir(filePath+"ionicapps/")
			shutil.rmtree(filePath+"/ionicapps/"+ptitle, ignore_errors=False, onerror=None)
			return HttpResponse("success")
		else:
			return HttpResponseBadRequest("Ionic Project not Exist")
	except Exception as e:
		print e
		return HttpResponseBadRequest("error")
