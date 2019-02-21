# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from Mobilebuilder.decorators import myuser_login_required 
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponseRedirect, HttpResponse,HttpResponseBadRequest
from django.shortcuts import render
from django.forms import modelformset_factory
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
from itertools import chain
from django.conf import settings
import os

from .models import Notification,NotificationConfiguration,NotificationButtons
from .forms import NotificationForm,NotificationConfigurationForm,NotificationButtonsForm
from .serializers import TxviewSerializer,ReportviewSerializer,ButtonSerializer,NotificationSerializer
from project.models import Projectwiseusersetup,Project
from rolesetup.models import Role
from transactionview.models import Transactionview,Component
from transactionview.serializers import EpostComponentSerializer
from transaction.models import Transaction
from reportview.models import Report

# Create your views here.
@myuser_login_required
def notificationindex(request):
    element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])              
    projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])
    if element.setasdefaultproject or request.session['projectid']:
        project_title = element.project_id.title
    
    projectid = request.session['projectid']

    try:
        notificationObj = Notification.objects.filter(projectid=projectid)
    except Notification.DoesNotExist:
        notificationObj= None
    
    try:
        notificationObjJson = Notification.objects.filter(projectid=projectid,creatingJson = False)
    except Notification.DoesNotExist:
        notificationObjJson= None


    if request.method == 'POST':
        form = NotificationForm(request.POST)
        print form.is_valid()
        print form.errors
        if form.is_valid():
            try:
                newForm = form.save(commit=False)
                newForm.creatingJson = False
                newForm.save()
                return HttpResponseRedirect('/notification/notificationindex/')
            except:
                return HttpResponseBadRequest("Error while saving notification")

        else:
            return HttpResponseBadRequest("Notification name already exist")
    else:  
        form = NotificationForm()
        return render(request, 'notificationindex.html',locals())      

@myuser_login_required
def delNotification(request,notificationid):
    try:
        query = Notification.objects.get(id=notificationid)
        query.delete()
    except:
         return HttpResponseBadRequest("Error while deleting notification")

    return HttpResponseRedirect('/notification/notificationindex/')

@csrf_exempt
def notificationEdit(request,notificationid):    
   
    notification = Notification.objects.get(id=notificationid)    
    print notification

    if request.method == 'POST':
        form = NotificationForm(request.POST,instance=notification)
        print form.is_valid()
        print form.errors
        if form.is_valid():
            try:
                newForm = form.save(commit=False)
                newForm.creatingJson = False
                newForm.save()
                return HttpResponse("Success")
            except:
                return HttpResponse("Error2")

        else:
            return HttpResponse("Error1")
    else:  
        form = NotificationForm(instance=notification)
        return render(request, 'notificationEditModal.html',locals())   


@myuser_login_required
def notificationConfig(request,notificationid):
    element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])              
    projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])
    if element.setasdefaultproject or request.session['projectid']:
        project_title = element.project_id.title

    notification = Notification.objects.get(id=notificationid)
    
    try:
        notificationStages =  NotificationConfiguration.objects.filter(notification_id=notificationid)
    except NotificationConfiguration.DoesNotExist:
        notificationStages = None

    return render(request, 'notificationstages.html',locals()) 

def getCombinedQuerySetChoices(request,processType,notificationid):
   
    pid = request.session['projectid']

    txviews = Transactionview.objects.filter(projectid_id=pid)
    txviews_serializer = TxviewSerializer(instance=txviews,many=True)
    txviews_serializer_json = json.dumps(txviews_serializer.data)
    
    reportviews = Report.objects.filter(project_id=pid)
    reportview_serializer = ReportviewSerializer(instance=reportviews,many=True)
    reportview_serializer_json = json.dumps(reportview_serializer.data)

    buttons = NotificationButtons.objects.filter(notification_configuration_id__in = NotificationConfiguration.objects.filter(notification_id=notificationid))
    buttons_serializer = ButtonSerializer(instance=buttons,many=True)
    buttons_serializer_json = json.dumps(buttons_serializer.data) 
    
    # result_list = list(chain(txviews, reportviews,buttons)) 
      
   
    if processType == "Buttons":
        return buttons_serializer_json
    elif processType == "Message":
        # context = {"txviews": txviews,"reportviews": reportviews, "buttons": buttons}
        # status_process_serializer = StatusProcessSerializer(context=context)
        # print status_process_serializer.context 
        
         
        
        status_process_serializer_json =  {
            'type':'Message',
            'txview':txviews_serializer_json,
            'report':reportview_serializer_json,
            'buttons':buttons_serializer_json,
        }
        
        return json.dumps(status_process_serializer_json)  



