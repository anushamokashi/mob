# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse,HttpResponseBadRequest
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from Mobilebuilder.decorators import myuser_login_required 
from reportview.forms import ReportForm,ReportGroupingForm,ReportParamFieldForm,ReportFieldForm,ReportGroupingForm,QueryForm,ReportActionForm,ReportPrintFormatActionForm,ReportPDFForm,ReportCSVForm,ReportHTMLForm,ReportSubmitForm,ReportEpostMapForm,PaymentForm,NewActionForm
from project.models import Project, Projectwiseusersetup
from authentication.models import userprofile
from reportview.models import Report,ReportParamField,Query,ReportField,ReportGrouping,ReportAction,ReportPrintFormatAction,ReportPDF,ReportCSV,ReportHTML,ReportSubmit,ReportEpostMap,Payment,NewAction
from printformat.models import PrintFormat
from django.shortcuts import get_list_or_404, get_object_or_404
import re
from schema.models import Db_connections_info, Db_profile
from django.conf import settings
import MySQLdb
import cx_Oracle as oracle
from django.template.defaultfilters import slugify
from unidecode import unidecode
from django.template import defaultfilters
from reportview.serializers import ReportviewSerializer,ReportActionSerializer
from rolesetup.models import Role,ViewsForRole
from hometemplate.models import Homepage,Menu
from transactionview.models import Transactionview
from django.forms.models import modelformset_factory
from django.db import transaction
import datetime
import string
import json
import os
import zipfile
import StringIO
from hometemplate.models import Homepage
from operator import itemgetter

# Create your views here.
@myuser_login_required
def reportview(request):
    pid = request.session['projectid']
    loginModel = userprofile.objects.get(is_user = True ,id = request.session['userid'])
    element =Projectwiseusersetup.objects.get(userid=loginModel.id,project_id = pid)
    projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])
    
    instance = Report.objects.filter(project_id = pid)
    form = ReportForm()
    return render(request, 'reportview.html', locals())

def reportedit(request,title):
    element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])
    project_title = element.project_id.title
    projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])
    form = ReportForm()
    edit=Report.objects.get(pk=title)
    request.session['reportid']=edit .id
    params = ReportParamField.objects.filter(report_id=title)
    query=Query.objects.filter(report_id=title)
    field=ReportField.objects.filter(report_id=title)
    grouping=ReportGrouping.objects.filter(report_id=title)
    actions =ReportAction.objects.filter(report_id=title)
    return render(request, "reportedit.html",locals())


@csrf_exempt
def saveReports(request):
    reportTitle = ""
    parentReportId = ""
    metaData = ""
    project_id = request.session['projectid']
    pid = Project.objects.get(pk = project_id)
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            newreport = form.save(commit=False)
            newreport.project_id = pid.id
            reporttitle = request.POST.get('title')
            newreport.identifiers=reporttitle.lower().replace(" ","")+"_rpt"
            newreport.save()
        else:
            print form.errors
         
    return HttpResponseRedirect('/reportview/repoviewdetails/')

def editmodal(request,title):
    edit=Report.objects.get(pk=title)
    rowtemplate = edit.rowtemplate
    reportdescription = edit.report_description
    form = ReportForm(instance = edit)
    comp_list = []
    report_br = ReportField.objects.filter(report_id =title)
    for titles in report_br:
        comp_dest = {"id":"",
        "slug":"",
        "title":""}
        comp_dest["id"]=titles.id
        comp_dest["slug"]=titles.slug
        comp_dest["title"]=titles.title
        comp_list.append(comp_dest)

    return render(request, "editdetails.html", locals()) 

@csrf_exempt
def updateReport(request,reportId):
    element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])
    project_title = element.project_id.title
    projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])
    project_id = request.session['projectid']
    pid = Project.objects.get(pk = project_id)
    repo=Report.objects.get(pk=reportId)
    form = ReportForm(request.POST,instance = repo)

    if request.POST:
        if form.is_valid():
            updatereport = form.save(commit=False)
            updatereport.project_id = pid.id
            updatereport.identifiers=updatereport.title.lower().replace(" ","")+"_rpt"
            updatereport.save()
            return HttpResponse("success")
        else:
            print form.errors

            return HttpResponseBadRequest("success")

def delReport(request,reportId):
    query = Report.objects.get(pk = reportId)
    project_id = request.session['projectid']
    try:
        role = Role.objects.filter(projectid_id = project_id)
        for r in role:
            roleid = r.id
            views = ViewsForRole.objects.filter(role_id = roleid)
            for view in views:
                lists = json.loads(view.reportview)
                try:
                    menu  = Menu.objects.filter(reportview_id = reportId)
                    for m in menu:
                        ids =  str(m.id)
                        lists.remove(ids)

                    view.reportview = json.dumps(lists)
                    view.save()
                except Exception as ed:
                    print ed
    except Exception as e:
        print e

    
    element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])
    project_title = element.project_id.title
    projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])

    if element:

        projectid = element.project_id.id
        dbprofile = element.db_profileid_id
        request.session['projectid'] = element.project_id.id


    dbProfileData = Db_profile.objects.get(pk=dbprofile)  
    print 'dbProfileData',dbProfileData 
    appDbId = dbProfileData.appdb_id
    appDbData = Db_connections_info.objects.get(pk=appDbId)
        
    host = appDbData.host
    print host
    username = appDbData.username
    print username
    password = appDbData.password
    print password
    database = appDbData.dbname
    print database 
    
    #Making connection
    db = MySQLdb.connect(host,username,password,database)
    cursor = db.cursor()
    print cursor
    #addComponent=("DELETE * FROM rprtmobilesqlmetadata WHERE  query_id = %s",[query.id])
    try:
        query = Report.objects.get(pk = reportId)
        print query.title,'query.title'
        cursor.execute("DELETE FROM rprtmetadata WHERE  report_id = %s",[query.title])
        db.commit()
        print "commit"
    except Exception as e:
        print e
        db.rollback()
        print "rollback"
     

    query. delete()
    return HttpResponseRedirect('/reportview/repoviewdetails/')


def parammodal(request,title):
    param=Report.objects.get(pk=title)
    paramform = ReportParamFieldForm()    
    report_param_list = ReportParamField.objects.filter(report_id = param.id)
    return render(request, "reportparam.html",locals()) 
  

def saveparams(request, repoid):
    if request.method == "POST":
        form = ReportParamFieldForm(request.POST)

        if form.is_valid() :
            paramreport = form.save(commit=False)
            paramreport.identifiers = slugify(paramreport.title)
            paramreport.caption=paramreport.title
            paramreport.slug=slugify(paramreport.title)
            paramreport.report_id = repoid
            paramreport.save()
            return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))           
            
        else:
            print form.errors

        return HttpResponseRedirect('/reportview/editReport/')


def parameditmodal(request,title,pk):
    paramform = ReportParamFieldForm()
    rpt =Report.objects.get(id=title)
    rpt_param = get_object_or_404(ReportParamField,pk=pk)
    comp_identifiers= []   
    if request.POST:
        try:
            rpt_param_form = ReportParamFieldForm(request.POST,instance=rpt_param)
            rpt_param_form.identifiers=request.POST.get('identifiers')
            rpt_param_form.sql=request.POST.get('sql')
            if rpt_param_form.sql == "" :
                print "nosql"
                rpt_param_form.save()
                return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))
            else:
                if rpt_param_form.is_valid() :
                    print"yessql"
                    rpt_param_form.save()
                    element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])
                    project_title = element.project_id.title
                    project_slug = element.project_id.slug
                    projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])
                    if element:
                        projectid = element.project_id.id
                        dbprofile = element.db_profileid_id
                        request.session['projectid'] = element.project_id.id
                        dbProfileData = Db_profile.objects.get(pk=dbprofile)
                        appDbId = dbProfileData.appdb_id
                        appDbData = Db_connections_info.objects.get(pk=appDbId)
                        host = appDbData.host
                        username = appDbData.username
                        password = appDbData.password
                        database = appDbData.dbname
                        db = MySQLdb.connect(host,username,password,database)
                        cursor = db.cursor()
                        parmsql =get_object_or_404(ReportParamField,pk=pk)
                        print "parmsql",parmsql.sql
                        if (parmsql):
                            comp_identifiers.append(parmsql.id) 
                        else:
                            comp_identifiers = []



                    try:
                        parasql = get_object_or_404(ReportParamField,pk=pk)
                        cursor.execute("SELECT * FROM rprtmobilesqlmetadata WHERE  query_id = %s AND report_id = %s",[parasql.title,rpt.identifiers]) 
                        paramSqlMetaData = cursor.fetchall()
                        #converting tuple to str
                        paramSqlMetaDataStr = []
                        for str in paramSqlMetaData:
                            paramSqlMetaDataStr.append(str[0])
                    except:
                        paramSqlMetaData = ()

                    now = datetime.datetime.now()
                    addComponent =   "INSERT INTO rprtmobilesqlmetadata (sqltext,sqltitle,report_sql_type,project_id,report_id,created,modified,query_id) VALUES (%(sqltext)s,%(sqltitle)s,%(report_sql_type)s,%(project_id)s,%(report_id)s,%(created)s,%(modified)s,%(query_id)s)"
                    updateComponent =  "UPDATE rprtmobilesqlmetadata SET sqltext=%(sqltext)s, modified=%(modified)s WHERE query_id = %(query_id)s AND report_id=%(report_id)s"
                    data_comp_list = []
                    data_comp_dict = {}
                    comp_identifiers= [] 

                    isThere = False 
                    rptid = rpt.identifiers
                    if len(paramSqlMetaData)== 0:
                        
                        paramid =parasql.title
                        data_comp_dict = {
                            'sqltext': parasql.sql,
                            'sqltitle':parasql.title,
                            'report_sql_type': "report_param_query",
                            'project_id':project_slug,
                            'report_id':rptid,
                            'query_id':paramid,                    
                            'created':now.strftime("%Y-%m-%d %H:%M"),
                            'modified':now.strftime("%Y-%m-%d %H:%M"),
                        }
                        data_comp_list.append(data_comp_dict)
                        try:
                            cursor.executemany(addComponent,data_comp_list)
                            db.commit()
                            print "commit"
                        except Exception as e:
                            print e
                            db.rollback()
                            print "rollback" 
                    else:
                        paramid =parasql.title
                        data_comp_dict = {
                            'sqltext': parasql.sql,
                            'modified':now.strftime("%Y-%m-%d %H:%M"),
                            'query_id': paramid,
                            'report_id':rptid,
                        }
                        try:
                            cursor.execute(updateComponent,data_comp_dict)
                            db.commit()
                            print "commited"
                        except Exception as e:
                            print e
                            db.rollback()
                            print "rollback"
               
               
                    return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))
        except Exception as e:
            print e

        



    else:
        rpt_param_form = ReportParamFieldForm(instance=rpt_param)
    return render(request, "editparam.html",locals()) 


