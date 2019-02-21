# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponseRedirect, HttpResponse,HttpResponseBadRequest
from django.shortcuts import render
from django.forms import modelformset_factory
import logging
logger = logging.getLogger(__name__)
from django.db import transaction as transaction_db
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from Mobilebuilder.decorators import myuser_login_required 
from slugify import slugify
from aldjemy.core import get_tables, get_engine
from sqlalchemy import *
from sqlalchemy import schema
import pandas, json
import MySQLdb
from django.db.models import Q

from schemageneration.views import generate_schema
from .models import Transaction
from authentication.models import userprofile
from project.models import Projectwiseusersetup
from transaction.models import Transaction,Txtabledetails,Txtablecomponentdetails,enumtitle,enumkeyvalue
from project.models import  Project
from schema.models import Db_connections_info, Db_profile
from schemageneration.models import GenerateSchemaTableComponent,GenerateSchemaComponent
from transactionview.models import Transactionview


from transaction.forms import UserTransForm,TableDetailsform,TableComponentform,EnumTitleform, EnumKeyValueform
from transaction.serializers import TransactionSerializer,TxtabledetailsSerializer,TxtablecomponentdetailsSerializer
# from Mobilebuilder.decorators import myadmin_login_required


# Create your views here.
@myuser_login_required
def transmain(request):
    element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])              
    projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])
    if element.setasdefaultproject or request.session['projectid']:
        project_title = element.project_id.title
        print project_title
        print element.userid_id
    return render(request, 'tempmain.html',locals())  

@myuser_login_required
def transindex(request):

    loginModel = userprofile.objects.get(is_user = True ,id = request.session['userid'])
    print request.session['userid']
    element =Projectwiseusersetup.objects.get(userid=loginModel.id,project_id = request.session['projectid'])
    projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])
    print projectselect
    if element:
        project_title = element.project_id.title
        projectid = element.project_id.id
        request.session['projectid'] = element.project_id.id
        print projectid
        transgroup =  Transaction.objects.filter(projectid = projectid)
        print transgroup       
    return render(request,'transindex.html',locals())     

@myuser_login_required
def delete(request ,txid):
    query = Transaction.objects.get(pk = txid)
    query.delete()
    return HttpResponseRedirect('/transindex/')    


@myuser_login_required
def tedit(request,transactionid):
    model =Transaction.objects.get(pk = transactionid)
    transactionname = model.txname
    transactiondes  = model.txdescription
    transactionid = model.id
    print transactionid
    form = UserTransForm(instance = model)
    return render(request,'transmodel.html',locals())    


@myuser_login_required
def tsave(request,transid):
    print request.POST
    model =Transaction.objects.get(pk = transid)
    if request.method == 'POST':
        projectid = model.projectid
        form = UserTransForm(request.POST,instance=model)
        print form.is_valid()
        print form.errors
        if form.is_valid():
           
            form.save()
            return HttpResponseRedirect('/transindex/')
        else:
            return HttpResponse('Error while creating transaction') 
    else:            

        return render(request,'transindex.html',locals())     

@csrf_exempt
def tranname_validation(request):
    print request.POST
    if request.method == 'POST':
        if request.POST.get('txname'):
            mailid = request.POST.get('txname')
            print mailid
            print request.session['projectid']  
        try:
            txname = Transaction.objects.get(txname=mailid,projectid_id=request.session['projectid'])
            print txname
        except Transaction.DoesNotExist:
            txname= None
        if txname:
            return HttpResponse ('This Transaction already exits')
        else:
            return HttpResponse ('')
    else:
         return render(request,'transindex.html',locals())    

