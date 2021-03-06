# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponseRedirect, HttpResponse,HttpResponseBadRequest
from django.shortcuts import render
from django.contrib import messages
from authentication.models import userprofile
from project.models import Projectwiseusersetup,Project
from transactionview.models import Transactionview
from logintemplate.models import Login,GeneralInfo
from reportview.models import Report
from .models import Homepage,Menu,RootPage,SubMenuConfig
from .forms import HomepageForm,MenuForm,RootPageForm,SubMenuConfigForm
from transactionview.serializers import ContainerSerializer
from transactionview.views import txnCreation
from reportview.views import generate_reportpage
from django.core import serializers
from hometemplate.serializers import HomepageSerializer
from rolesetup.serializers import RoleSerializer
from rolesetup.models import Role
import json
from Mobilebuilder.decorators import myuser_login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os

# Create your views here.
filePath = settings.MEDIA_ROOT
@csrf_exempt
@myuser_login_required
def hometemplate(request):
	element =Projectwiseusersetup.objects.get(userid = request.session['userid'],project_id = request.session['projectid'])
	project_title = element.project_id.slug
	projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])
	projectid = request.session['projectid']
	try:
		query = Homepage.objects.get(project_id_id = request.session['projectid'])
		menu = Menu.objects.filter(homepageid_id = query.id).order_by('id')
		rootsetup = RootPage.objects.get(project_id = request.session['projectid'])
		for lists in menu:
			if lists.typeofview == "transactionview":
				txviewid = lists.transactionview_id
				view = Transactionview.objects.get(id = txviewid)
			elif lists.typeofview == "reportview":
				repoviewid=lists.reportview_id
				view = Report.objects.get(id = repoviewid)

				if view.createpage == False:
					menulist = Menu.objects.get(id = lists.id)
					menulist.createpage = False
					menulist.save()

	except:
		query = Homepage.objects.filter(project_id_id = request.session['projectid'])

	if query:
		menu = Homepage.objects.get(project_id_id = request.session['projectid'])
		menulist = Menu.objects.filter(homepageid = menu.id).order_by('id')
		submenu = SubMenuConfig.objects.filter(homepageid = menu.id).order_by('displayorder')
		form = HomepageForm(request.POST or None,instance = menu)
		try:
			rootsetup = RootPage.objects.get(project_id = request.session['projectid'])
			root_form = RootPageForm(instance = rootsetup,homeid = menu.id)
		except Exception as e:
			print e
			rootpage = RootPage.objects.create(pageoption = 'default',project_id = request.session['projectid'])
			rootsetup = RootPage.objects.get(project_id = request.session['projectid'])
			root_form = RootPageForm(instance = rootsetup,homeid = menu.id)
	else:
		form = HomepageForm(request.POST or None)

	if request.method =='POST':
		if form.is_valid():
			savemenu = form.save(commit = False)
			savemenu.project_id_id = request.session['projectid']
			savemenu.save()
			try:
				dirPath = filePath+"static/ionicmeta/"+project_title
				fileList = os.listdir(dirPath)
				for fileName in fileList:
					if fileName == "db" or fileName =="login":
						pass
					else:
						os.system("rm -rf "+dirPath+"/"+fileName)

				for menu in menulist:
					if menu.typeofview == "transactionview":
						txnCreation(projectid,menu.transactionview_id)
					elif lists.typeofview == "reportview":
						generate_reportpage(request,menu.reportview_id)
			except Exception as e:
				print e
				return HttpResponse(e)

			return HttpResponse("Saved Successfully.")
		else:
			return HttpResponseBadRequest("Failed To Save.")
	else:
		return render(request,'pagecomponent.html',locals())

@csrf_exempt
def rootpage(request,homeid):
	print request.POST
	projectid = request.session['projectid']
	rootsetup = RootPage.objects.get(project_id = projectid)
	if request.POST:
		form = RootPageForm(request.POST,instance = rootsetup,homeid = homeid)
		print form.is_valid()
		print form.errors
		if form.is_valid():
			root = form.save(commit = False)
			root.project_id = projectid
			root.save()
			return HttpResponse('success')
		else:
			return HttpResponseBadRequest('error')

@myuser_login_required
def transview_asjson(request):
    data =serializers.serialize('json', Transactionview.objects.filter(projectid_id = request.session['projectid']))
    return HttpResponse(data)

@myuser_login_required
def addmenu(request):
	homepage = Homepage.objects.get(project_id_id = request.session['projectid'])
	reportview =Report.objects.filter(project_id = request.session['projectid'])
	pid = request.session['projectid']
	transactionview = Transactionview.objects.filter(projectid_id = request.session['projectid'])
	if request.method =='POST':
		tform = MenuForm(request.POST,pid = pid)
		if tform.is_valid():
			menuproperty = tform.save(commit = False)
			menuproperty.homepageid_id = homepage.id
			menuproperty.transactionview_id =request.POST.get("transactionview","")
			menuproperty.reportview_id =request.POST.get("reportview","")
			menuproperty.save()
			return HttpResponse('success')
		else:
			print 'ERRORS',tform.errors
			messages.add_message(request, messages.ERROR, 'There was some problems while saving.')
			return HttpResponseBadRequest('error')
	else:
		form = MenuForm(pid = pid)

		return render(request,'menuproperty.html',locals())