def delparam(request,title):
    query = ReportParamField.objects.get(pk = title)
    element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])
    project_title = element.project_id.title
    projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])

    if element:

        projectid = element.project_id.id
        dbprofile = element.db_profileid_id
        request.session['projectid'] = element.project_id.id


    dbProfileData = Db_profile.objects.get(pk=dbprofile)
    print 'dbProfileData',dbProfileData
    appDbId = dbProfileData.appdb_id
    appDbData = Db_connections_info.objects.get(pk=appDbId)

    host = appDbData.host
    print host
    username = appDbData.username
    print username
    password = appDbData.password
    print password
    database = appDbData.dbname
    print database

    #Making connection
    db = MySQLdb.connect(host,username,password,database)
    cursor = db.cursor()
    print cursor
    #addComponent=("DELETE * FROM rprtmobilesqlmetadata WHERE query_id = %s",[query.id])
    try:
        query = Report.objects.get(pk = reportId)
        #print query.title,'query.title'
        cursor.execute("DELETE FROM rprtmobilesqlmetadata WHERE report_id = %s",[query.identifiers])

        db.commit()
        print "commit"
    except Exception as e:
        print e
        db.rollback()
        print "rollback"


    query. delete()
    return HttpResponseRedirect('/reportview/repoviewdetails/')
    query.delete()
    return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))

def fieldmodal(request,title):
    field=Report.objects.get(pk=title)
    fieldform = ReportFieldForm()
    return render(request, "field.html",locals())

def fieldsave(request,repoid):

    if request.method == "POST":
        form = ReportFieldForm(request.POST)

        if form.is_valid() :
            reportfield = form.save(commit=False)
            reportfield .report_id = repoid
            reportfield.slug = slugify(reportfield.title).replace("-","_")
            reportfield.save()
            
            return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))
            
        else:
            print form.errors

    return HttpResponseRedirect('/reportview/editReport/')

def fieldeditmodal(request,pk,title):
    instance = ReportField.objects.filter(id = pk)
    rpt_field = get_object_or_404(ReportField,pk=pk)

    if request.POST:
        rpt_field_form = ReportFieldForm(request.POST,instance=rpt_field)
        if rpt_field_form.is_valid():
            fieldupdate=rpt_field_form.save(commit=False)
            fieldupdate.save()
            return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))
        
        else:
            print  rpt_field_form.errors 

    else:
        rpt_field_form = ReportFieldForm(instance=rpt_field)

    return render(request, "fieldedit.html",locals()) 

def delfield(request,title):

    query = ReportField.objects.get(pk = title)
    
    query.delete()
    return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))


def BRmodal(request,title):
    BR =Report.objects.get(pk=title)
    form = ReportBusinessRuleForm()
    comp_list = []
    report_br = ReportParamField.objects.filter(report_id = BR.id)
    for titles in report_br:
        comp_dest = {"id":"",
        "slug":"",
        "title":""}
        comp_dest["id"]=titles.id
        comp_dest["slug"]=titles.slug
        comp_dest["title"]=titles.title
        comp_list.append(comp_dest)


    return render(request, "businessrule.html",locals())

def brsave(request,repoid):
    
    if request.method == "POST":
        form = ReportBusinessRuleForm(request.POST)        
        
        if form.is_valid() :
            br = form.save(commit=False)
            br.title=request.POST.get('businesstitle')
            br .report_id = repoid
            br.save()
            return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))
            
        else:
            print form.errors
            
    return HttpResponseRedirect('/reportview/editReport/')

def BRedit(request,title,pk):
    form = ReportBusinessRuleForm()
    comp_list = []
    reports = ReportParamField.objects.filter(report_id =title)
    for titles in reports:
        comp_dest = {"id":"",
        "slug":"",
        "title":""}
        comp_dest["id"]=titles.id
        comp_dest["slug"]=titles.slug
        comp_dest["title"]=titles.title
        comp_list.append(comp_dest)

    report_br = get_object_or_404(ReportBusinessRule,pk = pk)
    if request.POST:
        updateform = ReportBusinessRuleForm(request.POST,instance=report_br)

        if updateform.is_valid():
            rpt_br_form = updateform.save(commit=False)
            rpt_br_form.title=request.POST.get('businesstitle')
            rpt_br_form .report_id = report_br.report_id
            rpt_br_form.save()

            return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))
        else:
            print form.errors

    else:
        updateform = ReportBusinessRuleForm(instance=report_br)

        return render(request, "bredit.html",locals())


def delBR(request,title):

    query = ReportBusinessRule.objects.get(pk = title)
    query. delete()
    return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))

def groupmodal(request,title):
    report =Report.objects.get(pk=title)
    rpt_group_form = ReportGroupingForm()
    comp_list = []
    report_br = ReportField.objects.filter(report_id =title)
    for titles in report_br:
        comp_dest = {"id":"",
        "slug":"",
        "title":""}
        comp_dest["id"]=titles.id
        comp_dest["slug"]=titles.slug
        comp_dest["title"]=titles.title
        comp_list.append(comp_dest)
    
    return render(request, "grouping.html",locals()) 

def groupingsave(request,repoid):

    if request.method == "POST":
        form = ReportGroupingForm(request.POST)
        
        if form.is_valid() :
            group = form.save(commit=False)
            group.report_id = repoid
            group.save()

            return HttpResponseRedirect('/reportview/editReport/%s'% (repoid))
            
        else:
            print form.errors
            
    return render(request, "reportedit.html",locals())

def groupeditmodal(request,title,pk):
    comp_list=[]
    report_br = ReportField.objects.filter(report_id =title)
    for titles in report_br:
        comp_dest = {"id":"",
        "slug":"",
        "title":""}
        comp_dest["id"]=titles.id
        comp_dest["slug"]=titles.slug
        comp_dest["title"]=titles.title
        comp_list.append(comp_dest)
    rpt_group=ReportGrouping.objects.get(pk=pk)

    if request.POST:
        rpt_group_form = ReportGroupingForm(request.POST,instance=rpt_group)

        if rpt_group_form.is_valid():
            rpt_group_form.save()

            return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))

        else:
             return HttpResponseRedirect('/reportview/editReport/',locals())

    else:
        rpt_group_form =ReportGroupingForm(instance=rpt_group)


    return render(request, "groupedit.html",locals())


def delgroup(request,title):  
    query = ReportGrouping.objects.get(pk = title)
    query. delete()
    return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))


def Querymodal(request,title):
    query=Report.objects.get(pk=title)
    form = QueryForm()
    return render(request, "query.html",locals())
    
