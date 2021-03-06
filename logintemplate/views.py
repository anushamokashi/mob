# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse,HttpResponseBadRequest
#from django.utils.text import slugify
from django.template.defaultfilters import slugify
from slugify import slugify
import re
import json
import os
from django.conf import settings
from django.db.models import Q
import requests
from rolesetup.models import Role


from .models import Login, UserList,GeneralInfo,EditedUsersList,EditedInfo
from .forms import LoginForm,UserListForm,GeneralInfoForm
from .serializers import loginSerializer
from project.models import Project, Projectwiseusersetup
from authentication.models import userprofile
from django.views.decorators.csrf import csrf_exempt
from Mobilebuilder.decorators import myuser_login_required
from .update_user_in_db import update_user_and_generalinfo 
import json
import os
from transaction.models import Transaction
from transactionview.models import Transactionview
from transactionview.serializers import ViewtreeSerializer
from transactionview.views import lists,ionicmetaJson
#from django.db.models import Q
filePath = settings.MEDIA_ROOT

# Create your views here.
@myuser_login_required
def loginindex(request):
	pid = Project.objects.get(pk=request.session['projectid'])
	loginModel = userprofile.objects.get(is_user = True ,id = request.session['userid'])
	element =Projectwiseusersetup.objects.get(userid=loginModel.id,project_id_id = request.session['projectid'] )
	projectselect =Projectwiseusersetup.objects.filter(userid =request.session['userid'])
	project_title = element.project_id.slug
	
	try:
		loginobj = Login.objects.get(project_id_id=pid)
	except Login.DoesNotExist:
		loginobj = None

	if loginobj:
		lform=LoginForm(instance=loginobj)
	else:
		lform = LoginForm() #An Unbound Form



	return render(request, 'loginindex.html', locals())

@csrf_exempt
def add(request):
	
	pid = Project.objects.get(pk=request.session['projectid'])
	try:
		loginobjEdit = Login.objects.get(project_id_id=pid)
	except Login.DoesNotExist:
		loginobjEdit = None
	
	if loginobjEdit:
		if request.method == 'POST':
			form = LoginForm(request.POST,request.FILES,instance=loginobjEdit)
			if form.is_valid():
				editform = form.save(commit=False)
				editform.createpage = False
				editform.save()
				return HttpResponseRedirect('/logintemplate/loginindex/')
			else:
				print form.errors
	else:
		if request.method == 'POST':
			form = LoginForm(request.POST,request.FILES)
			if form.is_valid():
				newform = form.save(commit=False)
				newform.project_id = pid
				newform.createpage = False
				newform.save()
				return HttpResponseRedirect('/logintemplate/loginindex/')
			else:
				print form.errors

	return render(request, 'loginindex.html')

@myuser_login_required
def delete(request):
	
	pid = Project.objects.get(pk=request.session['projectid'])
	
	try:
		
		loginobjDelete = Login.objects.get(project_id_id=pid)
	except Login.DoesNotExist:
		loginobjDelete = None
    
	if loginobjDelete:
		query = Login.objects.get(pk = loginobjDelete.id)
		query.delete()
    
	return HttpResponseRedirect('/logintemplate/loginindex/')  

@myuser_login_required
def serverconfig(request):
	
	loginModel = userprofile.objects.get(is_user = True ,id = request.session['userid'])
	element =Projectwiseusersetup.objects.get(userid=loginModel.id,project_id_id = request.session['projectid'] )
	projectselect =Projectwiseusersetup.objects.filter(userid =request.session['userid'])
	project_title = element.project_id.title
	pid = Project.objects.get(pk=request.session['projectid'])
	
	userObj = UserList.objects.filter(Q(project_id_id=pid) & ~Q(db_status='deleted'))
	infoObj = GeneralInfo.objects.filter(Q(project_id_id=pid) & ~Q(db_status='deleted'))

	infoform = GeneralInfoForm()

	
	return render(request, 'serverconfig.html',locals())