@csrf_exempt
def submenuadd(request):
	print "submenu"
	homepage = Homepage.objects.get(project_id_id = request.session['projectid'])
	pid = request.session['projectid']
	if request.method =='POST':
		tform = SubMenuConfigForm(request.POST,homeid = homepage.id)
		if tform.is_valid():
			submenu = tform.save(commit = False)
			submenu.homepageid_id = homepage.id
			submenu.project_id = pid
			submenu.save()
			return HttpResponseRedirect('/hometemplate/submenutable/%s'%homepage.id)
		else:
			print 'ERRORS',tform.errors
			messages.add_message(request, messages.ERROR, 'There was some problems while saving.')
			return HttpResponseBadRequest(json.dumps(tform.errors))
	else:
		print "no post"
		form = SubMenuConfigForm(homeid = homepage.id)
		return render(request,'submenuconfig.html',locals())

@myuser_login_required
def editmenu(request,menuid):
	menu_id = menuid
	transactionview = Transactionview.objects.filter(projectid_id = request.session['projectid'])
	pid = request.session['projectid']
	menu = Menu.objects.get(pk = menuid)
	home_id = menu.homepageid_id
	txview = menu.transactionview
	repview = menu.reportview
	if request.method =='POST':
		tform = MenuForm(request.POST,instance = menu,pid =pid)
		if tform.is_valid():
			tform.save()
			return HttpResponse("sucess")
		else:
			messages.add_message(request, messages.ERROR, 'There was some problems while saving.')
			return HttpResponseBadRequest('error')
	else:
		form = MenuForm(instance = menu,pid = pid)
		return render(request,'editmenu.html',locals())

@csrf_exempt
def submenuedit(request,menuid):
	print "submenu edit"
	menu_id = menuid
	pid = request.session['projectid']
	menu = SubMenuConfig.objects.get(pk = menuid)
	submenu = menu.id
	home_id = menu.homepageid_id
	if request.method =='POST':
		tform = SubMenuConfigForm(request.POST,instance = menu,homeid =home_id)
		if tform.is_valid():
			tform.save()
			return HttpResponseRedirect('/hometemplate/submenutable/%s'%home_id)
		else:
			messages.add_message(request, messages.ERROR, 'There was some problems while saving.')
			return HttpResponseBadRequest(json.dumps(tform.errors))
	else:
		form = SubMenuConfigForm(instance = menu,homeid =home_id)
		return render(request,'submenuedit.html',locals())

@myuser_login_required
def submenutable(request,homeid):
	submenu = SubMenuConfig.objects.filter(homepageid_id = homeid).order_by('displayorder')
	return render(request,'submenutable.html',locals())

@myuser_login_required
def deletesubmenu(request,menuid):
	query = SubMenuConfig.objects.get(pk = menuid)
	query.delete()
	return HttpResponseRedirect('/hometemplate/pagecomponent')

@myuser_login_required
def deletemenu(request,menuid):
	query = Menu.objects.get(pk = menuid)
	query.delete()
	return HttpResponseRedirect('/hometemplate/pagecomponent')

@myuser_login_required
def generatepage(request,homeid):
	projectid = request.session['projectid']
	home = Homepage.objects.filter(project_id_id = projectid)
	homemenu_serializer = HomepageSerializer(instance=home,many=True)
	homemenu_serializer_json = json.dumps(homemenu_serializer.data)
	home = homemenu_serializer.data[0]
	page = request.GET.get('page').lower().replace(" ","")
	if request.GET.get('value') == "true":
		value = True
	else:
		value = False
	menu = Menu.objects.get(id = homeid)
	print os.path.exists(filePath+"static/ionicmeta/"+home['project_id']+"/"+page)
	try:
		if os.path.exists(filePath+"static/ionicmeta/"+home['project_id']+"/"+page+"/"+page+".html"):
			menu.createpage = value
			menu.save()
			return HttpResponse("success")
		else:
			return HttpResponseBadRequest('Page Definition not generated.Please give "Generate Page".')
	except Exception as e:
		print e
		return HttpResponseBadRequest('Page Definition not generated.Please give "Generate Page".')