def reportQuerySave(request,repoid):
    report = Report.objects.get(id = repoid)   
    element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])
    project_title = element.project_id.title
    projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])

    if element:

        projectid = element.project_id.id
        dbprofile = element.db_profileid_id
        request.session['projectid'] = element.project_id.id

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
  
    
    if request.method=="POST":
        form=QueryForm(request.POST)
        report_query_title = request.POST.get('title')
    
        if form.is_valid():
            fieldquery=form.save(commit=False)
            fieldquery.report_id = repoid            
            fieldquery.slug =defaultfilters.slugify(report_query_title) 
            fieldquery.save()
            resp={}
            resp['data']="save"
            resp['data_msg']="successfully saved"
            report_query_sql = request.POST.get('sql')
            paramsame=parse_params(report_query_sql)
            print 'params',paramsame
            param_list =[]
            for num in paramsame:
                if num not in param_list:
                    param_list.append(num)
                    #print 'params',param_list
            #return param_list

            
            print 'params',param_list

            if fieldquery.is_main_query==True and fieldquery.sql is not None:

                for param in param_list:
                        report_parameter_slug=param.lower()
                        report_fields_order = ReportParamField.objects.filter(report=report).order_by("-display_order")
                        if report_fields_order.count() != 0:
                            report_field_order = report_fields_order.first().display_order 
                            display_order = report_field_order+1
                        else:
                            display_order = 1


                        report_param_field_form = ReportParamFieldForm({'title':param,
                                                                     'description':'',
                                                                     'slug':report_parameter_slug,
                                                                     'caption':param,
                                                                     'query':fieldquery.id,
                                                                     'display_order':display_order,
                                                                     'is_hidden':False,
                                                                     'no_of_decimal_digits':0,
                                                                     'allow_multiselect':False,
                                                                     'data_type':None,
                                                                     #'component_type':None,
                                                                     #'widget_type':None,
                                                                     #'related_table_component':None,
                                                                     'value_field':None,
                                                                     'display_field':None,
                                                                     'identifiers':param})
                        if report_param_field_form.is_valid():
                            report_param_field = report_param_field_form.save(commit=False)
                            report_param_field.report = report
                            report_param_field.save()

                        else:
                            pass


                reportquery = request.POST.get('is_main_query')
                sql_string = str(report_query_sql)
                match = re.compile(r":\w+")
                items = re.findall(match,sql_string)
                for item in items:
                    sql_string = str(sql_string).replace(item, sql_value_replace(str(item)),1)

                cursor.execute(sql_string)
                field_list = cursor.description

                for result_field in field_list:
                    report = Report.objects.get(id = repoid)
                    report_field_slug=result_field[0].lower()
                    report_fields_order = ReportField.objects.filter(report=report).order_by("-display_order")

                    if report_fields_order.count() != 0:
                                report_field_order = report_fields_order.first().display_order                                
                                display_order = report_field_order+1
                    else:
                        display_order = 1



                    report_field_form = ReportFieldForm({'title':result_field[0],
                                                                 'description':'',
                                                                 'slug':report_field_slug,
                                                                 'query':fieldquery.id,
                                                                 'caption':result_field[0],
                                                                 'report_field_type':"query-field",
                                                                 'no_of_decimal_digits':0,
                                                                 'show_running_total':False,
                                                                 'show_total':False,
                                                                 'is_hidden':False,
                                                                 'apply_comma':False,
                                                                 'dont_repeat':False,
                                                                 'dont_show_zero':False,
                                                                 'display_order':display_order,
                                                                 'template':'',
                                                                 'width':0,
                                                                 'height':0,
                                                                 'is_bold_font':False,
                                                                 'color':''} )

                    if report_field_form.is_valid():
                                report_field = report_field_form.save(commit=False)
                                report_field.report = report
                                report_field.save()

                    else:
                        pass


            return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))
            
        else:
            
            print form.errors

    else:
        return render(request, "reportedit.html",locals())
       

def sql_value_replace(match):
    return 'null'

def db_resultset(project,sql,userId):
    try:
        connection = get_app_db_config(userId,project)            
        cursor = connection.cursor()    
        sql_string = str(sql)
        match = re.compile(r":\w+")
        items = re.findall(match,sql_string)
        for item in items:
            sql_string = str(sql_string).replace(item, sql_value_replace(str(item)),1)                    
        
        if "Oracle" in str(connection):    
            result = cursor.execute(sql_string)
        elif "_mysql" in str(connection):
            sql_res = cursor.execute(sql_string)
            result = cursor  
            
    except oracle.DatabaseError as e:
        raise e    
    
    return result

def parse_params(sql):
    param_list=[]
    match = re.compile(r":\w+")
    items = re.findall(match,str(sql))
    for item in items:
        item = item.replace(':','')
        param_list.append(item)
        
        
    return param_list  


def Queryeditmodal(request,pk,title):
    report = Report.objects.get(id = title) 
    query=Query.objects.get(pk=pk)
    element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])
    project_title = element.project_id.title
    projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])

    if element:

        projectid = element.project_id.id
        dbprofile = element.db_profileid_id
        request.session['projectid'] = element.project_id.id


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
    if request.POST:
        form=QueryForm(request.POST, instance = query)
        query_title = request.POST.get('title')

        if form.is_valid():
            queryupdate=form.save(commit=False)
            queryupdate.report_id = report.id
            queryupdate.save()

            if queryupdate.is_main_query==True and queryupdate.sql is not None:
                paramdel = ReportParamField.objects.filter(query_id = pk) 
                paramdel.delete()
                report_query_sql = request.POST.get('sql')
                paramsame=parse_params(report_query_sql)
                print 'params',paramsame
                param_list =[]
                for num in paramsame:
                    if num not in param_list:
                        param_list.append(num)

                for param in param_list:
                    report_parameter_slug=param.lower()
                    #report = Report.objects.get(id = title) 
                    rpt_param_fields = ReportParamField.objects.filter(report_id = report).order_by('display_order')
                    if rpt_param_fields:
                        disp_order = rpt_param_fields.last().display_order+1
                    else:
                        disp_order = 1



                    report_param_field_form = ReportParamFieldForm({'title':param,
                                                                     'description':'',
                                                                     'slug':report_parameter_slug,
                                                                     'caption':param,
                                                                     'query':queryupdate.id,
                                                                     'display_order':disp_order,
                                                                     'is_hidden':False,
                                                                     'no_of_decimal_digits':0,
                                                                     'allow_multiselect':False,
                                                                     'data_type':None,
                                                                     'component_type':None,
                                                                     'widget_type':None,
                                                                     'related_table_component':None,
                                                                     'value_field':None,
                                                                     'display_field':None,
                                                                     'identifiers':param})
                             
                             
                    if report_param_field_form.is_valid():
                                           report_param_field = report_param_field_form.save(commit=False)
                                           report_param_field.report_id = report.id
                                           report_param_field.save()

                    else:
                        print report_param_field_form.errors


                    
                   
                reportquery = request.POST.get('is_main_query')
                fielddel = ReportField.objects.filter(query_id = pk)
                print 'fielddel',fielddel
                fielddel.delete()
                print 'report_query_sql',report_query_sql
                sql_string = str(report_query_sql)
                match = re.compile(r":\w+")
                items = re.findall(match,sql_string)
                for item in items:
                    print item
                    sql_string = str(sql_string).replace(item, sql_value_replace(str(item)),1)
                    
                     
                cursor.execute(sql_string)
                field_list = cursor.description
                print field_list

                for result_field in field_list:
                    print result_field
                    report = Report.objects.get(id = title)
                    report_field_slug=result_field[0].lower()
                    report_fields_order = ReportField.objects.filter(report_id=report).order_by("display_order")
                    if report_fields_order:
                            field_disp_order = report_fields_order.last().display_order+1

                    else:
                        
                        field_disp_order = 1
                    report_field_form = ReportFieldForm({'title':result_field[0],
                                                             'description':'',
                                                             'slug':report_field_slug,
                                                             'query':queryupdate.id,
                                                             'caption':result_field[0],
                                                             'report_field_type':"query-field",
                                                             #'data_type':data_type,
                                                             'no_of_decimal_digits':0,
                                                             'show_running_total':False,
                                                             'show_total':False,
                                                             'is_hidden':False,
                                                             'apply_comma':False,
                                                             'dont_repeat':False,
                                                             #'column_alignment':column_align,
                                                             'dont_show_zero':False,
                                                             'display_order':field_disp_order,
                                                             'template':'',
                                                             #'pivot_column_type':None,
                                                             'width':0,
                                                             'height':0,
                                                             'is_bold_font':False,
                                                             'color':''})

                    if report_field_form.is_valid():
                            #print report_field_form
                            report_field = report_field_form.save(commit=False)
                            report_field.report = report
                            report_field.save()

                    else:
                        print report_field_form.errors


                return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))


            else:
                print form.errors

            
        return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))



    else:
        return render(request, "queryedit.html",locals())