@csrf_exempt
def adduser(request):
	pid = Project.objects.get(pk=request.session['projectid'])
	
	if request.method == 'POST':
		userform = UserListForm(request.POST)
		# password = request.POST.get('password')
		# url = 'http://192.168.125.75:32923/mservice/mobileserviceapi/encryptStr'
		# data = {"data" : password}
		# response = requests.post(url, params=data)
		
		try:
			if userform.is_valid():
				newUser = userform.save(commit=False)
				# newUser.password = response.text
				# newUser.confirm_password = response.text
				newUser.project_id = pid
				newUser.is_active = True
				newUser.db_status = 'new'
				newUser.save()
				return HttpResponse("Success")
			else:
				print userform.errors
				return HttpResponse("Failure2")
		except Exception as e:
			print e
			return HttpResponse("Failure1")

		
	else:
		# roleObj = Role.objects.filter(projectid_id=pid)
		userform = UserListForm()
		userform.fields["role"].queryset = Role.objects.filter(projectid_id=pid)

		return render(request,'usermodal.html',locals())

def edituser(request,userid):
	pid = Project.objects.get(pk=request.session['projectid'])
	userObj = UserList.objects.get(id=userid)
	old_status = userObj.db_status
	print old_status
	
	if request.method == 'POST':
		# password = request.POST.get('password')
		# url = 'http://192.168.125.75:32923/mservice/mobileserviceapi/encryptStr'
		# data = {"data" : password}
		# response = requests.post(url, params=data)
		
		if old_status != 'new':
			try:
				existingData = EditedUsersList.objects.get(user_id=userObj.id)
			except EditedUsersList.DoesNotExist:
				existingData = None
			
			if existingData == None:
				user_backup_tab = EditedUsersList()
				user_backup_tab.user_id = userObj.id
				user_backup_tab.user_old_email = userObj.email_id
				user_backup_tab.pid = userObj.project_id_id
				user_backup_tab.save()
			else:
				existingData.user_old_email = userObj.email_id
				existingData.save()
			
		userform = UserListForm(request.POST,instance=userObj)
		
		try:
			if userform.is_valid():
				if old_status == 'new':
					edditedUser = userform.save(commit=False)
					# edditedUser.password = response.text
					# edditedUser.confirm_password = response.text
					edditedUser.save()
					
				else:
					uform = userform.save(commit=False)
					# uform.password = response.text
					# uform.confirm_password = response.text
					uform.db_status = 'edited'
					uform.save()

				
				return HttpResponse("Success")
			else:
				print form.errors
				return HttpResponse("Failure2")
		except Exception as e:
			print e
			return HttpResponse("Failure1")

		
	else:
		userform = UserListForm(instance=userObj)
		userform.fields["role"].queryset = Role.objects.filter(projectid_id=pid)
		return render(request,'usereditmodal.html',locals())
	
    
	

@myuser_login_required
def deleteuser(request,userid):
	
	try:
		query = UserList.objects.get(id=userid)
	except Login.DoesNotExist:
		query = None
    
	if query:
		query.db_status = 'deleted'
		query.save()    
	return HttpResponseRedirect('/logintemplate/serverconfig/') 

def addinfo(request):
	
	pid = Project.objects.get(pk=request.session['projectid'])
	
	if request.method == 'POST':
		infoform = GeneralInfoForm(request.POST)
		try:
			if infoform.is_valid():
				newInfo = infoform.save(commit=False)
				newInfo.project_id = pid
				newInfo.db_status = 'new'
				newInfo.save()
				return HttpResponse("Success")
			else:
				print infoform.errors
				return HttpResponse("Failure2")
		except Exception as e:
			print e
			return HttpResponse("Failure1")

def editinfo(request,infoid):

	pid = Project.objects.get(pk=request.session['projectid'])
	editInfoObj = GeneralInfo.objects.get(id=infoid)
	old_status = editInfoObj.db_status
	print old_status
	
	if request.method == 'POST':

		if old_status != 'new':
			try:
				existingData = EditedInfo.objects.get(key_id=editInfoObj.id)
			except EditedInfo.DoesNotExist:
				existingData = None
			
			if existingData == None:
				info_backup_tab = EditedInfo()
				info_backup_tab.key_id = editInfoObj.id
				info_backup_tab.old_key = editInfoObj.key
				info_backup_tab.pid = editInfoObj.project_id_id
				info_backup_tab.save()
			else:
				existingData.old_key = editInfoObj.key
				existingData.save()

		infoform = GeneralInfoForm(request.POST,instance=editInfoObj)
		try:
			if infoform.is_valid():

				if old_status == 'new':
					infoform.save()
				else:
					iform = infoform.save(commit=False)
					iform.db_status = 'edited'
					iform.save()
				
				return HttpResponse("Success")
			else:
				print infoform.errors
				return HttpResponse("Failure2")
		except Exception as e:
			print e
			return HttpResponse("Failure1")
	else:
		infoform = GeneralInfoForm(instance=editInfoObj)
		return render(request,'infoeditmodal.html',locals())