@myuser_login_required
def switchproject(request,tprojectid):
    print tprojectid
    loginModel = userprofile.objects.get(is_user = True ,id = request.session['userid'])
    element =Projectwiseusersetup.objects.get(userid=loginModel.id,project_id_id = tprojectid )
    print element
    projectselect =Projectwiseusersetup.objects.filter(userid =request.session['userid'])
    print projectselect
    if element:
        project_title = element.project_id.title
        projectid = element.project_id.id
        request.session['projectid'] = tprojectid
        transgroup =  Transaction.objects.filter(projectid = projectid)
        print transgroup
        return HttpResponseRedirect('/transaction/transmain/')
    #return render(request,'transindex.html',locals())    

@myuser_login_required    
def saveform(request):
    projectid =  request.session['projectid'] 
    print  projectid      
    if request.method == 'POST':
        print 'hello'
        form = UserTransForm(request.POST)
        print form.is_valid()
        print form.errors
        if form.is_valid():
            newtransaction = form.save(commit=False)
            newtransaction.projectid_id =  projectid
            newtransaction.save()
            return HttpResponseRedirect('/transindex/')
        else:
            return HttpResponseBadRequest('Error while creating transaction')    
    else:    
        return render(request,'transindex.html',locals())     

@myuser_login_required
def getin(request,transid):
    request.session['transactionid'] = transid
    transactionid = request.session['transactionid']
    transaction_id = request.session['transactionid']
    print transactionid
    loginModel = userprofile.objects.get(is_user = True ,id = request.session['userid'])
    threads = userprofile.objects.all()
    json_data = serializers.serialize('json', threads)
    element =Projectwiseusersetup.objects.get(userid=loginModel.id,project_id = request.session['projectid'])
    project_title = element.project_id.title
    projectselect =Projectwiseusersetup.objects.filter(userid =request.session['userid'])
    tablegroup = Txtabledetails.objects.filter(transactionid_id = transid )
    tablegroup_serializer = TxtabledetailsSerializer(instance=tablegroup,many=True)
    tablegroup_serializer_json = json.dumps(tablegroup_serializer.data)
    tablegroup_serializer_json_obj = json.loads(tablegroup_serializer_json)
  
    print tablegroup_serializer_json[0]
    print tablegroup_serializer_json
    if request.method == 'POST':
        form = TableDetailsform(request.POST)
        if form.is_valid():
            newtable = form.save(commit=False)
            newtable.transactionid_id =transactionid
            newtable.save()
            return HttpResponseRedirect('/transaction/transdetails/%s' %transactionid )
        else:
            return HttpResponseBadRequest('Error while creating transaction')
    else:
        form = TableDetailsform()             
        return render(request,'tabledetail.html',locals())     


def myModel_asJson(request):
    data =serializers.serialize('json', userprofile.objects.all())
    #data = '{"name": "mkyong","age": 30,"address": {"streetAddress": "88 8nd Street","city": "New York"},"phoneNumber": [{"type": "home","number": "111 111-1111"},{"type": "fax","number": "222 222-2222"}]}'
    #data = '{"name":crm","name":"connectedmarket","name":"gst"}'
    print data
    # print content
    return HttpResponse(data)
@csrf_exempt
def tabledetail(request):
   
    element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])              
    projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])
    project_title = element.project_id.title
    
    transaction_id = request.session['transactionid']
    transaction = Transaction.objects.get(id= transaction_id)
    tarn_title = transaction.txname
    project_id = request.session['projectid']
    print "pid", project_id
    print "tid",transaction_id

    table = Txtabledetails.objects.filter(Q(transactionid_id = transaction_id) & Q(projectid_id = project_id) & ~Q(status = "deleted"))
    print table
    table_ser =TxtabledetailsSerializer(instance=table,many=True)
    table_ser_json= json.dumps(table_ser.data)
    table_ser_json_obj = json.loads(table_ser_json) 
    	
    tableForm = TableDetailsform()
    try:
        primaryTab = Txtabledetails.objects.get(projectid_id=project_id,transactionid_id = transaction_id,isprimary = True)
    except Txtabledetails.DoesNotExist:
        primaryTab = None

    if primaryTab:
        tableForm.fields['db_type'].initial=primaryTab.db_type

    return render(request, 'tabledetail.html',locals()) 