def delQuery(request,title):
    query = Query.objects.get(pk = title)
    paramdelete = ReportParamField.objects.filter(query_id=title)
    fielddelete = ReportField.objects.filter(query_id=title)
    paramdelete. delete()
    fielddelete. delete()    
    element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])
    project_title = element.project_id.title
    projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])

    if element:

        projectid = element.project_id.id
        dbprofile = element.db_profileid_id
        request.session['projectid'] = element.project_id.id


    dbProfileData = Db_profile.objects.get(pk=dbprofile)  
    print 'dbProfileData',dbProfileData 
    appDbId = dbProfileData.appdb_id
    appDbData = Db_connections_info.objects.get(pk=appDbId)
        
    host = appDbData.host
    print host
    username = appDbData.username
    print username
    password = appDbData.password
    print password
    database = appDbData.dbname
    print database 
    
    #Making connection
    db = MySQLdb.connect(host,username,password,database)
    cursor = db.cursor()
    print cursor
    #addComponent=("DELETE * FROM rprtmobilesqlmetadata WHERE  query_id = %s",[query.id])
    try:
        query = get_object_or_404(Query,pk = title)
        print query.id,'query.id'
        cursor.execute("DELETE FROM rprtmobilesqlmetadata WHERE  query_id = %s",[query.id])
        db.commit()
        print "commit"
    except Exception as e:
        print e
        db.rollback()
        print "rollback"

    query. delete()
    return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))


def reportprocess(request,title,pk):    
    query = get_object_or_404(Query,pk = pk)
    rpt =Report.objects.get(id=title)
    fieldWSQL=[]
    comp_identifiers= []
    element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])
    project_title = element.project_id.title
    projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])
    if element:
        projectid = element.project_id.title
        dbprofile = element.db_profileid_id
        request.session['projectid'] = element.project_id.id     
    
    dbProfileData = Db_profile.objects.get(pk=dbprofile)  
    appDbId = dbProfileData.appdb_id
    appDbData = Db_connections_info.objects.get(pk=appDbId)
        
    host = appDbData.host
    username = appDbData.username
    password = appDbData.password
    database = appDbData.dbname
    db = MySQLdb.connect(host,username,password,database)
    cursor = db.cursor()
    try:
        #queryData = get_object_or_404(Query,pk = pk)
        queryData =Query.objects.filter(id=query.id)       
    except Query.DoesNotExist:
        queryData = None

    if (queryData):
        #Retriving identifiers
        for component in queryData:           
            if component.sql:
                comp_identifiers.append(component.id)    
        
            else:
                comp_identifiers = []


    #Meta data
    try:
        query = get_object_or_404(Query,pk = pk)
        cursor.execute("SELECT * FROM rprtmobilesqlmetadata WHERE  query_id = %s",[query.id]) 
        mobileSqlMetaData = cursor.fetchall()

    #converting tuple to str
        mobileSqlMetaDataStr = []
        for str in mobileSqlMetaData:
            mobileSqlMetaDataStr.append(str[0])

    except:
        mobileSqlMetaData = ()

    now = datetime.datetime.now()
    addComponent =   "INSERT INTO rprtmobilesqlmetadata (sqltext,sqltitle,report_sql_type,project_id,report_id,created,modified,query_id) VALUES (%(sqltext)s,%(sqltitle)s,%(report_sql_type)s,%(project_id)s,%(report_id)s,%(created)s,%(modified)s,%(query_id)s)"
    updateComponent =  "UPDATE rprtmobilesqlmetadata SET sqltext=%(sqltext)s, modified=%(modified)s WHERE query_id = %(query_id)s"
    data_comp_list = []
    data_comp_dict = {}
    comp_identifiers= []

    isThere = False
 

    if len(mobileSqlMetaData)== 0:
            for component in queryData:
                rptid = rpt
                queryid =component.id
                data_comp_dict = {
                'sqltext': component.sql,
                'sqltitle':component.title,
                'report_sql_type': "report_query",                    
                'project_id':projectid,
                'report_id':rptid,
                'query_id':queryid,                    
                'created':now.strftime("%Y-%m-%d %H:%M"),
                'modified':now.strftime("%Y-%m-%d %H:%M"),
            }
            data_comp_list.append(data_comp_dict)

            try:                
                cursor.executemany(addComponent,data_comp_list)
                db.commit()
                print "commit"
            except Exception as e:
                print e
                db.rollback()
                print "rollback"

    else:
        for component in queryData:
            data_comp_dict = {
                'sqltext': component.sql,
                'modified':now.strftime("%Y-%m-%d %H:%M"),
                'query_id': component.id,
            }
            try:
                cursor.execute(updateComponent,data_comp_dict)
                db.commit()
                print "commit"
            except Exception as e:
                print e
                db.rollback()
                print "rollback"
        

    return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))

def card(details,list_hide,fileName):
    if list_hide == 'hide':
        hide = "hidden"
    else:
        hide = ""
    cardbody=""
    cardinner=""
    parambutton =""
    bodystart="""<ion-list>"""
    bodyend ="""</ion-list>"""
    parambutton ="""<button style="width: 18%;margin-left: 81%;" ion-button full (click)="onButtonClick()" """+hide+""">Params</button>"""
    cardstart ="""<ion-card [hidden]="buttonClicked"><ion-card-header><ion-row><ion-col col-7>Param Fields</ion-col><ion-col><ion-thumbnail item-end><button ion-button type="submit" color="secondary" ion-button small (click)="getreport()">View Report</button></ion-thumbnail></ion-col></ion-row></ion-card-header><ion-card-content><form id=\""""+fileName+"""paramForm\" name=\""""+fileName+"""paramForm\">"""
    cardend="""</form></ion-card-content></ion-card>"""
    lists_sorted = sorted(details,key = itemgetter('do'))
    if lists_sorted:
        for item in lists_sorted:
            #cardbody +="""<ion-label>"""+item['sl']+"""</ion-label>"""
            card_type = item['wt'].lower()

            if card_type =='select':
                cardinner+=cardbody+typeselect(item)

            if card_type =='button':
                cardinner+=cardbody+typebutton(item) 

            if card_type =='checkbox':
                cardinner+=cardbody+typecheckbox(item)

            if card_type =='date':
                cardinner+=cardbody+typedate(item)

            if card_type =='email':
                cardinner+=cardbody+typeemail(item)

            if card_type =='password':
                cardinner+=cardbody+typepassword(item)

            if card_type =='number':
                cardinner+=cardbody+typenumber(item)

            if card_type =='text':
                cardinner+=cardbody+typetext(item)

            if card_type =='time':
                cardinner+=cardbody+typetime(item)

            if card_type =='textarea':
                cardinner+=cardbody+typetextarea(item)

            if card_type =='radiobox':
                cardinner+=cardbody+typeradiobox(item)        

            if card_type =='list':
                cardinner+=cardbody+typelist(item) 
            
            if card_type =='barcode':
                cardinner+=cardbody+typebarcode(item) 
    else:
        cardinner=""""""   
          
    cardhtml = parambutton+cardstart+bodystart+cardinner+bodyend+cardend
    return cardhtml

def typetext(text):
    try:
        if text['ih'] =='True':
            hide ="hidden"
        else:
            hide=""

        if text['sql'] == None or text['sql'] == "":
            Sql= ""
            
        else:
            Sql = text['sql']
            print Sql

        if text['exn'] == None:
            exp = ""
        else:
            exp = text['exn']   

        cardbody=""
        typetext=""
        if text:
            typetext+=""" <ion-item """+hide+"""><ion-label color="primary" stacked>"""+text['cap']+"""</ion-label><ion-input [(ngModel)]=\"preset_value."""+text['idt']+"""\" placeholder=\""""+text['idt']+"""\" id=\""""+text['idt']+"""\" name=\""""+text['idt']+"""\" data-id=\""""+text['idt']+"""\" data-sql=\""""+Sql+"""\" data-fieldname=\""""+text['idt']+"""\" data-eformid=\""""+text['rep']+"""\" data-hidden=\""""+text['ih']+"""\"  data-expression=\""""+exp+"""\" """+hide+""" (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)"></ion-input></ion-item>"""
            return typetext
    except Exception as e:
        print e
        print "111111"

def typeselect(select):
    if select['ih'] =='True':
        hide ="hidden"
    else:
        hide=""
    if select['sql'] == None or select['sql'] == "":
        Sql= ""

    else:
        Sql = select['sql']
        print Sql

    if select['exn'] == None:
        exp = ""
    else:
        exp = select['exn']

    cardbody=""
    typeselect=""
    if select:
        typeselect+=""" <ion-item """+hide+"""><ion-label style = "width: 200px">"""+select['cap']+"""</ion-label><ion-select (ionChange)="checkChange($event,\'"""+select['idt']+"""\')" """+hide+"""><ion-option>"""+select['cap']+"""</ion-option></ion-select></ion-item>"""
        return typeselect