def homehtml(pid):
	homehtml =""
	home = Homepage.objects.filter(project_id_id = pid)
	homemenu_serializer = HomepageSerializer(instance=home,many=True)
	homemenu_serializer_json = json.dumps(homemenu_serializer.data)
	rolesetup = Role.objects.filter(projectid_id = pid)
	rolesetup_serializer = RoleSerializer(instance=rolesetup,many=True)
	rolesetup_serializer_json = json.dumps(rolesetup_serializer.data)
	try:
		home = homemenu_serializer.data[0]
		role = rolesetup_serializer.data
		submenu = SubMenuConfig.objects.filter(project_id = home['pid']).order_by('displayorder')
		if home['menutype'] == "sidemenu":
			homehtml = sidemenupage(home,role,submenu)
		elif home['menutype'] == "grid":
			homehtml = gridmenupage(home,role,submenu)
		else:
			homehtml =""
	except Exception as e:
		print e
		raise e
	return HttpResponse(homehtml)


def sidemenupage(home,role,submenu):
	sideheader =""
	sidebody =""
	sidehtml=""
	login = Login.objects.filter(project_id_id = home['pid'])
	if submenu:
		sideheader = """<ion-header><ion-navbar color="primary"><ion-buttons """+home['sidemenu']+"""><button ion-button menuToggle><ion-icon name="menu"></ion-icon></button></ion-buttons><ion-row><ion-title>"""+home['p_title'].title()+"""</ion-title><ion-col col-1><ion-icon name="more" item-right (click)="presentPopover($event)" class="more_icon"></ion-icon></ion-col></ion-row></ion-navbar></ion-header><ion-nav [root]="rootPage" #content swipeBackEnabled="false"></ion-nav>"""
	else:
		sideheader = """<ion-header><ion-navbar color="primary"><ion-buttons """+home['sidemenu']+"""><button ion-button menuToggle><ion-icon name="menu"></ion-icon></button></ion-buttons><ion-title>"""+home['p_title'].title()+"""</ion-title></ion-navbar></ion-header><ion-nav [root]="rootPage" #content swipeBackEnabled="false"></ion-nav>"""

	sidebody = """<ion-content padding></ion-content>"""
	sidehtml = sideheader+sidebody
	page = homepage(home['menutype'],home['project_id'],sidehtml)
	try:
		appcom = appcomponentInclude(home['project_id'],home,role)
	except Exception as e:
		print e
		raise Exception(e)

	appmod = appmoduleincludeTs(home['project_id'],home['menutype'])
	popup = popuppage(submenu,home,login)
	return sidehtml

def homepage(fileName,ptitle,html):
	if not os.path.exists(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName):
		os.makedirs(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName)

	Html_file= open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".html","w")
	Html_file.write(html)

	with open(filePath+"static/ionicsrc/"+fileName+"/"+fileName+".ts") as f:
		with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".ts", "w") as f1:
			for line in f:
				f1.write(line)

	with open(filePath+"static/ionicsrc/"+fileName+"/"+fileName+".scss") as scss:
		with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".scss", "w") as f1:
			for line1 in scss:
				f1.write(line1)