def addtable(request):
    regex_pattern = r'[^-a-z0-9_]+'
    
    transaction_id = request.session['transactionid']
    project_id = request.session['projectid']
    userid=request.session['userid']

    projectObj = Project.objects.get(id=project_id)
    try:
        viewObj = Transactionview.objects.get(transactionid_id = transaction_id)
    except Transactionview.DoesNotExist:
        viewObj = None

    if request.method == 'POST':
        try:
            tableForm = TableDetailsform(request.POST)
            if tableForm.is_valid():
                tabName = request.POST.get('tablename')
                givenTabslug = slugify(tabName, separator='_', regex_pattern=regex_pattern)
                if projectObj.table_append_by_underscore == True:
                    try:
                        finalTabSlug =  str(viewObj.identifiers)+"_"+givenTabslug
                    except Exception as e:
                        return HttpResponse("slug")
                else:
                    finalTabSlug = givenTabslug

                try:
                    primaryTab = Txtabledetails.objects.get(projectid_id=project_id,transactionid_id = transaction_id,isprimary = True)
                except Txtabledetails.DoesNotExist:
                    primaryTab = None

                new_table = tableForm.save(commit=False)
                

                new_table.table_slug = finalTabSlug
                new_table.status = "new"
                new_table.user_id = userid

                if primaryTab:
                    new_table.isprimary = False
                    new_table.parent = primaryTab
                else:
                    new_table.isprimary = True
                
                try:
                    new_table.save()
                    print new_table.isprimary
                
                    if new_table.isprimary == True:
                        Txtablecomponentdetails.objects.create(title='is cancelled',txtabledetailid = new_table,columnname='is cancelled',datatype='CharField',maxlength=100,no_of_decimal_digits=0,field_slug='is_cancelled', isdbfield=True, isnull= True, is_system_component = True, db_type=new_table.db_type,status="new",user_id=userid)
                        Txtablecomponentdetails.objects.create(title='unique id field',txtabledetailid = new_table,columnname='unique id field',datatype='UUIDField',maxlength=100,no_of_decimal_digits=0,field_slug='unique_id_field', isdbfield=True, isnull= True, is_system_component = True, db_type=new_table.db_type,status="new",user_id=userid)
                        Txtablecomponentdetails.objects.create(title='created on',txtabledetailid = new_table,columnname='created on',datatype='DateTimeField',maxlength=100,no_of_decimal_digits=0,field_slug='created_on', isdbfield=True, isnull= True, is_system_component = True, db_type=new_table.db_type,status="new",user_id=userid)
                        Txtablecomponentdetails.objects.create(title='created by',txtabledetailid = new_table,columnname='created by',datatype='CharField',maxlength=100,no_of_decimal_digits=0,field_slug='created_by', isdbfield=True, isnull= True, is_system_component = True, db_type=new_table.db_type,status="new",user_id=userid)
                        Txtablecomponentdetails.objects.create(title='modified on',txtabledetailid = new_table,columnname='modified on',datatype='DateTimeField',maxlength=100,no_of_decimal_digits=0,field_slug='modified_on', isdbfield=True, isnull= True, is_system_component = True, db_type=new_table.db_type,status="new",user_id=userid)
                        Txtablecomponentdetails.objects.create(title='modified by',txtabledetailid = new_table,columnname='modified by',datatype='CharField',maxlength=100,no_of_decimal_digits=0,field_slug='modified_by', isdbfield=True, isnull= True, is_system_component = True, db_type=new_table.db_type,status="new",user_id=userid)
                        Txtablecomponentdetails.objects.create(title='upstream_txview_ref_id',txtabledetailid = new_table,columnname='upstream_txview_ref_id',datatype='IntegerField',maxlength=100,no_of_decimal_digits=0,field_slug='upstream_txview_ref_id', isdbfield=True, isnull= True, is_system_component = True, db_type=new_table.db_type,status="new",user_id=userid)
                        Txtablecomponentdetails.objects.create(title='post_tx_title',txtabledetailid = new_table,columnname='post_tx_title',datatype='CharField',maxlength=100,no_of_decimal_digits=0,field_slug='post_tx_title', isdbfield=True, isnull= True, is_system_component = True, db_type=new_table.db_type,status="new",user_id=userid)
                        Txtablecomponentdetails.objects.create(title='userid',txtabledetailid = new_table,columnname='userid',datatype='CharField',maxlength=100,no_of_decimal_digits=0,field_slug='userid', isdbfield=True, isnull= True, is_system_component = True, db_type=new_table.db_type,status="new",user_id=userid)
                        Txtablecomponentdetails.objects.create(title='projectid',txtabledetailid = new_table,columnname='projectid',datatype='CharField',maxlength=100,no_of_decimal_digits=0,field_slug='projectid', isdbfield=True, isnull= True, is_system_component = True, db_type=new_table.db_type,status="new",user_id=userid)
                        Txtablecomponentdetails.objects.create(title='ipadd',txtabledetailid = new_table,columnname='ipadd',datatype='CharField',maxlength=100,no_of_decimal_digits=0,field_slug='ipadd', isdbfield=True, isnull= True, is_system_component = True, db_type=new_table.db_type,status="new",user_id=userid)
                        Txtablecomponentdetails.objects.create(title='recid',txtabledetailid = new_table,columnname='recid',datatype='IntegerField',maxlength=100,no_of_decimal_digits=0,field_slug='recid', isdbfield=True, isnull= True, is_system_component = True, db_type=new_table.db_type,status="new",user_id=userid)
                        Txtablecomponentdetails.objects.create(title='versionid',txtabledetailid = new_table,columnname='versionid',datatype='CharField',maxlength=100,no_of_decimal_digits=0,field_slug='versionid', isdbfield=True, isnull= True, is_system_component = True, db_type=new_table.db_type,status="new",user_id=userid)
                        Txtablecomponentdetails.objects.create(title='roleid',txtabledetailid = new_table,columnname='roleid',datatype='CharField',maxlength=100,no_of_decimal_digits=0,field_slug='roleid', isdbfield=True, isnull= True, is_system_component = True, db_type=new_table.db_type,status="new",user_id=userid)               
                        Txtablecomponentdetails.objects.create(title='objectid',txtabledetailid = new_table,columnname='objectid',datatype='CharField',maxlength=100,no_of_decimal_digits=0,field_slug='objectid', isdbfield=True, isnull= True, is_system_component = True, db_type=new_table.db_type,status="new",user_id=userid)               
                        
                    return HttpResponse("Success")
                except Exception as e:
                    print e
                    return HttpResponse("Failure1")     

            else:	
                print tableForm.errors
                return HttpResponse("Failure2")
        except Exception as e:
            print e
    