def deleteinfo(request,infoid):

	try:
		query = GeneralInfo.objects.get(id=infoid)
	except Login.DoesNotExist:
		query = None
    
	if query:
		query.db_status = 'deleted'
		query.save()
    
	return HttpResponseRedirect('/logintemplate/serverconfig/')


def generateTemplate(pid):
	filePath = settings.MEDIA_ROOT
	lstarthtml = ""
	lbodyhtml =""
	lcontenthtml =""
	lbodystart = ""
	lbodyend=""
	lbodyhtml=""
	lendhtml =""
	lheaderhtml ="""<ion-header></ion-header><ion-content class="background">"""
	lendhtml ="""</ion-content>"""
	lbodystart = """<div><div style="background-image: url('images/bg-01.jpg');"><div class="wrap-login100"><form class="login100-form validate-form"><span class="login100-form-logo"><img src="assets/imgs/logo.png" style="width:50%" /></span><span class="login100-form-title p-b-34 p-t-27">Log in</span>"""
	login  = Login.objects.get(project_id_id = pid)
	if login.login_type == 'form':
		lbodyhtml = formhtml(login,pid)
	elif login.login_type == 'otp':
		lbodyhtml = otphtml(login,pid)
	elif login.login_type == 'bar':
		lbodyhtml = barhtml(login)

	if login.regeisterion_page == True:
		rghtml = """<div class="text-center1"><a class="txt1" href="#">Have You Not Registered Yet?</a></div><div class="container-login100-form-btn"><button class="login100-form-btn bg" id="reigterbt" (click)="register($event)">Register</button></div>"""
	else:
		print "NO REG PAGE TEMPLATE"
		rghtml=""""""


	lbodyend = """<div class="text-center p-t-90"><a class="txt1" href="#">Forgot Password?</a></div></form></div></div></div>"""
	lcontenthtml = lheaderhtml+lbodystart+lbodyhtml+rghtml+lbodyend+lendhtml
	project = Project.objects.get(id = login.project_id_id)
	ptitle = project.slug
	if not os.path.exists(filePath+"static/ionicmeta/"+ptitle+"/login"):
		os.makedirs(filePath+"static/ionicmeta/"+ptitle+"/login")

	Html_file= open(filePath+"static/ionicmeta/"+ptitle+"/login/login.html","w")
	Html_file.write(lcontenthtml)
	Html_file.close()
	login_scss(ptitle,login)
	return HttpResponse("success")

def login_scss(ptitle,login):
	filePath = settings.MEDIA_ROOT
	css_file= open(filePath+"static/ionicmeta/"+ptitle+"/login/login.scss","w")
	css_file.write("")
	css_file.close()
	with open(filePath+"static/ionicsrc/login/login.scss") as scss:
		with open(filePath+"static/ionicmeta/"+ptitle+"/login/login.scss", "w") as scss1:
			for line in scss:
				scss1.write(line)

	if login.bgcolor == 'green':
		color1 = "#0aab60"
	elif login.bgcolor == 'red':
		color1 = "#da4b4b"
		color2 ="#b21414"
	elif login.bgcolor == 'blue':
		color1 ="#41a6e0"
		color2 ="#7579ff"

	with open(filePath+"static/ionicmeta/"+ptitle+"/login/login.scss", "r") as file :
		filedata = file.read()

	# Replace the target string
	filedata = filedata.replace('#41a6e0', color1)
	# Write the file out again
	with open(filePath+"static/ionicmeta/"+ptitle+"/login/login.scss", "w") as file:
		file.write(filedata)	
		