def appcomponentInclude(ptitle,home,role):
	complines = ["import { Component, ViewChild } from '@angular/core';\n", "import { Nav, Platform ,AlertController} from 'ionic-angular';\n", "import { StatusBar } from '@ionic-native/status-bar';\n", "import { SplashScreen } from '@ionic-native/splash-screen';\n", "import { Storage } from '@ionic/storage';\n", "import { Events } from 'ionic-angular';\n","import { OneSignal } from '@ionic-native/onesignal';\n", "import { ModalController } from 'ionic-angular';\n", "import { MenuController } from 'ionic-angular';\n", "import { IonicApp} from 'ionic-angular';\n", "import { ToastController } from 'ionic-angular';\n", '\n',"import { SingletonProvider } from '../providers/singleton/singleton';\n",  "import { NotifyProvider } from '../providers/notify/notify';\n", "import { HomePage } from '../pages/home/home';\n", '\n', '@Component({\n', "  templateUrl: 'app.html'\n", '})\n', 'export class MyApp {\n', '  @ViewChild(Nav) nav: Nav;\n', '  rootPage: any = HomePage;\n', '  UserDetails:any;\n', '  alert:any;\n', '  pages: Array<{title: string,cls: string, component: any}>;\n', '\n', '  constructor(public platform: Platform,private alertCtrl: AlertController, public statusBar: StatusBar,public events: Events,public modal:ModalController,public singleton:SingletonProvider,public menuCtrl:MenuController,public ionicApp:IonicApp,public toastCtrl: ToastController, public splashScreen: SplashScreen, public storage: Storage,private oneSignal: OneSignal,public notify:NotifyProvider) {\n', '    this.initializeApp();\n', '    // used for an example of ngFor and navigation\n', "    events.subscribe('user:role', (role) => {\n", '     }); \n', '}\n', '   initializeApp() {\n', '    this.platform.ready().then(() => {\n', '      // Okay, so the platform is ready and our plugins are available.\n', '      // Here you can do any higher level native things you might need.\n', '     // let status bar overlay webview\n', '\t\tthis.statusBar.overlaysWebView(false);\n', '\t\t// set status bar to white\n', "\t\tthis.oneSignal.startInit(this.singleton.apikey, this.singleton.senderid);\n","\t\tthis.oneSignal.inFocusDisplaying(this.oneSignal.OSInFocusDisplayOption.Notification);\n",'\t\tthis.oneSignal.handleNotificationReceived().subscribe((data) => {\n','\t\t // do something when notification is received\n','\t\t\tthis.notify.notificationIndb(data);\n','\t\t});\n','\t\tthis.oneSignal.handleNotificationOpened().subscribe((data) => {\n','\t\t  // do something when a notification is opened\n','\t\t\tthis.notify.notificationIndb(data);\n','\t\t});\n',"\t\tthis.oneSignal.endInit();\n","\t\tthis.statusBar.backgroundColorByHexString('#000000');\n",'      \tthis.splashScreen.hide();\t\n', '\t    this.platform.registerBackButtonAction(() => {\n', '\t\t         let ready;\n', '                 let activePortal = this.ionicApp._loadingPortal.getActive() ||\n', '                 this.ionicApp._modalPortal.getActive() ||\n', '                 this.ionicApp._toastPortal.getActive() ||\n', '                 this.ionicApp._overlayPortal.getActive();\n', '                 if (activePortal) {\n', '                     ready = false;\n', '                     activePortal.dismiss();\n', '                     activePortal.onDidDismiss(() => { ready = true; });\n', '                     return;\n', '                  }\n', '                  if (this.menuCtrl.isOpen()) {\n', '                     this.menuCtrl.close();\n', '                     return;\n', '                   }\n', '                    let view = this.nav.getActive();\n', '                    let page = view ? this.nav.getActive().instance : null;\n', '                     if(this.nav.canGoBack()){\n', '                        this.nav.pop();\n', '                     }else{\n', '                         if(this.alert){\n', '                           this.alert.dismiss();\n', '                           this.alert =null;\n', '                     }else{\n', '                          this.showAlert();\n', '                     }\n', '                  }\n', '           }, 1);\n', '    });\n', '  }\n', '\n', '  openPage(page) {\n', '    // Reset the content nav to have just this page\n', "    // we wouldn't want the back button to show in this scenario\n", "    this.storage.get('userObj').then((loginInfo) => {\n", '        this.UserDetails = \tloginInfo;\n','    if(page.title == "Logout"){\n', '    this.nav.setRoot(HomePage);}\n', '    else{\n', '\t\t  console.log(this.nav.canGoBack());\n', '\t\t  if(this.nav.canGoBack() == true){\n', "\t\t\t  this.nav.push(page.component,{'userdetails':this.UserDetails}).then(() => {\n", '\t\t\t\t  const startIndex = this.nav.getActive().index - 1;\n', '\t\t\t\t  this.nav.remove(startIndex, 1);\n', '\t\t\t  });\n', '\t\t  }\n', '\t\t  else\n', '\t\t  {\n', "\t\t\t  this.nav.push(page.component,{'userdetails':this.UserDetails});\n", '\t\t  }\n', '\t  }\n','    });\n', '  }\n', '   \n', '   showAlert() {\n', '           this.alert = this.alertCtrl.create({\n', "            title: 'Exit?',\n", "            message: 'Do you want to exit the app?',\n", '                buttons: [\n', '                 {\n', "                     text: 'Cancel',\n", "                     role: 'cancel',\n", '                     handler: () => {\n', '                     this.alert =null;\n', '                  }\n', '                  },\n', '                 {\n', "                     text: 'Exit',\n", '                     handler: () => {\n', '                     this.platform.exitApp();\n', '                  }\n', '               }\n', '            ]\n', '        });\n', '       this.alert.present();\n', '       }\n', '\n', '      showToast() {\n', '           alert("Press Again to exit");\n', '       }\n', '  }\n', '\n']
	apphtml = ['<ion-menu [content]="content">\n', '  <ion-header>\n', '    <ion-toolbar>\n', '      <ion-title>Menu</ion-title>\n', '    </ion-toolbar>\n', '  </ion-header>\n', '\n', '  <ion-content>\n', '    <ion-list>\n', '      <button menuClose ion-item *ngFor="let p of pages" (click)="openPage(p)">\n', '        <ion-row><ion-col col-2><ion-icon name="{{p.cls}}"></ion-icon></ion-col><ion-col>{{p.title}}</ion-col></ion-row>\n', '      </button>\n', '    </ion-list>\n', '  </ion-content>\n', '\n', '</ion-menu>\n', '\n', "<!-- Disable swipe-to-go-back because it's poor UX to combine STGB with side menus -->\n", '<ion-nav [root]="rootPage" #content swipeBackEnabled="false"></ion-nav>']

	page = complines.index("import { HomePage } from '../pages/home/home';\n")
	login = Login.objects.filter(project_id_id = home['pid'])
	try:
		gInfo = GeneralInfo.objects.get(key = 'notification',project_id_id = home['pid'])
		notifyvalue = gInfo.value.lower()
		complines.insert(page+1, "import { NotificationPage } from '../pages/notification/notification';\n")
	except Exception as e:
		notifyvalue =""

	for menu in home['home_menu']:
		title =""
		icls =""
		pagetitle=""
		title = menu['title'].lower().replace(" ","")
		icls = menu['iconcls']
		if menu['typeofview'] == 'transactionview':
			pagetitle = menu['transactionview'].lower().replace(" ","")
		elif menu['typeofview'] == 'reportview':
			pagetitle = menu['reportview'].lower().replace(" ","")

		complines.insert(page, "import { "+pagetitle.capitalize()+"Page } from '../pages/"+pagetitle+"/"+pagetitle+"';\n")

	event = complines.index("    events.subscribe('user:role', (role) => {\n")
	if login:
		#complines.replace('HomePage', 'LoginPage')
		for r in role:
			complines.insert(event+1, "     if(role == '"+r['rn']+"'){\n")
			page_obj = complines.index("     if(role == '"+r['rn']+"'){\n")
			complines.insert(page_obj+1,"      }\n")
			pg_obj = complines.index("     if(role == '"+r['rn']+"'){\n")
			complines.insert(pg_obj+1,"      this.pages = [\n")
			pg_obj_line = complines.index("      this.pages = [\n")
			complines.insert(pg_obj_line+1,"      { title: 'Logout',cls: 'power', component: 'LoginPage' },\n")
			complines.insert(pg_obj_line+2,"      ];\n")
			if notifyvalue == 'true':
				pg_obj_line = complines.index("      this.pages = [\n")
				complines.insert(pg_obj_line+1,"      { title: 'Notice Board',cls: 'notifications', component: NotificationPage },\n")
			txview = json.loads(r['views'][0]['tx'])
			rpview = json.loads(r['views'][0]['rp'])
			if txview:
				pg_obj_line = complines.index("      this.pages = [\n")
				for i, item in enumerate(txview):
					menu = Menu.objects.filter(id = item)
					if menu:
						pagetitle = menu[0].transactionview.identifiers
						complines.insert(pg_obj_line+1,"      { title: '"+menu[0].title.title()+"', component: "+pagetitle.capitalize()+"Page ,cls: '"+menu[0].iconcls+"'},\n")

			if rpview:
				pg_obj_line = complines.index("      this.pages = [\n")
				for i, item in enumerate(rpview):
					menu = Menu.objects.filter(id = item)
					if menu:
						pagetitle = menu[0].reportview.identifiers
						complines.insert(pg_obj_line+1,"      { title: '"+menu[0].title.title()+"', component: "+pagetitle.capitalize()+"Page ,cls: '"+menu[0].iconcls+"'},\n")

	else:
		page_obj = complines.index('    this.initializeApp();\n')
		complines.insert(page_obj+1,"      this.pages = [\n")
		complines.insert(page_obj+2,"      ];\n")
		if notifyvalue == 'true':
				pg_obj_line = complines.index("      this.pages = [\n")
				complines.insert(pg_obj_line+1,"      { title: 'Notice Board',cls: 'notifications', component: NotificationPage },\n")

		menuline = complines.index("      this.pages = [\n")
		for menu in home['home_menu']:
			title =""
			icls =""
			pagetitle=""
			title = menu['title'].lower()
			icls = menu['iconcls']
			if menu['typeofview'] == 'transactionview':
				pagetitle = menu['transactionview'].lower().replace(" ","")
			elif menu['typeofview'] == 'reportview':
				pagetitle = menu['reportview'].lower().replace(" ","")

			complines.insert(menuline+1,"      { title: '"+title.capitalize()+"',cls: '"+icls+"' , component: "+pagetitle.capitalize()+"Page },\n")


	with open(filePath+"ionicapps/"+ptitle+"/src/app/app.component.ts", "w") as com:
		for line1 in complines:
			com.write(line1)

	with open(filePath+"ionicapps/"+ptitle+"/src/app/app.html", "w") as app:
		for line2 in apphtml:
			app.write(line2)


