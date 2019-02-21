# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .models import TxnMappingForEvent
from .forms import TxnMappingForEventForm
from .serializers import ComponentEventSerializer,TxnMappingForEventSerializer
from project.models import Project
from transaction.models import Transaction
from transactionview.models import Transactionview,Component

import json
from django.http import HttpResponseRedirect, HttpResponse,HttpResponseBadRequest
from slugify import slugify
import os
from django.conf import settings



filePath = settings.MEDIA_ROOT


# Create your views here.

def mapTxnFields(request):
    pid = request.session['projectid']

    try:
        eventObj = TxnMappingForEvent.objects.get(project_id= pid)
        eventform =  TxnMappingForEventForm(instance = eventObj)
        eventform.fields['txview'].queryset = Transactionview.objects.filter(projectid_id = pid)
        eventform.fields['event_title'].queryset = Component.objects.filter(transactionviewid_id = eventObj.txview_id )
        eventform.fields['event_desc'].queryset = Component.objects.filter(transactionviewid_id = eventObj.txview_id)
        eventform.fields['event_location'].queryset = Component.objects.filter(transactionviewid_id = eventObj.txview_id)
        eventform.fields['event_start_day'].queryset = Component.objects.filter(transactionviewid_id = eventObj.txview_id)
        eventform.fields['event_start_time'].queryset = Component.objects.filter(transactionviewid_id = eventObj.txview_id)
        eventform.fields['event_end_day'].queryset = Component.objects.filter(transactionviewid_id = eventObj.txview_id)
        eventform.fields['event_end_time'].queryset = Component.objects.filter(transactionviewid_id = eventObj.txview_id)
    except TxnMappingForEvent.DoesNotExist:
        eventObj = None
        eventform =  TxnMappingForEventForm()
        eventform.fields['txview'].queryset = Transactionview.objects.filter(projectid_id = pid)
        eventform.fields['event_title'].queryset = Component.objects.none()
        eventform.fields['event_desc'].queryset = Component.objects.none()
        eventform.fields['event_location'].queryset = Component.objects.none()
        eventform.fields['event_start_day'].queryset = Component.objects.none()
        eventform.fields['event_start_time'].queryset = Component.objects.none()
        eventform.fields['event_end_day'].queryset = Component.objects.none()
        eventform.fields['event_end_time'].queryset = Component.objects.none()

    return render(request, 'eventconfiguration.html',locals())

def getcomponents(request,txviewid):
    try:
        compObj =  Component.objects.filter(transactionviewid_id = txviewid).values('id','title')
        comp_serializer = ComponentEventSerializer(instance=compObj,many=True)
        comp_serializer_json = json.dumps(comp_serializer.data)
    except Exception as e:
        print e
        comp_serializer_json =  None

    return HttpResponse(comp_serializer_json)

def addEvent(request):
    pid = request.session['projectid']
    projectObj = Project.objects.get(id=pid)
    regex_pattern = r'[^-a-z0-9_]+'
    try:
        eventObj = TxnMappingForEvent.objects.get(project_id= pid)
        eventform =  TxnMappingForEventForm(request.POST or None,instance = eventObj)
    except TxnMappingForEvent.DoesNotExist:
        eventObj = None
        eventform =  TxnMappingForEventForm(request.POST)
    
    eventTitle = request.POST.get('title')
        
    if eventform.is_valid():
        newForm =  eventform.save(commit=False)
        newForm.project_id = pid
        newForm.slug = slugify(eventTitle, separator='_', regex_pattern=regex_pattern)
        newForm.save()

        #JSON CREATION
        query = TxnMappingForEvent.objects.get(id = newForm.id)
        query_serializer = TxnMappingForEventSerializer(instance=query)
        query_serializer_json = json.dumps(query_serializer.data)

        if not os.path.exists(filePath+"static/ionicmeta/"+projectObj.slug+"/calendareventjson"):
			os.makedirs(filePath+"static/ionicmeta/"+projectObj.slug+"/calendareventjson")

        json_file= open(filePath+"static/ionicmeta/"+projectObj.slug+"/calendareventjson/calendarevent.json","w")
        json_file.write(query_serializer_json)
        json_file.close()


        return HttpResponse("success")
    else:
        print eventform.errors
        return  HttpResponse("error")

def deleteEvent(request,eventid):
    query =  TxnMappingForEvent.objects.get(id=eventid)
    query.delete()
    return HttpResponseRedirect('/eventconfiguration/mapTxnFields/')



    




     
    