def typedate(date):
    try:
        if date['ih'] =='True':
            hide ="hidden"
        else:
            hide=""

        if date['exn'] == None:
            exp = ""
        else:
            exp = date['exn']
            
        cardbody=""
        typedate=""
        if date:
            typedate+=""" <ion-item """+hide+"""><ion-label style = "width: 200px">"""+date['cap']+"""</ion-label> <ion-datetime [(ngModel)]=\"preset_value."""+date['idt']+"""\" placeholder=\""""+date['idt']+"""\" id=\""""+date['idt']+"""\" name=\""""+date['idt']+"""\" data-id=\""""+date['idt']+"""\"  data-fieldname=\""""+date['idt']+"""\" data-eformid=\""""+date['rep']+"""\" data-hidden=\""""+date['ih']+"""\"  data-expression=\""""+exp+"""\" """+hide+""" (ionFocus)="onFocus($event)" (ionBlur)="checkBlur($event)"></ion-datetime></ion-item>"""
            return typedate
    except Exception as e:
        print e
        print "2222222"

def typebarcode(barcode):
    if barcode['ih'] =='True':
        hide ="hidden"
    else:
        hide=""

    if barcode['exn'] == None:
        exp = ""
    else:
        exp = barcode['exn']   

    cardbody=""
    typebarcodehtml=""
    if barcode:
        typebarcodehtml+="""<ion-item """+hide+""">
                                <ion-label color="primary" stacked>"""+barcode['cap']+"""</ion-label>
                            </ion-item>
                            <ion-row>
                                <ion-col col-10>
                                    <ion-input placeholder=\""""+barcode['idt']+"""\" id=\""""+barcode['idt']+"""\" name=\""""+barcode['idt']+"""\" data-expression=\""""+exp+"""\" """+hide+"""></ion-input>
                                </ion-col>
                                <ion-thumbnail item-end>
                                    <button ion-button outline icon-only color=\"secondary\"  (click)="scan($event,\'"""+barcode['idt']+ """\')">
                                        <ion-icon name="barcode"></ion-icon>
                                    </button>
                                </ion-thumbnail>
                            </ion-row>"""
        return typebarcodehtml

def grid(fgrid):
    fgridbody =""
    contentbody=""
    fgridstart = """<ion-list class="scroll"><table class="table table-striped" id="reporttb" name="reporttb" ><thead>"""
    
    if fgrid:
        for grids in fgrid:
            if grids['ih'] == 'T':
                hide = "hidden"
                dhide = "true"
            else:
                hide= ""
                dhide = "false"


            if grids['dor'] == 'T':
                dor ="dontrepeat"
                norepeat="true"
            else:
                dor=""
                norepeat="false"

            if grids['data_typ']=='button':
                data_typ="datatype"
                datatype="button"
            else:
                data_typ=""
                datatype=""                
                
         
            if grids['icls']!= None:
                icls="icons"
                icons=grids['icls']
            else:                    
                icons="" 

            if grids['exp'] != None:
                exp = grids['exp']
            else:
                exp = ""


            fgridvalue="""</thead><tbody></tbody></table></ion-list>"""        
            fgridbody +="""<th   """+hide+""" data-hidden=\""""+dhide+"""\" data-type=\""""+datatype+"""\" data-dontrepeat=\""""+norepeat+"""\" data-icons=\""""+icons+"""\" data-exp=\""""+exp+"""\">"""+grids['cap']+"""</th>""" 
        gridhtml = fgridstart+fgridbody+fgridvalue
        return gridhtml