NotificationButtonsFormSet = modelformset_factory(NotificationButtons,form = NotificationButtonsForm,can_delete=True,extra=1)

@csrf_exempt
def addStage(request,notificationid):
    pid = request.session['projectid']
    result_list = [
        {
            u'type': u'',
            u'id': '',
            u'value': u'',
            u'title': u'----------'
        }
    ]
    
    stageform = NotificationConfigurationForm(initial={'from_date':datetime.now(),'to_date':datetime.now()},views = result_list)
    stageform.fields['role'].queryset = Role.objects.filter(projectid_id=pid)
    stageform.fields['from_date'].queryset = Component.objects.none()
    stageform.fields['to_date'].queryset = Component.objects.none()
    stageform.fields['basicid_field'].queryset = Component.objects.none()
    stageform.fields['user_field'].queryset = Component.objects.none()
    dd = NotificationConfiguration.objects.filter(notification_id=notificationid)
    formset = NotificationButtonsFormSet(queryset=NotificationButtons.objects.none(),form_kwargs={'stage':dd})
    return render(request,'stagesModal.html',locals())

@csrf_exempt
def saveStage(request,notificationid):
    pid = request.session['projectid']
    processType = request.POST.get('status_process_type')

    notificationObj = Notification.objects.get(id=notificationid)

    result_list_json = getCombinedQuerySetChoices(request,processType,notificationid)
    result_list = json.loads(result_list_json)

    stageform = NotificationConfigurationForm(request.POST,views = result_list)
    
    if stageform.is_valid():
        newform = stageform.save()
        notificationObj.creatingJson = False
        notificationObj.save()
        dd = NotificationConfiguration.objects.filter(notification_id=notificationid)
        formset = NotificationButtonsFormSet(request.POST,queryset=NotificationButtons.objects.none(),form_kwargs={'stage':dd})
        for form in formset:
            if form.is_valid() and form.cleaned_data:                
                instance = form.save(commit=False)
                instance.notification_configuration_id = newform.id
                instance.notification_id = notificationid
                print instance.stage
                try:
                    instance.save()
                except Exception as e:
                    print e
                    return HttpResponse("Button1") #dublicate Button Name under one stage
                
            # else:
            #     print "***ELSE******"
            #     print form.is_valid()
            #     print form.cleaned_data
            #     print form.errors
            #     return HttpResponse("Button2") #form is not valid  means some req field was left out.

        return HttpResponse("Success")
    else:
        print stageform.errors
        return HttpResponse("Stage")


@myuser_login_required
def deleteStage(request,notificationstageid):
    try:
        query = NotificationConfiguration.objects.get(id=notificationstageid)
        notificationId = query.notification_id
        query.delete()
    except:
         return HttpResponseBadRequest("Error while deleting notification")

    return HttpResponseRedirect('/notification/notificationconfig/%s' %(notificationId))