def tabledetail_edit(request,tableeditid):
    
    regex_pattern = r'[^-a-z0-9_]+'
    transaction_id = request.session['transactionid']
    project_id = request.session['projectid']
    userid=request.session['userid']

    projectObj = Project.objects.get(id=project_id)
    try:
        viewObj = Transactionview.objects.get(transactionid_id = transaction_id)
    except Transactionview.DoesNotExist:
        viewObj = None

    query = Txtabledetails.objects.get(pk = tableeditid)
    
    if request.method =='POST':
        
        if query.status != "new" and query.status != "modified":
            GenerateSchemaTableComponent.objects.create(tablename=query.tablename,table_slug=query.table_slug,table_id=query.id,projectid_id= project_id,transactionid_id = transaction_id,user_id=userid,isprimary=query.isprimary)
        
        
        form = TableDetailsform(request.POST,instance = query)
        
        if form.is_valid():
            tabName = request.POST.get('tablename')

            givenTabslug = slugify(tabName, separator='_', regex_pattern=regex_pattern)
            if projectObj.table_append_by_underscore == True:
                finalTabSlug = str(viewObj.identifiers)+"_"+givenTabslug
            else:
                finalTabSlug = givenTabslug
            
            newtable = form.save(commit=False)
            newtable.table_slug = finalTabSlug
            newtable.user_id = userid
            if query.status != "new":
                newtable.status = "modified"

            try:
                newtable.save()
                
                table = Txtabledetails.objects.filter(Q(transactionid_id = transaction_id) & Q(projectid_id = project_id) & ~Q(status = "deleted"))
                table_ser =TxtabledetailsSerializer(instance=table,many=True)
                table_ser_json= json.dumps(table_ser.data)
                table_ser_json_obj = json.loads(table_ser_json)     
                return render(request,'tableMidPart.html',locals())
            
            except Exception as e:
                print e
                return HttpResponse('Failure1') 
                
        else:
            print form.errors
            return HttpResponse('Failure') 
    else:
        form = TableDetailsform(instance = query)
        return render(request,'tabledetailedit.html',locals())           