@myuser_login_required
def generate_reportpage(request,reportid):
    reporthtml=""
    completehtml=""    
    paramshtml=""
    gridhtml=""
    cardhtml=""
    ionhtml=""
    headerhtml=""
    reportheader=""
    paramhtml =""
    footer_buttonhtml=""
    graphvalue=""
    filePath = settings.MEDIA_ROOT
    projectid = request.session['projectid']
    project = Project.objects.get(pk = projectid)
    ptitle = project.slug
    view = Report.objects.get(id = reportid)
    viewid = view.id
    reporttype= view.report_type
    reportgroup = Report.objects.filter(id = reportid)
    reportgroup_serializer = ReportviewSerializer(instance=reportgroup,many=True)
    reportserialzier =reportgroup_serializer.data
   
    fileName = reportgroup_serializer.data[0]['idt']
    if reportserialzier.__len__() > 0:
        report_serializer_json = json.dumps(reportgroup_serializer.data[0])
        reportactiongroup = ReportAction.objects.filter(report_id = reportid)
        reportactiongroup_serializer = ReportActionSerializer(instance=reportactiongroup,many=True)
        reportserialzier =reportactiongroup_serializer.data  
        actiongroup = ReportAction.objects.filter(report_id = reportid)
        action_serializer = ReportActionSerializer(actiongroup,many = True)
        action_button  = action_serializer.data

        try:
            printFomatAction = ReportAction.objects.get(report_id=view.id,report_action="print_format")
        except ReportAction.DoesNotExist:
            print "No Print Format Action For This Report"
        
       
        
        if reporttype != "displayreport":
            try:
                if action_button:
                    action_json = action_button_html(action_button,reporttype)
                    action_list = json.loads(action_json)
                    actionhtml =  action_list['fab']
                    try:
                        footer_buttonhtml = action_list['button']
                    except:
                        footer_buttonhtml=""""""
                else:
                    actionhtml=""""""

                projectid = reportgroup_serializer.data[0]['pid']
                formhtml = reportgroup_serializer.data[0]   
                jsonMeta = ionicmetaJson(report_serializer_json,fileName,ptitle,request,reportid)
                data =open(filePath+"static/ionicmeta/"+ptitle+"/"+fileName+"/"+fileName+".json").read()
                jsonData = json.loads(data)    
                reportparam= jsonData.get('reportparamfield_meta')
                if reportparam:
                    paramhtml=  card(reportparam,"",fileName) 
                reportfld =jsonData.get('reportfield_meta')
                repdatahtml =  grid(reportfld)
                #return HttpResponse(reportparam)
                completehtml = repdatahtml
                home = Homepage.objects.filter(project_id_id = projectid)
                
                if home[0].menutype == "sidemenu":
                    headerhtml="""<ion-header><ion-toolbar color="primary"><ion-buttons """+home[0].sidemenu+"""><button ion-button menuToggle><ion-icon name="menu"></ion-icon></button></ion-buttons><ion-title style="margin-left: 19%;" >"""+reportgroup_serializer.data[0]['tit']+"""</ion-title ></ion-toolbar>"""+actionhtml+"""</ion-header><ion-content><form id=\""""+fileName+"""Form\" name=\""""+fileName+"""Form\">"""
                else:
                    headerhtml="""<ion-header><ion-navbar><ion-title>"""+reportgroup_serializer.data[0]['tit']+"""</ion-title></ion-navbar>"""+actionhtml+"""</ion-header><ion-content><form id=\""""+fileName+"""Form\" name=\""""+fileName+"""Form\">"""    
                if jsonData['rh1']:
                    header1 =""
                    header2 =""
                    header1 ="""<ion-row class="header_align"><h6>"""+jsonData['rh1']+"""</h6></ion-row>"""
                    if jsonData['rh2']:
                        header2="""<ion-row class="header_align"><h5>"""+jsonData['rh2']+"""</h5></ion-row>"""
                    
                    reportheader ="""<ion-list class="report_header"><div>"""+header1+paramhtml+"""</div></ion-list>"""

                footerhtml2="""<ion-footer style="background-color: #8c969254"><ion-navbar><ion-title style="margin-left: 33%;" >"""+jsonData['rf1']+""" <p class="subtitle">"""+jsonData['rf2']+""" </p> </ion-title></ion-navbar></ion-footer>"""
                reporthtml = headerhtml+reportheader+completehtml+"""</form></ion-content>"""+footer_buttonhtml
               
                if not os.path.exists(filePath+"static/ionicmeta/"+ptitle+"/"+fileName):
                    os.makedirs(filePath+"static/ionicmeta/"+ptitle+"/"+fileName)

                Html_file= open(filePath+"static/ionicmeta/"+ptitle+"/"+fileName+"/"+fileName+".html","w")
                Html_file.truncate()
                Html_file.write(reporthtml)
                Html_file.close()
                view.createpage = True
                view.save()
                return HttpResponse("success")
            except Exception as E:
            	print E
                return HttpResponseBadRequest("error")



        elif reporttype == "graphicalreport":
            
            try:
                if fabbutton:
                    fabconthtml = fab(fabbutton)
                else:
                    fabconthtml=""""""
                print 'Graphicalreport//////////////////////'
                fileName = reportgroup_serializer.data[0]['tit'].lower().replace(" ","")
                #print "fileName",fileName
                #print "ptitle",ptitle
                projectid = reportgroup_serializer.data[0]['pid']
                formhtml = reportgroup_serializer.data[0]   
                jsonMeta = ionicmetaJson(report_serializer_json,fileName,ptitle,request,reportid)
                data =open(filePath+"static/ionicmeta/"+ptitle+"/"+fileName+"/"+fileName+".json").read()
                jsonData = json.loads(data)    
                #print jsonData
                reportparam= jsonData.get('reportparamfield_meta')
                print "paramhtml$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",reportparam
                if reportparam:
                    paramhtml=  card(reportparam,"") 
                reportfld =jsonData.get('reportfield_meta')
                print "reportfld",reportfld
                repdatahtml =  graph(reportfld)
                graphtype=reportgroup_serializer.data[0]['gtype']
                xcoord=reportgroup_serializer.data[0]['xcoord']
                ycoord=reportgroup_serializer.data[0]['ycoord']
                print xcoord,ycoord,"graphtype"
                graphvalue="""<div style="display: block"> <canvas baseChart [datasets]=Data [labels]=Labels [options]=Options [legend]=Legend [chartType]=Type></canvas></div>"""
                #return HttpResponse(reportparam)
                print graphvalue
                completehtml = repdatahtml
                home = Homepage.objects.filter(project_id_id = projectid)
                if home[0].menutype == "sidemenu":                    
                    headerhtml="""<ion-header><ion-toolbar color="primary"><ion-buttons """+home[0].sidemenu+"""><button ion-button menuToggle><ion-icon name="menu"></ion-icon></button></ion-buttons><ion-title>"""+reportgroup_serializer.data[0]['tit']+"""</ion-title></ion-toolbar>"""+fabconthtml+"""</ion-header><ion-content><form id="myreportForm" name="myreportForm">"""
                    
                else:
                    headerhtml="""<ion-header><ion-navbar color="primary"><ion-title>"""+reportgroup_serializer.data[0]['tit']+"""</ion-title></ion-navbar>"""+fabconthtml+"""</ion-header><ion-content><form id="myreportForm" name="myreportForm">"""
                    
                        
                if jsonData['rh1']:
                    header1 =""
                    header2 =""
                    header1 ="""<ion-row class="header_align"><h3>"""+jsonData['rh1']+"""</h3></ion-row>"""
                    if jsonData['rh2']:
                        header2="""<ion-row class="header_align">"""+jsonData['rh2']+"""</ion-row>"""                        
                    reportheader ="""<ion-list class="report_header"><div>"""+header1+header2+"""</div></ion-list>"""
                
                
                footerhtml2="""<ion-footer style="background-color: #8c969254"><ion-navbar><ion-title style="margin-left: 33%;" >"""+jsonData['rf1']+""" <p class="subtitle">"""+jsonData['rf2']+""" </p> </ion-title></ion-navbar></ion-footer>"""
                reporthtml = headerhtml+reportheader+paramhtml+graphvalue+"""</form></ion-content>"""
                if not os.path.exists(filePath+"static/ionicmeta/"+ptitle+"/"+fileName):
                    os.makedirs(filePath+"static/ionicmeta/"+ptitle+"/"+fileName) 
                Html_file= open(filePath+"static/ionicmeta/"+ptitle+"/"+fileName+"/"+fileName+".html","w")
                Html_file.truncate()
                Html_file.write(reporthtml)
                Html_file.close()
                view.createpage = True
                view.save()
                return HttpResponse("success")


            except Exception as e:
                print e
                return HttpResponseBadRequest("error")

        
        else:
            templatehtml =""
            templatestart =""
            templateend =""
            template=""
            paramhtml =""
            try:
                if action_button:
                    action_json = action_button_html(action_button,reporttype)
                    action_list = json.loads(action_json)
                    actionhtml =  action_list['fab']
                    try:
                        footer_buttonhtml = action_list['button']
                    except:
                        footer_buttonhtml=""""""
                else:
                    actionhtml=""""""
                projectid = reportgroup_serializer.data[0]['pid']
                formhtml = reportgroup_serializer.data[0]
                jsonMeta = ionicmetaJson(report_serializer_json,fileName,ptitle,request,reportid)
                data =open(filePath+"static/ionicmeta/"+ptitle+"/"+fileName+"/"+fileName+".json").read()
                jsonData = json.loads(data)    
                reportparam= jsonData.get('reportparamfield_meta')
                
                templatetype = reportgroup_serializer.data[0]['tem_type']
                if templatetype == 'card':
                    templatestart = """<div id="displayreport"><ion-card *ngFor="let active of this.names let i =index" id="activerow-{{i}}">"""
                    templateend ="""</ion-card></div>"""
                elif templatetype == 'list':
                    templatestart = """<div id="displayreport"><ion-list *ngFor="let active of this.names let i =index" id="activerow-{{i}}">"""
                    templateend ="""</ion-list></div>"""

                template  = reportgroup_serializer.data[0]['template']
               
                paramfield = reportgroup_serializer.data[0]['reportparamfield_meta']
                if len(paramfield) >0:
                    paramhtml=  card(paramfield,"hide",fileName)

                templatehtml = templatestart+template+templateend
                reportfld =jsonData.get('reportfield_meta')
                home = Homepage.objects.filter(project_id_id = projectid)
                if home[0].menutype == "sidemenu":
                    headerhtml="""<ion-header><ion-toolbar color="primary"><ion-buttons """+home[0].sidemenu+"""><button ion-button menuToggle><ion-icon name="menu"></ion-icon></button></ion-buttons><ion-title>"""+reportgroup_serializer.data[0]['tit']+"""</ion-title></ion-toolbar>"""+actionhtml+"""</ion-header><ion-content><form id=\""""+fileName+"""Form\" name=\""""+fileName+"""Form\">"""
                else:
                    headerhtml="""<ion-header><ion-navbar color="primary"><ion-title>"""+reportgroup_serializer.data[0]['tit']+"""</ion-title></ion-navbar>"""+actionhtml+"""</ion-header><ion-content><form id=\""""+fileName+"""Form\" name=\""""+fileName+"""Form\">"""    
                
                if jsonData['rh1']:
                    header1 =""
                    header2 =""
                    header1 ="""<ion-row class="header_align"><h3>"""+jsonData['rh1']+"""</h3></ion-row>"""
                    if jsonData['rh2']:
                        header2="""<ion-row class="header_align">"""+jsonData['rh2']+"""</ion-row>"""
                    
                    reportheader ="""<ion-list class="report_header"><div>"""+header1+header2+"""</div></ion-list>"""

                footerhtml2="""<ion-footer style="background-color: #8c969254"><ion-navbar><ion-title style="margin-left: 33%;" >"""+jsonData['rf1']+""" <p class="subtitle">"""+jsonData['rf2']+""" </p> </ion-title></ion-navbar></ion-footer>"""
                reporthtml = headerhtml+reportheader+paramhtml+templatehtml+"""</form></ion-content>"""+footer_buttonhtml
                if not os.path.exists(filePath+"static/ionicmeta/"+ptitle+"/"+fileName):
                    os.makedirs(filePath+"static/ionicmeta/"+ptitle+"/"+fileName)

                Html_file= open(filePath+"static/ionicmeta/"+ptitle+"/"+fileName+"/"+fileName+".html","w")
                Html_file.truncate()
                Html_file.write(reporthtml)
                Html_file.close()
                view.createpage = True
                view.save()
                return HttpResponse("success")
            except Exception as e:
                print e
                return HttpResponseBadRequest("error")
        
    return HttpResponseRedirect('/reportview/repoviewdetails/')   




        




def ionicmetaJson(repojson,fileName,ptitle,request,reportid):
    filePath = settings.MEDIA_ROOT
    if not os.path.exists(filePath+"static/ionicmeta/"+ptitle+"/"+fileName):
        os.makedirs(filePath+"static/ionicmeta/"+ptitle+"/"+fileName)

    json_file= open(filePath+"static/ionicmeta/"+ptitle+"/"+fileName+"/"+fileName+".json","w")
    json_file.truncate()
    json_file.write(repojson)
    json_file.close()
    rpt =Report.objects.get(id=reportid)
    #rptt = rpt.title
    element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])
    project_title = element.project_id.title
    projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])

    if element:
            projectid = element.project_id.title
            dbprofile = element.db_profileid_id
            request.session['projectid'] = element.project_id.id
    
    dbProfileData = Db_profile.objects.get(pk=dbprofile)  
    appDbId = dbProfileData.appdb_id
    appDbData = Db_connections_info.objects.get(pk=appDbId)
        
    host = appDbData.host
    username = appDbData.username
    password = appDbData.password
    database = appDbData.dbname
    db = MySQLdb.connect(host,username,password,database)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM rprtmetadata WHERE report_id =  %s AND  project_id =  %s ",[rpt.title,projectid])
    mobileMetaData = cursor.fetchall()

    mobileSqlMetaDataStr = []
    for str in mobileMetaData:
        mobileSqlMetaDataStr.append(str[0])
    now = datetime.datetime.now()
    addComponent =  "INSERT INTO rprtmetadata (metadata,project_id,report_id,created,modified) VALUES (%(metadata)s,%(project_id)s,%(report_id)s,%(created)s,%(modified)s)"
    updateComponent =  "UPDATE rprtmetadata SET metadata=%(metadata)s, modified=%(modified)s WHERE report_id =  %s AND  project_id =  %s ",[rpt.title,projectid]
    data_comp_list = []
    data_comp_dict = {}
    comp_identifiers= []
    isThere = False    
    metaData = repojson
    if metaData:
        for component in metaData:
            rptid=rpt
        if len(mobileMetaData)==0:
            data_comp_dict = {

                'metadata': metaData,
                #'rpt_sql_type': "tx-field",                    
                'project_id':projectid,
                'report_id':rptid,
                'created':now.strftime("%Y-%m-%d %H:%M"),
                'modified':now.strftime("%Y-%m-%d %H:%M"),
            }
            data_comp_list.append(data_comp_dict)

            try:
                cursor.executemany(addComponent,data_comp_list)
                db.commit()
            except Exception as e:
                print e
                db.rollback()

        else:
            for component in metaData:
                rptid=rpt
            data_comp_dict = {
                'metadata': metaData,
                'modified':now.strftime("%Y-%m-%d %H:%M"),
                'report_id':rptid,
            }
            try:
                cursor.execute(updateComponent,data_comp_dict)
                db.commit()
            except Exception as e:
                print e
                db.rollback()