@csrf_exempt
def updateStage(request,notificationstageid):
    pid = request.session['projectid']
    notificationStage = NotificationConfiguration.objects.get(id=notificationstageid)
    
    notificationid = notificationStage.notification_id
    notificationObj = Notification.objects.get(id=notificationid)
   
    if request.method == 'POST':
        statusProcessType = request.POST.get('status_process_type')
    
        result_list_json = getCombinedQuerySetChoices(request,statusProcessType,notificationid)
        result_list = json.loads(result_list_json)
        stageform = NotificationConfigurationForm(request.POST,instance=notificationStage,views= result_list)
        
        if stageform.is_valid():
            newform = stageform.save()
            notificationObj.creatingJson = False
            notificationObj.save()
            print "NEW FORM ID",newform.id
            dd = NotificationConfiguration.objects.filter(notification_id=notificationid)
            formset = NotificationButtonsFormSet(request.POST,queryset=NotificationButtons.objects.filter(notification_configuration_id=notificationstageid),form_kwargs={'stage':dd})
            
            for form in formset:
                if form.is_valid() and form.cleaned_data.get('DELETE') and form.instance.pk:
                    print "************DELETE*******************"
                    print form.instance.pk
                    form.instance.delete()
                elif form.is_valid() and form.cleaned_data:
                    print "************VALID*********************"
                    print form.is_valid()
                  
                    instance = form.save(commit=False)
                    instance.notification_configuration_id = newform.id
                    instance.notification_id = notificationid
                    print instance.stage
                    try:
                        instance.save()
                    except Exception as e:
                        print e
                        return HttpResponse("Button1")
                
                  
            return HttpResponse("Success")

           
        else:
            print stageform.errors
            return HttpResponse("Stage")
    
    else:

        statusProcessType = notificationStage.status_process_type
        statusProcess = notificationStage.status_process
        choosedStatusProcess = notificationStage.choosed_status_process

        statusProcessArray = statusProcess.split('-')
        
        result_list_json = getCombinedQuerySetChoices(request,statusProcessType,notificationid)
        result_list = json.loads(result_list_json)

        stageform = NotificationConfigurationForm(instance=notificationStage,views= result_list)  
    
        stageform.fields['role'].queryset = Role.objects.filter(projectid_id=pid)
        
        if choosedStatusProcess == "Transaction":
            stageform.fields['from_date'].queryset = Component.objects.filter(transactionviewid_id=statusProcessArray[0])
            stageform.fields['to_date'].queryset = Component.objects.filter(transactionviewid_id=statusProcessArray[0])
            stageform.fields['basicid_field'].queryset = Component.objects.filter(transactionviewid_id=statusProcessArray[0])
            stageform.fields['user_field'].queryset = Component.objects.filter(transactionviewid_id=statusProcessArray[0])
        else:
            stageform.fields['from_date'].queryset = Component.objects.none()
            stageform.fields['to_date'].queryset = Component.objects.none()
            stageform.fields['basicid_field'].queryset = Component.objects.none()
            stageform.fields['user_field'].queryset = Component.objects.none()
    
        dd = NotificationConfiguration.objects.filter(notification_id=notificationid)
        formset = NotificationButtonsFormSet(queryset=NotificationButtons.objects.filter(notification_configuration_id=notificationstageid),form_kwargs={'stage':dd})
        return render(request, 'stagesModal.html',locals())  


@csrf_exempt
def processType(request):
    processType =  request.GET.get('ProcessType')
    notificationId = request.GET.get('notificationId')
    result = getCombinedQuerySetChoices(request,processType,notificationId)
    print result
   
    return HttpResponse(result)


@csrf_exempt
def getTxviewField(request,txviewid):
	try:
		component = Component.objects.filter(transactionviewid_id = txviewid)
		tablegroup_serializer = EpostComponentSerializer(instance=component,many=True)
		tablegroup_serializer_json = json.dumps(tablegroup_serializer.data)
		return HttpResponse(tablegroup_serializer_json)
	except Exception as e:
		print e
		return HttpResponseBadRequest("error")


@csrf_exempt
def generateProcess(request):
    try:
        pid = request.session['projectid']
        projectObj = Project.objects.get(id=pid)
        
        filePath = settings.MEDIA_ROOT
        
        notificationObj = Notification.objects.filter(projectid_id = pid)
        notification_serializer = NotificationSerializer(instance=notificationObj,many=True)
        notification_serializer_json = json.dumps(notification_serializer.data)
        print notification_serializer_json

        if not os.path.exists(filePath+"static/ionicmeta/"+projectObj.slug+"/Notification"):
            os.makedirs(filePath+"static/ionicmeta/"+projectObj.slug+"/Notification")
        
        json_file= open(filePath+"static/ionicmeta/"+projectObj.slug+"/Notification/notification.json","w")
        json_file.write(notification_serializer_json)
        json_file.close()

        for query in notificationObj:
            query.creatingJson = True
            query.save()

        return HttpResponse("success")
    except Exception as e:
        print e
        return HttpResponseBadRequest


    



   