def formhtml(login,pid):
	html = ""
	buttonhtml =""
	sql = ""
	projectObj = Project.objects.get(id=pid)
	if projectObj.ismultitenant == True:
		if projectObj.imei_based_login == True:
			imeiSqlStr = "ri.imei_no,"
		else:
			imeiSqlStr = ""
		
		sql = "SELECT ri.userid AS 'muserid',ri.firstname AS 'first_name', ri.phonenumberind AS 'mobile_number', ri.emailidind AS 'email_id', ri.enabled  AS 'is_active', 'User' AS role, ri.projectid, "+imeiSqlStr+" si.mservice_url FROM register_info ri,system_info si WHERE ri.node_id = si.nodeid AND phonenumberind = :USERNAME AND passwordind = :PASSWORD"
	
	else: 

		if projectObj.imei_based_login == True:
			imeiSqlStr = "imei_no,"
		else:
			imeiSqlStr = ""
		
		sql = "SELECT muserid,first_name, mobile_number, email_id, role, is_active, "+imeiSqlStr+" "+pid+" AS projectid FROM muser WHERE mobile_number = :USERNAME AND pwd = :PASSWORD"


	print "************"
	print sql
	
	html = """<div class="wrap-input100 validate-input" data-validate = "Enter username"><ion-row><ion-icon name="person" class="icon-login"></ion-icon><input class="input100" type="text"id="login_username_id" [(ngModel)]="Username" name="username" placeholder="Username"><span class="focus-input100"></span></ion-row></div>
	               <div class="wrap-input100 validate-input" data-validate="Enter password"><ion-row>
                     <ion-icon name="lock" class="icon-login"></ion-icon>
						<input class="input100" type="password" id="login_password_id" [(ngModel)]="Password" name="pass" placeholder="Password">
						<span class="focus-input100"></span></ion-row>
					</div>"""

	buttonhtml = """<div class="container-login100-form-btn">
						<button class="login100-form-btn" id="login_login_id" data-sql=\""""+sql+"""\" data-sqlparams="USERNAME,PASSWORD" data-logintype="form" 
  	(click)="customLogin($event)">
							Login
						</button>
					</div>""" 
	formhtml = html+buttonhtml
	return formhtml

def otphtml(login,pid):
	html= ""
	sql = ""

	projectObj = Project.objects.get(id=pid)
	imeiSqlStr = ""
	

	if projectObj.ismultitenant == True:
		if projectObj.imei_based_login == True:
			imeiSqlStr = "ri.imei_no"
		else:
			imeiSqlStr = ""
		
		sql = "SELECT ri.userid AS 'muserid',ri.firstname AS 'first_name', ri.phonenumberind AS 'mobile_number', ri.emailidind AS 'email_id', ri.enabled  AS 'is_active', 'User' AS role, ri.projectid, "+imeiSqlStr+" si.mservice_url FROM register_info ri,system_info si WHERE ri.node_id = si.nodeid AND phonenumberind = :MOBILENUMBER"
	
	else: 
		if projectObj.imei_based_login == True:
			imeiSqlStr = "imei_no"
		else:
			imeiSqlStr = ""
		
		sql = "SELECT muserid,first_name, mobile_number, email_id, role, is _active, "+imeiSqlStr+" "+pid+" AS projectid FROM muser WHERE mobile_number = :MOBILENUMBER"
	
	html ="""<div class="wrap-input100 validate-input" data-validate = "Enter Mobilenumber"><ion-row><ion-icon name="phone-portrait" class="icon-login"></ion-icon><input class="input100" type="text"id="login_mobilenumber_id" [(ngModel)]="Mobilenumber" name="mobilenumber" placeholder="Mobile Number"><span class="focus-input100"></span></ion-row></div>"""
	buttonhtml= """<div class="container-login100-form-btn">
						<button class="login100-form-btn" id="login_login_id" data-sql=\""""+sql+"""\" data-sqlparams="MOBILENUMBER" data-logintype="otp" 
  	(click)="customLogin($event)">
							LOGIN
						</button></div>"""
	otphtml = html+buttonhtml
	return otphtml					 

def barhtml(login):
	barhtml = ""
	return barhtml

def generateLoginpage(projectid):
	try:
		filePath = settings.MEDIA_ROOT
		project = Project.objects.get(id = projectid)
		ptitle = project.slug
		if not os.path.exists(filePath+"ionicapps/"+ptitle+"/src/pages/login"):
			os.makedirs(filePath+"ionicapps/"+ptitle+"/src/pages/login")

		with open(filePath+"static/ionicmeta/"+ptitle+"/login/login.html") as f:
			with open(filePath+"ionicapps/"+ptitle+"/src/pages/login/login.html", "w") as f1:
				for line in f:
					f1.write(line)

		appincludeTs(ptitle,"login")
		logints_scss(ptitle,"login")
		loginlogo(projectid,ptitle)
		loginObj = Login.objects.get(project_id_id = projectid)
		print loginObj.regeisterion_page
		if loginObj.regeisterion_page == True:
			generateRegPage(projectid)
		else:
			print "*************"
			print "REG PAGE FALSE"
	except Exception as e:
		print "**********"
		print e
	return "success"			