def tabledetail_delete(request,tableid):
    transaction_id = request.session['transactionid']
    transactionid = request.session['transactionid']
    project_id = request.session['projectid']
    # userid=request.session['userid']
    query = Txtabledetails.objects.get(pk = tableid)
    if query.status == "new":
        query.delete()
    else:
        try:
            geneatedSchemaObj = GenerateSchemaTableComponent.objects.get(projectid_id= project_id,transactionid_id = transaction_id,table_id=query.id)
            geneatedSchemaObj.delete()
        except GenerateSchemaTableComponent.DoesNotExist:
            geneatedSchemaObj = None

        query.status = "deleted"
        query.save()

        if query.isprimary == True:
            try:
                childTables = Txtabledetails.objects.filter(projectid_id=project_id,transactionid_id = transaction_id,isprimary =False)
            except Txtabledetails.DoesNotExist:
                childTables = None
            if childTables:
                for ctable in childTables:
                    try:
                        geneatedSchemaChildObj = GenerateSchemaTableComponent.objects.get(projectid_id= project_id,transactionid_id = transaction_id,table_id=ctable.id)
                        geneatedSchemaChildObj.delete()
                    except GenerateSchemaTableComponent.DoesNotExist:
                        geneatedSchemaChildObj = None
                    
                    ctable.status = "deleted"
                    ctable.save()

    return HttpResponseRedirect('/transaction/tabledetail/' )


def tablecomp_create(request,tableid):
    regex_pattern = r'[^-a-z0-9_]+'
    transactionid = request.session['transactionid']
    transaction_id = request.session['transactionid']
    project_id = request.session['projectid']
    userid=request.session['userid']
    tableObj = Txtabledetails.objects.get(id=tableid)
    projectObj = Project.objects.get(id=project_id)
    
    if request.method =='POST':
        fieldName = request.POST.get('columnname')
        
        givenColumnslug = slugify(fieldName, separator='_', regex_pattern=regex_pattern)
        if projectObj.table_append_by_underscore == True:
            finalColumnSlug = slugify(tableObj.tablename, separator='_', regex_pattern=regex_pattern)+"_"+givenColumnslug
        else:
            finalColumnSlug = givenColumnslug
        
        form = TableComponentform(request.POST)
        try:
            if form.is_valid():
                newField = form.save(commit=False)
                newField.txtabledetailid_id = tableid
                newField.is_system_component= False
                newField.field_slug =  finalColumnSlug
                newField.status = "new"
                newField.user_id = userid
                newField.save()

                return HttpResponse("Success")
            else:
                print form.errors
                return HttpResponse("Failure2")
        except Exception as e:
            print e
            return HttpResponse("Failure1")
    else:        
        form = TableComponentform()
        form.fields["db_type"].initial = tableObj.db_type
        try:
            enumObj = enumtitle.objects.filter(project_id_id= project_id)
        except enumtitle.DoesNotExist:
            enumObj = None
        print enumObj
        form.fields["enum"].queryset = enumObj
        return render(request,'tablecomponent.html',locals()) 