def ionicpages(ptitle,request,reportid):
    projectid = request.session['projectid']
    reportgroup = Report.objects.filter(project_id = projectid)
    project = Project.objects.get(pk = projectid)
    projectTitle = project.title
    for report in reportgroup:
        pages = reppagemeta(report.id,projectTitle)
    return  HttpResponse("success")

def reppagemeta(viewid,ptitle):
    filePath = settings.MEDIA_ROOT
    try:
        reportgroup = Report.objects.filter(id = viewid)
        reportgroup_serializer = ReportviewSerializer(instance=reportgroup,many=True)
        reportserialzier =reportgroup_serializer.data
        if reportserialzier.__len__() > 0:
            report_serializer_json = json.dumps(reportgroup_serializer.data[0])

            fileName = reportgroup_serializer.data[0]['idt']

        if os.path.exists(filePath+"static/ionicmeta/"+ptitle+"/"+fileName+"/"+fileName+".html"):
            if not os.path.exists(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName):
                os.makedirs(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName)

            with open(filePath+"static/ionicmeta/"+ptitle+"/"+fileName+"/"+fileName+".html") as f:
                with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".html", "w") as f1:
                    f1.truncate()

                    for line in f:                        
                        f1.write(line)
                           

        tsPage = tsFile(fileName,ptitle)
        scssPage = scssFile(fileName,ptitle)
        metajson = pagejson(fileName,ptitle)
        copyReportTemplate(viewid,fileName,ptitle)
        return "success"
    except Exception as e:
        print e
        return "error"

def copyReportTemplate(viewid,fileName,ptitle):

    filePath = settings.MEDIA_ROOT
    reportViewObj = Report.objects.get(id = viewid)
    try:
		actionObj = ReportAction.objects.get(report_id = viewid,report_action="print_format")
		txnPFObj = ReportPrintFormatAction.objects.get(report_action_id = actionObj.id)
    except ReportAction.DoesNotExist:
		actionObj = None
		txnPFObj = None
    
    if txnPFObj:
        pfConfigObj = PrintFormat.objects.get(id=txnPFObj.pfconfig_id)
        FileUrl = pfConfigObj.htmlfile
      
        if os.path.exists(filePath+str(FileUrl)):
            if not os.path.exists(filePath+"ionicapps/"+ptitle+"/src/assets/mustache"):
                os.makedirs(filePath+"ionicapps/"+ptitle+"/src/assets/mustache")

            with open(filePath+str(FileUrl)) as f:
                with open(filePath+"ionicapps/"+ptitle+"/src/assets/mustache/"+fileName+".html", "w") as f1:
                    for line in f:
                        f1.write(line)
        else:
            raise Exception("Could not a find a uplaoded html file for "+txviewObj.identifiers+" view")
        
	return "success"

def tsFile(fileName,ptitle):
    filePath = settings.MEDIA_ROOT
    with open(filePath+"static/ionicsrc/report/report.ts") as f:
        with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".ts", "w") as f1:
            for line in f:
                f1.write(line)

    with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".ts", "r") as file :
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('page-report', 'page-'+fileName)
    filedata = filedata.replace('report.html', fileName+'.html')
    filedata = filedata.replace('ReportPage', fileName.capitalize()+'Page')
    filedata = filedata.replace('report.json', fileName+'.json')
    filedata = filedata.replace('report_id', fileName)
    # Write the file out again
    with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".ts", "w") as file:
        file.write(filedata)

    appincludeTs(fileName,ptitle)
    
    if os.path.exists(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"modal/"):
        with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".ts", "r") as modalfile :
            modalfiledata = modalfile.read()

        # Replace the target stringmodal
        modalfiledata = modalfiledata.replace('HomePage', fileName.capitalize()+'modalPage')
        modalfiledata = modalfiledata.replace('../home/home','../'+fileName+'modal/'+fileName+'modal')

        with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".ts", "w") as modal:
            modal.write(modalfiledata)

    return filedata

def metajson(request):
    lines =""
    with open("ionichtml/app.module.ts") as f:
        lines = f.readlines()
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



def appincludeTs(fileName,ptitle):
    filePath = settings.MEDIA_ROOT
    with open(filePath+"ionicapps/"+ptitle+"/src/app/app.module.ts") as f:
        lines = f.readlines()
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

    with open(filePath+"ionicapps/"+ptitle+"/src/app/app.module.ts","w") as file:
        for tslines in lines:
            file.write(tslines)

    return lines  

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

def scssFile(fileName,ptitle):
    filePath = settings.MEDIA_ROOT
    with open(filePath+"static/ionicsrc/report/report.scss") as f:
        with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".scss", "w") as f1:
            for line in f:
                f1.write(line)

    with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".scss", "r") as file :
        filedata = file.read()

    filedata = filedata.replace('page-report', 'page-'+fileName)
    with open(filePath+"ionicapps/"+ptitle+"/src/pages/"+fileName+"/"+fileName+".scss", "w") as file:
        file.write(filedata)    

    return filedata


def add_action_report(request,report_id):

    action_type=ReportAction.objects.filter(report_id=report_id) 
    action_ids=[action.report_action for action in action_type]
    report=Report.objects.get(id=report_id)

    if request.method=="GET":
        form=ReportActionForm(initial={'report_action':action_ids})        
        return render(request,"reportactions.html",locals())

    if request.method=="POST":
        form=ReportActionForm(request.POST,initial={ 'report_action': action_ids})
        
        if form.is_valid():

            if action_type:
                action_list = form.cleaned_data['report_action']
                query = ReportAction.objects.filter(report_id = report_id)
                table =[]
                newtable =[]
                if len(action_list)>0:
                    for types in query:
                        if types.report_action in action_list:
                            table.append(types.report_action)
                        else:
                            typedelete = ReportAction.objects.filter(report_action = types.action_type,report_id = report_id)
                            typedelete.delete() 

                    for actions in action_list:
                        if actions in table:
                            newtable.append(actions)
                        else:
                            type = ReportAction.objects.create(report_action=actions,order = 0 ,report_id = report_id,title=actions)
                            type.save()

                return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))       

            else:
                action_list = form.cleaned_data['report_action']
                for action in action_list:
                    type = ReportAction.objects.create(report_action=action,order = 0 ,report_id = report_id,title=action)
                    type.save()

                return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))
        else:
            return HttpResponse('failure')    

    else:
        form = ReportActionForm(initial={'action_type':action_ids}) 
        return render(request,'reportactions.html',locals())


@csrf_exempt
def print_format_config(request,title,pk):
    pid = request.session['projectid']
    print_format_config_id = pk
    
    try:
        printformat=ReportPrintFormatAction.objects.get(report_action_id=pk)
        rpf_form=ReportPrintFormatActionForm(request.POST or None,instance=printformat)
        rpf_form.fields['pfconfig'].queryset = PrintFormat.objects.filter(project_id=pid)
        
    except Exception as e:
        rpf_form=ReportPrintFormatActionForm(request.POST or None,request.FILES or None)
        rpf_form.fields['pfconfig'].queryset = PrintFormat.objects.filter(project_id=pid)
        

    if request.method == "POST":
        print rpf_form.is_valid()
        if rpf_form.is_valid():
            try:
                pfaction=rpf_form.save(commit=False)
                pfaction.report_action_id = pk
                pfaction.save()
                return HttpResponse("Success")
            except Exception as e:
                print e
                return HttpResponse("Failure")

        else:
            print rpf_form.errors
            return HttpResponse("Failure")
                
    else:
        return render(request,"reportprintformat.html",locals())