def appmoduleincludeTs(ptitle,fileName):
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


def gridmenupage(home,role,submenu):
	gmenuheader =""
	gmenubody=""
	gmenuhtml = ""
	menuextra = ""
	login = Login.objects.filter(project_id_id = home['pid'])
	if submenu:
		menuextra = """<ion-col col-1><ion-icon name="more" item-right (click)="presentPopover($event)" class="more_icon"></ion-icon></ion-col>"""
	else:
		menuextra= """<ion-thumbnail item-end><button ion-button icon-only item-right (click)="logout()" class="icon-button"><ion-icon name="power"></ion-icon></button></ion-thumbnail>"""

	if login:
		gmenuheader = """<ion-header><ion-navbar color="primary"><ion-row><ion-title>"""+home['p_title'].title()+"""</ion-title>"""+menuextra+"""</ion-row></ion-navbar></ion-header>"""
	else:
		menuextra = ""
		if submenu:
			menuextra = """<ion-thumbnail item-end><button ion-button icon-only item-right (click)="submenu()" class="icon-button"><ion-icon name="more"></ion-icon></button></ion-thumbnail>"""
		gmenuheader = """<ion-header><ion-navbar color="primary"><ion-row><ion-title>"""+home['p_title'].title()+"""</ion-title>"""+menuextra+"""</ion-row></ion-navbar></ion-header>"""

	

	if home['column'] == "one":
		width = "col-12"
		css = "d-"
	elif home['column'] == "two":
		width = "col-6"
		css ="s-"
	else:
		width ="col-4"
		css ="d-"

	gmenubody = """<ion-content padding class="background"><ion-grid><ion-row wrap><ion-col """+width+""" *ngFor="let page of this.grid"><div class="card """+css+"""one" (click)="openPage(page)"><div class="card-block """+css+"""two"><div class="centered"><ion-icon name={{page.cls}} class="icon"></ion-icon></div></div><div class="card-footer"><div class="container"><div class="centered">{{page.title}}</div></div></div></div></ion-col></ion-row></ion-grid></ion-content>"""
	gmenuhtml = gmenuheader+gmenubody
	page = homepage(home['menutype'],home['project_id'],gmenuhtml)
	try:
		gridts = gridtsinclude(home['project_id'],home,role)
	except Exception as e:
		raise Exception(e)

	modulets = appmoduleincludeTs(home['project_id'],home['menutype'])
	appcom = gridappcomponent(home['project_id'])
	popup = popuppage(submenu,home,login)
	return "success"