def tablecomponent_edit(request,tabcompid):
    query = Txtablecomponentdetails.objects.get(pk = tabcompid)
    print query

    regex_pattern = r'[^-a-z0-9_]+'
    transaction_id = request.session['transactionid']
    project_id = request.session['projectid']
    userid=request.session['userid']
    tableObj = Txtabledetails.objects.get(id=query.txtabledetailid_id)

    projectObj = Project.objects.get(id=project_id)
    
    if request.method =='POST':

        if query.status != "new" and query.status != "modified":
            GenerateSchemaComponent.objects.create(column_id=query.id,columnname=query.columnname,field_slug=query.field_slug,datatype=query.datatype,maxlength=query.maxlength,no_of_decimal_digits=query.no_of_decimal_digits,isdbfield=query.isdbfield,isnull=query.isnull)
        
        fieldName = request.POST.get('columnname')
        givenColumnslug = slugify(fieldName, separator='_', regex_pattern=regex_pattern)
        if projectObj.table_append_by_underscore == True:
            finalColumnSlug = slugify(tableObj.tablename, separator='_', regex_pattern=regex_pattern)+"_"+givenColumnslug
        else:
            finalColumnSlug = givenColumnslug
        form = TableComponentform(request.POST,instance = query)
        if form.is_valid():
            editField = form.save(commit = False)
            # editField.txtabledetailid_id = tableid
            editField.field_slug = finalColumnSlug
            if query.status != "new":
                editField.status = "modified"
            editField.user_id = userid
            editField.save()
            print editField
            print editField.id 

            table = Txtabledetails.objects.filter(Q(transactionid_id = transaction_id) & Q(projectid_id = project_id) & ~Q(status = "deleted"))
            table_ser =TxtabledetailsSerializer(instance=table,many=True)
            table_ser_json= json.dumps(table_ser.data)
            table_ser_json_obj = json.loads(table_ser_json)                

            return render(request,'tableMidPart.html',locals())
        else:
            print form.errors
            return HttpResponse('Failure')
    else:      
        form =TableComponentform(instance = query)
        try:
            enumObj = enumtitle.objects.filter(project_id_id= project_id)
        except enumtitle.DoesNotExist:
            enumObj = None
        form.fields["enum"].queryset = enumObj
        return render(request,'tablecomponentedit.html',locals())      




def tablecomponent_delete(request,tabcompid):
    transactionid = request.session['transactionid']
    transaction_id = request.session['transactionid']
    query = Txtablecomponentdetails.objects.get(pk = tabcompid)

    if query.status == "new":
        query.delete()
    else:
        try:
            geneatedSchemaObj = GenerateSchemaComponent.objects.get(column_id=query.id)
            geneatedSchemaObj.delete()
        except GenerateSchemaComponent.DoesNotExist:
            geneatedSchemaObj = None            

        query.status = "deleted"
        query.save()
      
    return HttpResponseRedirect('/transaction/tabledetail/')