@csrf_exempt
def report_pdf(request,title,pk):
    report=Report.objects.get(pk=title)
    try:
        pdf=ReportPDF.objects.get(report_id=title,report_action_id=pk)
        form=ReportPDFForm(request.POST or None,instance=pdf)
    except:
        form=ReportPDFForm(request.POST or None)

    if request.method=="POST":
        if form.is_valid():
            pdfrepo=form.save(commit=False)
            pdfrepo.report_id=title
            pdfrepo.report_action_id=pk
            pdfrepo.save()
            return HttpResponseRedirect('/reportview/editReport/%s' %(request.session['reportid']))
        else:
            return HttpResponseBadRequest("save error")
    else:        
        return render(request,"reportpdf.html",locals())

@csrf_exempt
def payment(request,title,pk):
    payment_config_id = pk
    report=Report.objects.get(pk=title)
    try:
        pdf=Payment.objects.get(report_id=title,report_action_id=pk)
        form=PaymentForm(request.POST or None,instance=pdf)
    except:
        form=PaymentForm(request.POST or None)

    if request.method=="POST":
        if form.is_valid():
            payment=form.save(commit=False)
            payment.report_id=title
            payment.report_action_id=pk
            payment.save()
            return HttpResponseRedirect('/reportview/editReport/%s' %(request.session['reportid']))
        else:
            return HttpResponseBadRequest("save error")
    else:        
        return render(request,"payment.html",locals())


@csrf_exempt
def newaction(request,title,pk):
    newaction_config_id = pk
    report=Report.objects.get(pk=title)
    try:
        new=NewAction.objects.get(report_id=title,report_action_id=pk)
        form=NewActionForm(request.POST or None,instance=new)
    except:
        form=NewActionForm(request.POST or None)

    if request.method=="POST":
        if form.is_valid():
            newactionform=form.save(commit=False)
            newactionform.report_id=title
            newactionform.report_action_id=pk
            newactionform.save()
            return HttpResponseRedirect('/reportview/editReport/%s' %(request.session['reportid']))
        else:
            return HttpResponseBadRequest("save error")
    else:        
        return render(request,"reportnewaction.html",locals())
                
ReportMapFormSet = modelformset_factory(ReportEpostMap,form = ReportEpostMapForm,can_delete=True,extra=1)

@csrf_exempt
@transaction.atomic
def report_submit(request,title,pk):
    tx =""
    submit_id = pk
    report=Report.objects.get(pk=title)
    pid = request.session['projectid']
    try:
        submit_action=ReportSubmit.objects.get(report_id=title,report_action_id=pk)
        if request.POST:
            tx = request.POST.get('epost_target')
        else:
            tx = submit_action.epost_target_id

        form=ReportSubmitForm(request.POST or None,instance=submit_action,pid = pid)
        formset = ReportMapFormSet(request.POST or None,queryset=ReportEpostMap.objects.filter(reportsubmit_id = submit_action.id),form_kwargs={'reportid': report.id,'tx':tx})
    except Exception as e:
        if request.POST:
            tx = request.POST.get('epost_target')
        form=ReportSubmitForm(request.POST or None,pid = pid)
        formset = ReportMapFormSet(request.POST or None,queryset=ReportEpostMap.objects.none(),form_kwargs={'reportid': report.id,'tx':tx})

    if request.POST:
        tx = request.POST.get('epost_target')


        try:
            if form.is_valid():
                try:
                    submitrepo=form.save(commit=False)
                    submitrepo.report_id=title
                    submitrepo.report_action_id=pk
                    submitrepo.save()

                    if formset.deleted_forms:
                        for eform in formset.deleted_forms:
                            if eform.instance.pk:
                                eform.instance.delete()
                            else:
                                pass

                    if formset.is_valid():
                        instance = formset.save(commit = False)
                        for item in instance:
                            item.reportsubmit_id = submitrepo.id
                            item.save()

                    return HttpResponse("Saved Successfully")
                except Exception as ep:
                    print ep
                    return HttpResponseBadRequest("Error")

        except:
            pass

    else:
        return render(request,"reportsubmit.html",locals())

       
def report_csv(request,title,pk):
    try:
        reportcsv=ReportCSV.objects.get(report_id=title,report_action_id=pk)
        form=ReportCSVForm(request.POST or None,instance=reportcsv)
    except:
        form=ReportCSVForm(request.POST or None)

    if request.method=="POST":
        if form.is_valid():
            csvrepo=form.save(commit=False)
            csvrepo.report_id=title
            csvrepo.report_action_id=pk
            csvrepo.save()
            return HttpResponseRedirect('/reportview/editReport/%s' %(request.session['reportid']))
        else:
            return HttpResponseBadRequest("Save Error")

    else:
        return render(request,"reportcsv.html",locals())

def report_html(request,title,pk):
    try:
        html=ReportHTML.objects.get(report_id=title,report_action_id=pk)
        form=ReportHTMLForm(request.POST or None,instance=html)
    except:
        form=ReportHTMLForm(request.POST or None)

    if request.method=="POST":
        if form.is_valid():
            htmlrepo=form.save(commit=False)
            htmlrepo.report_id=title
            htmlrepo.report_action_id=pk
            htmlrepo.save()
            return HttpResponseRedirect('/reportview/editReport/%s' %(request.session['reportid']))
        else:
            return HttpResponseBadRequest("Save Error")

    else:
        return render(request,"reporthtml.html",locals())

def delaction(request,title,pk):
    report=Report.objects.get(pk=title)
    action=ReportAction.objects.get(id=pk)
    #querydel=ReportCSV.objects.get(report_action_id=pk)
    action.delete()
    #querydel.delete()
    return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))


def action_button_html(actionbutton,reporttype):
    dict = {}
    try:
        actionhtml = ""
        actionstart =""
        actionend=""
        actionlist =""
        buttonhtml =""
        actionstart="""<ion-fab top right><button ion-fab mini style="margin:0px;" ><ion-icon name="star"></ion-icon></button><ion-fab-list side="bottom" style="margin:44px -8px">"""
        for action  in actionbutton:
            if action['at'] ==  'pdf':
                pdf = action['ReportPDF']
                if pdf:
                    actionlist += """<button ion-fab form="form_id" (click)="pdf()" data-exp=\""""+pdf['exp']+"""\" ><ion-icon md=\""""+pdf['icls']+"""\" ></ion-icon><ion-label>Pdf</ion-label></button>"""
                else:
                    actionlist+="""""" 

            if action['at'] == 'csv':
                csv = action['ReportCSV']
                if csv:
                    actionlist += """<button ion-fab (click)="csv()" data-exp=\""""+csv['exp']+"""\" ><ion-icon md=\""""+csv['icls']+"""\" ></ion-icon><ion-label>Csv</ion-label></button>"""
                else:
                    actionlist+=""""""     

            if action['at'] == 'print_format':
                if reporttype == "displayreport":
                    pf = action['ReportPrintFormatAction']
                    if pf:
                        buttonhtml += """<button ion-button full color="primary" (click)="printReport($event)" data-reporttype="displayreport">Print Preview</button>"""    
                    else:
                        buttonhtml+=""""""

            if action['at'] == 'html':
                delete = action['ReportHTML']
                if delete:
                    actionlist += """<button ion-fab (click)="delete()" data-exp=\""""+delete['exp']+"""\" data-pos=\""""+delete['pos']+"""\"><ion-icon md=\""""+delete['icls']+"""\" ></ion-icon><ion-label>Delete</ion-label></button>"""
                else:
                    actionlist+=""""""     

            if action['at'] == 'new':
              
                newAction = action['NewActionConfig']
               
                if newAction:
                    if newAction['click']:
                        click = """(click)=\""""+newAction['click']+"""\""""
                    else:
                        click = ""
                    actionlist += """<button ion-fab """+click+""" data-exp=\""""+newAction['exp']+"""\" ><ion-icon name=\""""+newAction['icls']+"""\"></ion-icon><ion-label>newAction</ion-label></button>"""       
                else:
                    actionlist+=""""""

            if action['at'] == 'submit':
                sfield =""
                submit = action['ReportSubmit']
                if submit:
                    if submit['click']:
                        click = """(click)=\""""+submit['click']+"""\""""
                    else:
                        click = ""
                    actionlist += """<button ion-fab """+click+""" data-exp=\""""+submit['exp']+"""\" ><ion-icon name=\""""+submit['icls']+"""\"></ion-icon><ion-label>Submit</ion-label></button>"""       
                else:
                    actionlist+="""""" 

            if action['at'] == 'payment':
                pay = action['Payconfig']
                if pay:
                    if pay['click']:
                        click = """(click)=\""""+pay['click']+"""\""""
                    else:
                        click = ""
                    buttonhtml+="""<button ion-button full color="primary" """+click+""" data-exp=\""""+pay['exp']+"""\">Pay Now</button>"""
                else:
                    buttonhtml+=""""""

                

       
        actionend="""</ion-fab-list></ion-fab>"""
        actionhtml=actionstart+actionlist+actionend
        dict['button'] = "<ion-footer>"+buttonhtml+"</ion-footer>"
        dict['fab'] = actionhtml
        return json.dumps(dict)
    except Exception as e:
       
        print e
        raise e

    