def popuppage(submenu,home,login):
	ptitle = home['project_id']
	if not os.path.exists(filePath+"ionicapps/"+ptitle+"/src/pages/searchmodal/popover.html"):
		os.makedirs(filePath+"ionicapps/"+ptitle+"/src/pages/searchmodal/popover.html")

	submenustart = """<div *ngIf="!searchEnabled">"""	
	submenuend = """</div>"""
	submenubody = """"""

	if submenu:
		for sub in submenu:
			pageid=""
			if sub.menuaction == 'menu':
				print "arun"
				if sub.pageValue.transactionview:
					pageid = sub.pageValue.transactionview.identifiers
					print pageid
				elif sub.pageValue.reportview:
					pageid = sub.pageValue.reportview.identifiers

				submenubody += """<button ion-item (click)="redirectpage('redirect','"""+pageid+"""')">"""+sub.Caption+"""</button>"""
			elif sub.menuaction == 'other':
				pass

		if login:
			submenubody += """<button ion-item (click)="logout()">Log Out</button>"""	

	submenuhtml = submenustart+submenubody+submenuend


					

		

	html ="""<ion-list no-lines style="margin:5px">"""+submenuhtml+"""<div *ngIf="searchEnabled"><button ion-item (click)="view('view')">View</button><button ion-item (click)="view('modify')">Modify</button></div></ion-list>"""

	Html_file= open(filePath+"ionicapps/"+ptitle+"/src/pages/searchmodal/popover.html","w")
	Html_file.write(html)