@csrf_exempt
def enumlist(request):
    element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])              
    projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])
    project_title = element.project_id.title
    pid = request.session['projectid']

    if request.method == 'POST':
        print request.POST
        keyValue = []
        exisitingEnum = any
        
        unicodeKV = request.POST.get('KV')
        stringKV =  str(unicodeKV)
        arrayUniKV = json.loads(stringKV)
        
        for i in range(len(arrayUniKV)):
            keyValue.append({"key":str(arrayUniKV[i]['key']),"value":str(arrayUniKV[i]['value'])})
        print "KEYVALUE",keyValue

        title = request.POST.get('title')
        desc = request.POST.get('desc')
        
        try:
            exisitingEnum = enumtitle.objects.get(enum_title=title,project_id_id=pid)
        except Exception as e:
            exisitingEnum = None
        
        if exisitingEnum == None:
            try:
                with transaction_db.atomic():
                    titleTable = enumtitle()
                    titleTable.enum_title = title
                    titleTable.description = desc
                    titleTable.project_id_id = element.project_id.id
                    titleTable.save()
                    print titleTable

                    if titleTable:
                        for item in keyValue:
                            kvTable = enumkeyvalue()
                            kvTable.key = item['key']
                            kvTable.value = item['value']
                            kvTable.enum_title_fk = titleTable
                            kvTable.save()
                            print kvTable.id
                        return HttpResponse("Success")
            except Exception as e:
                print e 
                return HttpResponse("Failure")
        else:
            return HttpResponse("Exist")
    else:
        enumTitleForm = EnumTitleform()
        enumKeyValueForm = EnumKeyValueform()
        enumValue = enumtitle.objects.filter(project_id_id = element.project_id.id).order_by('id')
        return render (request,'enum.html',locals())


@csrf_exempt
def enumedit(request,enumid):
    pid = request.session['projectid']
    print enumid
    editKeyValue = []
    dbKV = []
    
    enumTitleObj = enumtitle.objects.get(id=enumid,project_id_id=pid)
    print enumTitleObj.description
    enumKeyValueObj = enumkeyvalue.objects.filter(enum_title_fk_id = enumTitleObj.id).order_by('id')
    for itemKV in enumKeyValueObj:
        dbKV.append(itemKV.id)
    
    enumKvFormSet = modelformset_factory(enumkeyvalue,fields=('key','value'),extra=0)
    
    if request.method =='POST':

        unicodeKV = request.POST.get('KV')
        stringKV =  str(unicodeKV)
        arrayUniKV = json.loads(stringKV)
        
        existKV = request.POST.get('existingkv')
        strExistKV = str(existKV)
        arrayUniExistKV = json.loads(strExistKV)
        arrayExistKV = []

        #Deleting KV
        for i in range(len(arrayUniExistKV)):
            arrayExistKV.append(str(arrayUniExistKV[i]))

        print arrayExistKV
        print dbKV

        for x in dbKV:
            if str(x) not in arrayExistKV:
                query = enumkeyvalue.objects.get(id = x)
                query.delete()
        
        
        #Updating KV
        
        for i in range(len(arrayUniKV)):
            editKeyValue.append({"id":str(arrayUniKV[i]['id']),"key":str(arrayUniKV[i]['key']),"value":str(arrayUniKV[i]['value'])})

       
        title = request.POST.get('title')
        desc = request.POST.get('desc')

        try:
            exisitingEnum = enumtitle.objects.get(enum_title=title,project_id_id=pid)
        except Exception as e:
            exisitingEnum = None
        
        if exisitingEnum == None or exisitingEnum == enumTitleObj:
       
            try:
                with transaction_db.atomic():
                    enumTitleObj.enum_title = title
                    enumTitleObj.description = desc
                    enumTitleObj.save()
                    print enumTitleObj.id

                    if enumTitleObj:
                        for item in editKeyValue:
                            print item
                            if item['id'] != '':
                                print item['id']
                                kvColumn = enumkeyvalue.objects.get(id = item['id'] )
                                print kvColumn
                                if kvColumn:
                                    kvColumn.key = item['key']
                                    kvColumn.value = item['value']
                                    kvColumn.save()
                                    print kvColumn.id
                            else:
                                print "NEW KV"
                                kvTable = enumkeyvalue()
                                kvTable.key = item['key']
                                kvTable.value = item['value']
                                kvTable.enum_title_fk = enumTitleObj
                                kvTable.save()
                                print kvTable.id

                        return HttpResponse("Success")
            
            except Exception as e:
                print e 
                return HttpResponse("Failure")
        else:
            return HttpResponse("Exist")
        
        
       
    else:
        titleForm = EnumTitleform(instance = enumTitleObj)
        print titleForm
        formset = enumKvFormSet(queryset=enumKeyValueObj)
        return render (request,'enumedit.html',locals())