def logints_scss(ptitle,filename):
	filePath = settings.MEDIA_ROOT
	try:
		with open(filePath+"static/ionicsrc/"+filename+"/"+filename+".ts") as f:
			with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+filename+"/"+filename+".ts", "w") as f1:
				for line in f:
					f1.write(line)
		if filename == "login":
			with open(filePath+"static/ionicmeta/"+ptitle+"/"+filename+"/"+filename+".scss") as scss:
				with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+filename+"/"+filename+".scss", "w") as scss1:
					for line in scss:
						scss1.write(line)
		elif filename == "registration":
			with open(filePath+"static/ionicsrc/registration/registration.scss") as scss:
				with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+filename+"/"+filename+".scss", "w") as scss1:
					for line in scss:
						scss1.write(line)
	except Exception as e:
		print e

def appincludeTs(ptitle,filename):
	filePath = settings.MEDIA_ROOT
	with open(filePath+"ionicapps/"+ptitle+"/src/app/app.module.ts") as f:
		lines = f.readlines()
		#print lines
		imp = lines.index("import { HomePage } from '../pages/home/home';\n")
		try:
			if lines.index("import { "+filename.capitalize()+"Page } from '../pages/"+filename+"/"+filename+"';\n"):
				i = lines.index("import { "+filename.capitalize()+"Page } from '../pages/"+filename+"/"+filename+"';\n")

		except:
			lines.insert(imp+1, "import { "+filename.capitalize()+"Page } from '../pages/"+filename+"/"+filename+"';\n")
			dec = lines.index( '  declarations: [\n')
			lines.insert(dec+2, "    "+filename.capitalize()+"Page,\n")
			ent = lines.index( '  entryComponents: [\n')
			lines.insert(ent+2, "    "+filename.capitalize()+"Page,\n")
			#print imp 

	with open(filePath+"ionicapps/"+ptitle+"/src/app/app.module.ts","w") as file:
		for tslines in lines:
			file.write(tslines)

	return lines

def loginlogo(pid,ptitle):
	filePath = settings.MEDIA_ROOT
	try:
		print "arun at login"
		login = Login.objects.get(project_id_id = pid)
		if login.logoimg:
			with open(filePath+"/"+str(login.logoimg), "r") as file :
				filedata = file.read()

			with open(filePath+"ionicapps/"+ptitle+"/src/assets/imgs/logo.png", "w") as file:
				file.write(filedata)

		return "success"		

	except Exception as e:
		print e
		return "success"
def loginmetaJson(loginjson,ptitle):
	filePath = settings.MEDIA_ROOT
	if not os.path.exists(filePath+"ionicapps/"+ptitle+"/src/assets/json"):
		os.makedirs(filePath+"ionicapps/"+ptitle+"/src/assets/json")

	json_file= open(filePath+"ionicapps/"+ptitle+"/src/assets/json/login.json","w")
	json_file.write(loginjson)
	json_file.close()

def alreadyLoginpg(request,pid):
	filePath = settings.MEDIA_ROOT
	currentProject = Project.objects.get(id = pid)
	login = Login.objects.get(project_id_id = pid)
	Ptname = currentProject.slug
	if login.createpage == True:
		return HttpResponse("exist")
	else:
		return HttpResponse("not exist")


@csrf_exempt
def createLoginpg(request,pid):
	try:
		generateTemplate(pid)
		login = Login.objects.get(project_id_id = pid)
		login.createpage = True
		login.save()
		return HttpResponse("success")
	except Exception as e:
		print e
		return HttpResponseBadRequest("error")	


@csrf_exempt
def update_user_in_db(request):
	
	project_id = request.session['projectid']
	user_id = request.session['userid']
	db_error = []
	
	errors = update_user_and_generalinfo(request,user_id,project_id,"server")
	errors += update_user_and_generalinfo(request,user_id,project_id,"client")
	
	if len(errors) > 0:
		for error in errors:
			db_error.append(str(error))
			print db_error
		return HttpResponse(json.dumps(db_error))
	else:
		return HttpResponse("SUCCESS")



def callService(request):
	
	url = 'http://192.168.125.75:32923/mservice/mobileserviceapi/encryptStr'
	data = {"data" : "password"}
	response = requests.post(url, params=data)
	dat = response.text
	print dat

	return HttpResponse("AISH")