def gridtsinclude(ptitle,home,role):
	with open(filePath+"static/ionicsrc/grid/grid.ts") as f:
		gridlines = f.readlines()

	grid = gridlines.index("import { HomePage } from '../home/home';\n")
	try:
		gInfo = GeneralInfo.objects.get(key = 'notification',project_id_id = home['pid'])
		notifyvalue = gInfo.value.lower()
		if (notifyvalue == 'true'):
			gridlines.insert(grid+1, "import { NotificationPage } from '../notification/notification';\n")
	except Exception as e:
		print e
		notifyvalue =""

	for menu in home['home_menu']:
		title =""
		icon=""
		title = menu['title'].lower()
		if menu['typeofview'] == 'transactionview':
			pagetitle = menu['transactionview'].lower().replace(" ","")
		elif menu['typeofview'] == 'reportview':
			pagetitle = menu['reportview'].lower().replace(" ","")

		gridlines.insert(grid, "import { "+pagetitle.capitalize()+"Page } from '../"+pagetitle+"/"+pagetitle+"';\n")

	login = Login.objects.filter(project_id_id = home['pid'])
	if login:
		for r in role:
			event = gridlines.index('\t  //array pages for grid menu \n')
			gridlines.insert(event+1, "     if(this.singleton.role == '"+r['rn']+"'){\n")
			page_obj = gridlines.index("     if(this.singleton.role == '"+r['rn']+"'){\n")
			gridlines.insert(page_obj+1,"      }\n")
			pg_obj = gridlines.index("     if(this.singleton.role == '"+r['rn']+"'){\n")
			gridlines.insert(pg_obj+1,"      this.grid = [\n")
			pg_obj_line = gridlines.index("      this.grid = [\n")
			gridlines.insert(pg_obj_line+1,"      ];\n")
			if notifyvalue == 'true':
				pg_obj_line = gridlines.index("      this.grid = [\n")
				gridlines.insert(pg_obj_line+1,"      { title: 'Notice Board', component: NotificationPage,cls: 'notifications'  },\n")

			txview = json.loads(r['views'][0]['tx'])
			rpview = json.loads(r['views'][0]['rp'])
			if txview:
				pg_obj_line = gridlines.index("      this.grid = [\n")
				for i, item in enumerate(txview):

					menu = Menu.objects.filter(id = item)
					if menu:
						pagetitle = menu[0].transactionview.identifiers
						gridlines.insert(pg_obj_line+1,"      { title: '"+menu[0].title.title()+"', component: "+pagetitle.capitalize()+"Page ,cls: '"+menu[0].iconcls+"'},\n")

			if rpview:
				pg_obj_line = gridlines.index("      this.grid = [\n")
				for i, item in enumerate(rpview):

					menu = Menu.objects.filter(id = item)
					if menu:
						pagetitle = menu[0].reportview.identifiers
						gridlines.insert(pg_obj_line+1,"      { title: '"+menu[0].title.title()+"', component: "+pagetitle.capitalize()+"Page ,cls: '"+menu[0].iconcls+"'},\n")

	else:
		page_obj = gridlines.index('      this.userdetails = navParams.get("");\n')
		gridlines.insert(page_obj+1,"      this.grid = [\n")
		gridlines.insert(page_obj+2,"      ];\n")
		if notifyvalue == 'true':
				pg_obj_line = gridlines.index("      this.grid = [\n")
				gridlines.insert(pg_obj_line+1,"      { title: 'Notice Board', component: NotificationPage,cls: 'notifications'  },\n")

		menuline = gridlines.index("      this.grid = [\n")
		for menu in home['home_menu']:
			title =""
			icls =""
			pagetitle=""
			title = menu['title'].lower().replace(" ","")
			icls = menu['iconcls']
			if menu['typeofview'] == 'transactionview':
				pagetitle = menu['transactionview'].lower().replace(" ","")
			elif menu['typeofview'] == 'reportview':
				pagetitle = menu['reportview'].lower().replace(" ","")

			gridlines.insert(menuline+1,"      { title: '"+title.title()+"',cls: '"+icls+"' , component: "+pagetitle.capitalize()+"Page },\n")



	with open(filePath+"ionicapps/"+ptitle+"/src/pages/grid/grid.ts", "w") as f1:
		for gline in gridlines:
			f1.write(gline)

	firstpage = first_page(ptitle,home['pid'],'grid')
	print "first_name"
	if login:
		logoutinclude(ptitle,home)

def first_page(ptitle,pid,page):
	print "first"
	print page
	try:
		fst = RootPage.objects.get(project_id = pid)
		print fst.pageoption
		if fst.pageoption == 'default':
			firstpage_name = page
		else:
			menu = fst.pageValue
			print menu
			if menu.transactionview:
				firstpage_name = menu.transactionview.identifiers
			elif menu.reportview:
				firstpage_name = menu.reportview.identifiers

		if os.path.exists(filePath+"ionicapps/"+ptitle+"/src/pages/login/login.ts"):
			with open(filePath+"ionicapps/"+ptitle+"/src/pages/login/login.ts", "r") as file :
				filedata = file.read()

				# Replace the target string
			filedata = filedata.replace('SidemenuPage',firstpage_name.capitalize()+'Page')
			filedata = filedata.replace('sidemenu', firstpage_name)
			with open(filePath+"ionicapps/"+ptitle+"/src/pages/login/login.ts", "w") as file:
				file.write(filedata)
	except Exception as e:
		print e
		raise Exception('Root Page Setting Error In Project.Please Check.')

def logoutinclude(ptitle,home):
	if os.path.exists(filePath+"ionicapps/"+ptitle+"/src/pages/grid/grid.ts"):
		with open(filePath+"ionicapps/"+ptitle+"/src/pages/grid/grid.ts", "r") as file :
			filedata = file.read()

		# Replace the target string
		filedata = filedata.replace('HomePage', 'LoginPage')
		filedata = filedata.replace('home', 'login')
		with open(filePath+"ionicapps/"+ptitle+"/src/pages/grid/grid.ts", "w") as file:
			file.write(filedata)