def enumdelete(request,enumid):
    print  enumid
    pid = request.session['projectid']
    query = enumtitle.objects.get(id=enumid,project_id_id=pid)
    query.delete()
    return HttpResponseRedirect('/transaction/enumlist/')

@csrf_exempt
def generateSchema(request,txnid):
    element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])              
    projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])
    project_title = element.project_id.slug
        
    transaction_id = request.session['transactionid']
    project_id = request.session['projectid']
    userid = request.session['userid']
    db_error = []
    
    table_component_dict={}
    tx_comp_dict={}
    
    pid = Project.objects.get(pk=project_id)
    tid = Transaction.objects.get(pk=transaction_id)
    uid = userprofile.objects.get(pk=userid)
    
    errors = generate_schema(request,transaction_id,project_id,userid)
    
    print "ERRORS",errors
    print "TABLE DICT",table_component_dict
    print "TABLE COMPONENT DICT",tx_comp_dict

    if len(errors) > 0:
        for error in errors:
            db_error.append(str(error))
            print db_error
        return HttpResponse(json.dumps(db_error))

    else:
        # try:
        #     with transaction_db.atomic():
                
        #         table_components = Txtabledetails.objects.filter(projectid = project_id,transactionid = transaction_id)
        #         primarytable = Txtabledetails.objects.get(projectid = project_id,transactionid = transaction_id,isprimary=True)
        
        #         for table_comp in table_components:
        #             if table_comp.tablename and table_comp.table_slug in table_component_dict and table_component_dict[table_comp.table_slug] == 'add':
                        
        #                 generate_schema_tab = GenerateSchemaTableComponent.objects.create(projectid=pid,transactionid= tid,user=uid,table=table_comp,tablename=table_comp.tablename,table_slug=table_comp.table_slug,ddl_type='add',isprimary=table_comp.isprimary,db_type=table_comp.db_type)
        #                 print generate_schema_tab
                        
        #                 if generate_schema_tab:
                            
        #                     components = Txtablecomponentdetails.objects.filter(txtabledetailid=table_comp.id,isdbfield=True)
        #                     for component in components:
        #                         if component.field_slug in tx_comp_dict and tx_comp_dict[component.field_slug] == 'add':
        #                             print generate_schema_tab
        #                             print table_comp.tablename
        #                             print component.columnname
        #                             generate_schema_field=GenerateSchemaComponent.objects.create(gen_schema_table=generate_schema_tab,
        #                                                                 ddl_type='add',
        #                                                                 column = component,
        #                                                                 columnname = component.columnname,
        #                                                                 datatype=component.datatype,
        #                                                                 maxlength=component.maxlength,
        #                                                                 no_of_decimal_digits=component.no_of_decimal_digits,
        #                                                                 field_slug = component.field_slug,
        #                                                                 isdbfield = component.isdbfield,
        #                                                                 isnull=component.isnull,
        #                                                                 db_type=component.db_type)
        #                             print generate_schema_field
                                    
                        
                                                                                                                                                                
                                                                                                                                                                
        # except Exception as e:
        #     print e
        #     logger.exception("Error while saving generate schema")
        

        # table = Txtabledetails.objects.filter(transactionid_id = transaction_id, projectid_id = project_id)
        # table_ser =TxtabledetailsSerializer(instance=table,many=True)
        # table_ser_json= json.dumps(table_ser.data)
        # table_ser_json_obj = json.loads(table_ser_json) 	

        # tableForm = TableDetailsform()
        # return render(request, 'tabledetail.html',locals()) 
        return HttpResponse("SUCCESS")