def generateRegTemplate(viewid,ptitle):
	regheaderhtml ="""<ion-header></ion-header>
					<ion-content class="background">"""
	
	
	regbodystart = """<div>
						<div style="background-image: url('images/bg-01.jpg');">
						<div class="wrap-login100">
						<form class="login100-form validate-form" id="signupForm" name="signupForm">
						<span class="login100-form-title p-b-34 p-t-27">Register</span>"""
	
	# regbodyend = """<span class="focus-input100"></span>
	# 				</div>"""
	regendhtml =""" <div class="container-login100-form-btn">
                        <button class="login100-form-btn" id="sign_up" (click)="save($event)">
                            Sign Up
                        </button>
                    </div>
					<div class="text-center1"><a class="txt1" href="#">Already have an account?</a></div>
                    <div class="container-login100-form-btn">
                        <button class="login100-form-btn bg" id="reigterbt" (click)="login($event)">Login</button>
                    </div>
					</form></div></div></div></ion-content>"""

	transgroup = Transactionview.objects.filter(id = viewid)
	tran_serializer = ViewtreeSerializer(instance=transgroup,many=True)
	tran_serializer_json = json.dumps(tran_serializer.data)
	formhtml = tran_serializer.data[0]
	viewtype = tran_serializer.data[0]['vt']
	conthtml = formhtml['cont_meta']
	listhtml = lists(conthtml[0],viewtype,"registration",ptitle,"primary")
	regbodymid =listhtml

	wholehtml = regheaderhtml+regbodystart+regbodymid+regendhtml

	if not os.path.exists(filePath+"static/ionicmeta/"+ptitle+"/registration"):
		os.makedirs(filePath+"static/ionicmeta/"+ptitle+"/registration")

	Html_file= open(filePath+"static/ionicmeta/"+ptitle+"/registration/registration.html","w")
	Html_file.write(wholehtml)
	Html_file.close()
	ionicmetaJson(tran_serializer_json,"registration",ptitle)				
	return "success"


def generateRegPage(projectid):
	filePath = settings.MEDIA_ROOT
	project = Project.objects.get(id = projectid)
	ptitle = project.slug
	if not os.path.exists(filePath+"ionicapps/"+ptitle+"/src/pages/registration"):
		os.makedirs(filePath+"ionicapps/"+ptitle+"/src/pages/registration")

	with open(filePath+"static/ionicmeta/"+ptitle+"/registration/registration.html") as f:
		with open(filePath+"ionicapps/"+ptitle+"/src/pages/registration/registration.html", "w") as f1:
			for line in f:
				f1.write(line)

	with open(filePath+"static/ionicmeta/"+ptitle+"/registration/registration.json") as f:
		with open(filePath+"ionicapps/"+ptitle+"/src/assets/json/registration.json", "w") as f1:
			for line in f:
				f1.write(line)

	appincludeTs(ptitle,"registration")
	logints_scss(ptitle,"registration")

	#IMPORING REG PAGE  

	with open(filePath+"ionicapps/"+ptitle+"/src/pages/login/login.ts", "r") as file :
		filedataForImport = file.readlines()

	scrpit = filedataForImport.index("import { HomePage } from '../home/home';\n",)
	filedataForImport.insert(scrpit+1, "import { RegistrationPage } from '../registration/registration';\n")
	
	with open(filePath+"ionicapps/"+ptitle+"/src/pages/login/login.ts", "w") as loginfile :
		for tslines in filedataForImport:
			loginfile.write(tslines)

	#WRITING REGISTER FUNCTION
	with open(filePath+"ionicapps/"+ptitle+"/src/pages/login/login.ts", "r") as file :
		fieldataFun = file.readlines()
	
	lastrow = len(fieldataFun)
	for i in range(1,20): 
		if fieldataFun[lastrow-i] != "\n":
			print fieldataFun[lastrow-i]
			print i
			lastrowofData = lastrow-i
			fieldataFun.insert(lastrowofData-1, "\n \tregister(){\n \t \t this.navCtrl.setRoot(RegistrationPage); \n \t}\n")
			break

	with open(filePath+"ionicapps/"+ptitle+"/src/pages/login/login.ts", "w") as loginfilefun :
		for funlines in fieldataFun:
			loginfilefun.write(funlines)
		