def gridappcomponent(ptitle):
	complines = ["import { Component, ViewChild } from '@angular/core';\n", "import { Nav, Platform ,AlertController} from 'ionic-angular';\n", "import { StatusBar } from '@ionic-native/status-bar';\n", "import { SplashScreen } from '@ionic-native/splash-screen';\n", "import { Storage } from '@ionic/storage';\n", "import { ModalController } from 'ionic-angular';\n", "import { MenuController } from 'ionic-angular';\n", "import { IonicApp} from 'ionic-angular';\n", "import { ToastController } from 'ionic-angular';\n","import { OneSignal } from '@ionic-native/onesignal';\n","import { SingletonProvider } from '../providers/singleton/singleton';\n","import { NotifyProvider } from '../providers/notify/notify';\n", '\n', "import { HomePage } from '../pages/home/home';\n", '\n', '@Component({\n', "  templateUrl: 'app.html'\n", '})\n', 'export class MyApp {\n', '  @ViewChild(Nav) nav: Nav;\n', '  rootPage: any = HomePage;\n', '  UserDetails:any;\n', '  alert:any;\n', '  pages: Array<{title: string,cls: string, component: any}>;\n', '\n', '  constructor(public platform: Platform,private alertCtrl: AlertController,public singleton:SingletonProvider,public statusBar: StatusBar,public modal:ModalController,public menuCtrl:MenuController,public ionicApp:IonicApp,public toastCtrl: ToastController, public splashScreen: SplashScreen, public storage: Storage,private oneSignal: OneSignal,public notify:NotifyProvider) {\n', '    this.initializeApp();\n', '}\n', '   initializeApp() {\n', '    this.platform.ready().then(() => {\n', '      // Okay, so the platform is ready and our plugins are available.\n', '      // Here you can do any higher level native things you might need.\n', '     // let status bar overlay webview\n', '\t\tthis.statusBar.overlaysWebView(false);\n', '\t\t// set status bar to white\n', "\t\tthis.statusBar.backgroundColorByHexString('#000000');\n", "\t\tthis.oneSignal.startInit(this.singleton.apikey, this.singleton.senderid);\n","\t\tthis.oneSignal.inFocusDisplaying(this.oneSignal.OSInFocusDisplayOption.Notification);\n",'\t\tthis.oneSignal.handleNotificationReceived().subscribe((data) => {\n','\t\t // do something when notification is received\n','\t\t\tthis.notify.notificationIndb(data);\n','\t\t});\n','\t\tthis.oneSignal.handleNotificationOpened().subscribe((data) => {\n','\t\t  // do something when a notification is opened\n','\t\t\tthis.notify.notificationIndb(data);\n','\t\t});\n',"\t\tthis.oneSignal.endInit();\n", '      \tthis.splashScreen.hide();\t\n', '\t    this.platform.registerBackButtonAction(() => {\n', '\t\t         let ready;\n', '                 let activePortal = this.ionicApp._loadingPortal.getActive() ||\n', '                 this.ionicApp._modalPortal.getActive() ||\n', '                 this.ionicApp._toastPortal.getActive() ||\n', '                 this.ionicApp._overlayPortal.getActive();\n', '                 if (activePortal) {\n', '                     ready = false;\n', '                     activePortal.dismiss();\n', '                     activePortal.onDidDismiss(() => { ready = true; });\n', '                     return;\n', '                  }\n', '                  if (this.menuCtrl.isOpen()) {\n', '                     this.menuCtrl.close();\n', '                     return;\n', '                   }\n', '                    let view = this.nav.getActive();\n', '                    let page = view ? this.nav.getActive().instance : null;\n', '                     if(this.nav.canGoBack()){\n', '                        this.nav.pop();\n', '                     }else{\n', '                         if(this.alert){\n', '                           this.alert.dismiss();\n', '                           this.alert =null;\n', '                     }else{\n', '                          this.showAlert();\n', '                     }\n', '                  }\n', '           }, 1);\n', '    });\n', '  }\n', '   \n', '   showAlert() {\n', '           this.alert = this.alertCtrl.create({\n', "            title: 'Exit?',\n", "            message: 'Do you want to exit the app?',\n", '                buttons: [\n', '                 {\n', "                     text: 'Cancel',\n", "                     role: 'cancel',\n", '                     handler: () => {\n', '                     this.alert =null;\n', '                  }\n', '                  },\n', '                 {\n', "                     text: 'Exit',\n", '                     handler: () => {\n', '                     this.platform.exitApp();\n', '                  }\n', '               }\n', '            ]\n', '        });\n', '       this.alert.present();\n', '       }\n', '\n', '      showToast() {\n', '           alert("Press Again to exit");\n', '       }\n', '  }\n', '\n']

	with open(filePath+"ionicapps/"+ptitle+"/src/app/app.component.ts", "w") as com:
		for line1 in complines:
			com.write(line1)
