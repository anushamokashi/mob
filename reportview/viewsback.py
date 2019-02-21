# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from Mobilebuilder.decorators import myuser_login_required 
from reportview.forms import ReportForm,ReportGroupingForm,ReportParamFieldForm,ReportFieldForm,ReportGroupingForm,QueryForm
from project.models import Project, Projectwiseusersetup
from authentication.models import userprofile
from reportview.models import Report,ReportParamField,Query,ReportField,ReportGrouping,ReportAction
#from report.serializers import ReportSerializer
from django.shortcuts import get_list_or_404, get_object_or_404
import re
from schema.models import Db_connections_info, Db_profile
from django.conf import settings
import MySQLdb
import cx_Oracle as oracle
# from django.utils.text import slugify
#from slugify import slugify, Slugify, UniqueSlugify
from unidecode import unidecode
from django.template import defaultfilters
from reportview.serializers import ReportviewSerializer
import datetime
import string
import json
import os
import zipfile
import StringIO
from hometemplate.models import Homepage
#from django.template.defaultfilters import slugify





# Create your views here.
@myuser_login_required
def reportview(request):
    print request.session['userid']
    loginModel = userprofile.objects.get(is_user = True ,id = request.session['userid'])
    element =Projectwiseusersetup.objects.get(userid=loginModel.id,project_id = request.session['projectid'])
    projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])
    
    instance = Report.objects.all()
    form = ReportForm()
    #for title in instance:
    #print title.id
    return render(request, 'reportview.html', locals())

def reportedit(request,title):
    #print 'title',title
    element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])
    project_title = element.project_id.title
    projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])
    form = ReportForm()
    edit=Report.objects.get(pk=title)
    #print edit .id
    request.session['reportid']=edit .id
    params = ReportParamField.objects.filter(report_id=title)

    query=Query.objects.filter(report_id=title)
    field=ReportField.objects.filter(report_id=title)
    grouping=ReportGrouping.objects.filter(report_id=title)
    #br=ReportBusinessRule.objects.filter(report_id=title)   
    
    #print "edit",edit
    

    return render(request, "reportedit.html",locals())
    #return HttpResponseRedirect('/reportview/editReport/')


@csrf_exempt
def saveReports(request):
    reportTitle = ""
    parentReportId = ""
    metaData = ""
    project_id = request.session['projectid']
    pid = Project.objects.get(pk = project_id)
    #print pid
    #print project_id

    if request.method == "POST":
        print request.POST
        form = ReportForm(request.POST)
        #print form
        if form.is_valid():
            #print 'ok'
            newreport = form.save(commit=False)
            newreport.project_id = pid.id
            newreport.save()
        else:
            print 'ok'
            print form.errors
         
      
    
    return HttpResponseRedirect('/reportview/repoviewdetails/')

def editmodal(request,title):
    print "calling"
    edit=Report.objects.get(pk=title)
    print edit.id
    form = ReportForm()
    return render(request, "editdetails.html", locals()) 


def updateReport(request,reportId):
    #print "printtttttttttttttuuuuuuuuuuu"
    element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])
    project_title = element.project_id.title
    projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])

    repo=Report.objects.get(pk=reportId)
    #print "repo", repo
    form = ReportForm(request.POST,instance = repo)

    if request.POST:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))

          
        else:
            print form.errors

            return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))

def delReport(request,title):

    query = Report.objects.get(pk = title)
    query. delete()
    return HttpResponseRedirect('/reportview/repoviewdetails/')




def parammodal(request,title):
    #print "calling"
    param=Report.objects.get(pk=title)
    #print "param",param.id
    paramform = ReportParamFieldForm()    
    report_param_list = ReportParamField.objects.filter(report_id = param.id)
    #print report_param_list
    # for para in report_param_list:
    #     print para
    #     comp_dest = {"id":"",
    #     "slug":"",
    #     "title":""}
    #     comp_dest["id"]=para.id
    #     comp_dest["slug"]=para.slug
    #     comp_dest["title"]=para.title
    #     comp_list.append(comp_dest)
    #     print comp_list


    return render(request, "reportparam.html",locals()) 
  

def saveparams(request, repoid):
    #print 'comein'
    #print repoid
    #print brtitle

  
    if request.method == "POST":
        form = ReportParamFieldForm(request.POST)
        #form2 =ReportParamBusinessRuleForm(request.POST)


        if form.is_valid() :
            print 'ok'
            paramreport = form.save(commit=False)
            paramreport.report_id = repoid
            paramreport.save()
            
            # brReport=form2.save(commit=False)
            # brReport.title=request.POST.get('brtitle')
            # brReport.report_id =repoid
            # brReport.report_param_field_id = paramreport.id
            # brReport.save()
            return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))

            #paramreport.projectid_id = project_id
           
            
        else:
           # print form2.errors
            print form.errors

        return HttpResponseRedirect('/reportview/editReport/')



 
def parameditmodal(request,title,pk):
    print 'oh',title
    print 'ok',pk
    paramform = ReportParamFieldForm()
    # instance = ReportParamField.objects.filter(id=pk)

    # for title in instance:
    #     #print 'fk',title.report_id

    #     comp_list = []
    #     report_param_field_list = ReportParamField.objects.filter(report_id = title.report_id)
    # #print report_param_list

    # for title in report_param_field_list:
    #     #print title
    #     comp_dest = {"id":"",
    #     "slug":"",
    #     "title":""}
    #     comp_dest["id"]=title.id
    #     comp_dest["slug"]=title.slug
    #     comp_dest["title"]=title.title
    #     comp_list.append(comp_dest)    

    #parameditform = ReportParamFieldForm()

    rpt_param = get_object_or_404(ReportParamField,pk=pk)
    print rpt_param.id

    # if rpt_param:
    #     rpt_business_rule = get_object_or_404(ReportBusinessRule,report_param_field_id=rpt_param.id)
       
    if request.POST:
        rpt_param_form = ReportParamFieldForm(request.POST,instance=rpt_param)
        #rpt_br_form = ReportParamBusinessRuleForm(request.POST,instance=rpt_business_rule)


        if rpt_param_form.is_valid() :
            rpt_param_form.save()
           

            # rpt_br_obj = rpt_br_form.save(commit=False)
            # rpt_br_obj.title=request.POST.get('brtitle')
            # rpt_br_obj.report_id = rpt_param.report_id
            # rpt_br_obj.report_param_field_id = rpt_param.id
            # #print rpt_br_form.report_param_field_id
            # rpt_br_obj.save()

            return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))
        else:
            print rpt_param_form.errors
            #print rpt_br_form.errors  

    else:
        rpt_param_form = ReportParamFieldForm(instance=rpt_param)
        #rpt_br_form = ReportParamBusinessRuleForm(instance=rpt_business_rule) 
        #print  rpt_param_form,rpt_param_form  

    return render(request, "editparam.html",locals()) 


def delparam(request,title):

    query = ReportParamField.objects.get(pk = title)
    
    query.delete()
    return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))

def fieldmodal(request,title):
    #print "field"
    field=Report.objects.get(pk=title)
    #print field.id
    fieldform = ReportFieldForm()
    # comp_list = []
    # report_field_list = ReportParamField.objects.filter(report_id = field.id)
    # #print report_param_list
    # for sql in report_field_list:
    #     print sql
    #     comp_dest = {"id":"",
    #     "slug":"",
    #     "title":""}
    #     comp_dest["id"]=sql.id
    #     comp_dest["slug"]=sql.slug
    #     comp_dest["title"]=sql.title
    #     comp_list.append(comp_dest)


    return render(request, "field.html",locals())

def fieldsave(request,repoid):
    #print "field"
    #print repoid

    if request.method == "POST":
        form = ReportFieldForm(request.POST)
        #form2=ReportFieldBusinessRuleForm(request.POST)

        if form.is_valid() :
            print 'ok'
            reportfield = form.save(commit=False)
            reportfield .report_id = repoid
            reportfield.save()
            
            # reportBR=form2.save(commit=False)
            # reportBR.title=request.POST.get('fieldtitle')
            # reportBR.report_id = repoid
            # reportBR.report_field_id = reportfield.id
            # reportBR.save()
            return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))
            
        else:
            print form.errors
            #print form2.errors

    return HttpResponseRedirect('/reportview/editReport/')

def fieldeditmodal(request,pk,title):
    #print "field"
    print title
    print pk
    instance = ReportField.objects.filter(id = pk)

    #for title in instance:
        #print 'fk',title.report_id
    #     comp_list = []
    #     report_field_list = ReportParamField.objects.filter(report_id = title.report_id)
    # #print report_param_list
    # for title in report_field_list:
    #     #print title
    #     comp_dest = {"id":"",
    #     "slug":"",
    #     "title":""}
    #     comp_dest["id"]=title.id
    #     comp_dest["slug"]=title.slug
    #     comp_dest["title"]=title.title
    #     comp_list.append(comp_dest)


    rpt_field = get_object_or_404(ReportField,pk=pk)
    #print rpt_field.id
    # if rpt_field:
    #     rpt_business_rule = get_object_or_404(ReportBusinessRule,report_field_id=rpt_field.id)

    if request.POST:
        rpt_field_form = ReportFieldForm(request.POST,instance=rpt_field)
        #rpt_br_form = ReportFieldBusinessRuleForm(request.POST,instance=rpt_business_rule)
        if rpt_field_form.is_valid():
            fieldupdate=rpt_field_form.save(commit=False)
            fieldupdate.save()
            return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))
            # BRupdate = rpt_br_form.save(commit =False)
            # BRupdate.title=request.POST.get('fieldtitle')
            # BRupdate.report_id = rpt_field.report_id
            # BRupdate.report_field_id = rpt_field.id
            # BRupdate.save()
            #print 'ok'

          
        
        else:
            print  rpt_field_form.errors 
            #print  rpt_br_form.errors 

    else:
        rpt_field_form = ReportFieldForm(instance=rpt_field)
        #rpt_br_form = ReportFieldBusinessRuleForm(instance=rpt_business_rule)


    return render(request, "fieldedit.html",locals()) 

def delfield(request,title):

    query = ReportField.objects.get(pk = title)
    
    query.delete()
    return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))


def BRmodal(request,title):
    #print "calling"
    BR =Report.objects.get(pk=title)
    #print BR.id
    #print "hi"
    form = ReportBusinessRuleForm()
    #form1 = ReportFieldBusinessRuleForm()
    comp_list = []
    report_br = ReportParamField.objects.filter(report_id = BR.id)
    #print report_param_list
    for titles in report_br:
        print titles
        comp_dest = {"id":"",
        "slug":"",
        "title":""}
        comp_dest["id"]=titles.id
        comp_dest["slug"]=titles.slug
        comp_dest["title"]=titles.title
        comp_list.append(comp_dest)


    return render(request, "businessrule.html",locals())




def brsave(request,repoid):
    #print "br"
    
    if request.method == "POST":
        form = ReportBusinessRuleForm(request.POST)        
        
        if form.is_valid() :
            #print 'ok'
            br = form.save(commit=False)
            br.title=request.POST.get('businesstitle')
            br .report_id = repoid
            br.save()
            return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))
            #return HttpResponseRedirect('/reportview/editReport/')
            
        else:
            print form.errors
            
    return HttpResponseRedirect('/reportview/editReport/')

def BRedit(request,title,pk):
    #print "calling"
    form = ReportBusinessRuleForm()
    #print title
    #print pk
  
    comp_list = []
    reports = ReportParamField.objects.filter(report_id =title)
    #print report_param_list
    for titles in reports:
        print titles
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
            print rpt_br_form.title
            rpt_br_form .report_id = report_br.report_id
            print rpt_br_form .report_id 
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
    #print "calling"
    report =Report.objects.get(pk=title)
    #print report.id
    rpt_group_form = ReportGroupingForm()
    comp_list = []
    report_br = ReportField.objects.filter(report_id =title)
    #print report_param_list
    for titles in report_br:
        print titles
        comp_dest = {"id":"",
        "slug":"",
        "title":""}
        comp_dest["id"]=titles.id
        comp_dest["slug"]=titles.slug
        comp_dest["title"]=titles.title
        comp_list.append(comp_dest)
    
    return render(request, "grouping.html",locals()) 

def groupingsave(request,repoid):
    #print "groupsave"
    #print repoid

    if request.method == "POST":
        print request.POST
        form = ReportGroupingForm(request.POST)
        
        if form.is_valid() :
            print 'ok'
            group = form.save(commit=False)
            group.report_id = repoid
            group.save()

            return HttpResponseRedirect('/reportview/editReport/%s'% (repoid))
            
        else:
            print form.errors
            
    return render(request, "reportedit.html",locals())

def groupeditmodal(request,title,pk):
    # print "field"
    print title
    print pk
    comp_list=[]
    # instance = Report.objects.all()

    # for title in instance:
    #    print title.id 
    #print "rpt_group",rpt_group
    #rpt_group = get_object_or_404(ReportGrouping.objects.get(report_id = title))
    report_br = ReportField.objects.filter(report_id =title)
    #print report_param_list
    for titles in report_br:
        print titles
        comp_dest = {"id":"",
        "slug":"",
        "title":""}
        comp_dest["id"]=titles.id
        comp_dest["slug"]=titles.slug
        comp_dest["title"]=titles.title
        comp_list.append(comp_dest)
    rpt_group=ReportGrouping.objects.get(pk=pk)
    print "rpt_group",rpt_group

    if request.POST:
        rpt_group_form = ReportGroupingForm(request.POST,instance=rpt_group)

        if rpt_group_form.is_valid():
            rpt_group_form.save()

            return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))

        else:
             print rpt_group_form.errors

             return HttpResponseRedirect('/reportview/editReport/',locals())
             #return render(request, "reportedit.html",locals())

    else:
        rpt_group_form =ReportGroupingForm(instance=rpt_group)


    return render(request, "groupedit.html",locals())


def delgroup(request,title):  
    print request.session['reportid']

    query = ReportGrouping.objects.get(pk = title)
    query. delete()
    return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))


def Querymodal(request,title):
    #print "yesss"
    query=Report.objects.get(pk=title)
    #print query.id

    form = QueryForm()
    # comp_list = []
    # report_field_list = ReportParamField.objects.filter(report_id = query.id)
    # #print report_param_list
    # for sql in report_field_list:
    #     print sql
    #     comp_dest = {"id":"",
    #     "slug":"",
    #     "title":""}
    #     comp_dest["id"]=sql.id
    #     comp_dest["slug"]=sql.slug
    #     comp_dest["title"]=sql.title
    #     comp_list.append(comp_dest)
    
    return render(request, "query.html",locals())
    
def reportQuerySave(request,repoid):
    #print"entering to query........"
    #general_slug = slugify()
    #general_slug.separator='_'
    report = Report.objects.get(id = repoid)   
    # project = Project.objects.get(slug= report.project.slug)
    # print 'project',project 
    element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])
    print element,'element'
    project_title = element.project_id.title
    projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])

    if element:

        projectid = element.project_id.id
        dbprofile = element.db_profileid_id
        request.session['projectid'] = element.project_id.id
        #print projectid
        #print dbprofile
        #print request.session['projectid'] 

        #ADMIN DB    
    dbProfileData = Db_profile.objects.get(pk=dbprofile)  
    print 'dbProfileData',dbProfileData 
    appDbId = dbProfileData.appdb_id
    #print adminDbId    
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
  
    
    if request.method=="POST":
        form=QueryForm(request.POST)
        report_query_title = request.POST.get('title')
        #print request.POST
        #print report_query_title
      
        if form.is_valid():
            fieldquery=form.save(commit=False)
            fieldquery.report_id = repoid            
            fieldquery.slug =defaultfilters.slugify(report_query_title) 
            fieldquery.save()
            #print fieldquery.is_main_query
            resp={}
            resp['data']="save"
            resp['data_msg']="successfully saved"
            print "saved sucessfully"
            #return HttpResponse("Success")
            report_query_sql = request.POST.get('sql')
            param_list = parse_params(report_query_sql)
            print 'params',param_list

            if fieldquery.is_main_query==True and fieldquery.sql is not None:

                for param in param_list:
                    #if param not in param_array:
                        print param
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
                            print report_param_field_form.errors


                reportquery = request.POST.get('is_main_query')
                print reportquery
                #result = db_resultset(report.project,fieldquery.sql,request.user)
                #print 'result',result
                sql_string = str(report_query_sql)
                match = re.compile(r":\w+")
                items = re.findall(match,sql_string)
                for item in items:
                    print item
                    sql_string = str(sql_string).replace(item, sql_value_replace(str(item)),1)

                cursor.execute(sql_string)
                field_list = cursor.description
                print "field_list",field_list

                for result_field in field_list:
                    print result_field
                    #print repoid
                    report = Report.objects.get(id = repoid)
                    report_field_slug=result_field[0].lower()

                    #reportfield = ReportField.objects.get(report_field__iexact=result_field[0],query=fieldquery,report_id=repoid)
                    #reportfield.save()
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
                                                                 #'data_type':data_type,
                                                                 'no_of_decimal_digits':0,
                                                                 'show_running_total':False,
                                                                 'show_total':False,
                                                                 'is_hidden':False,
                                                                 'apply_comma':False,
                                                                 'dont_repeat':False,
                                                                 #'column_alignment':column_align,
                                                                 'dont_show_zero':False,
                                                                 'display_order':display_order,
                                                                 'template':'',
                                                                 #'pivot_column_type':None,
                                                                 'width':0,
                                                                 'height':0,
                                                                 'is_bold_font':False,
                                                                 'color':''} )

                    if report_field_form.is_valid():
                                report_field = report_field_form.save(commit=False)
                                report_field.report = report
                                report_field.save()

                    else:
                        print report_field_form.errors


            return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))
            
        else:
            
            print form.errors

    else:
        return render(request, "reportedit.html",locals())
       
    #return HttpResponse(json.dumps(resp)) 
    #return render(request, "reportedit.html",locals())

def sql_value_replace(match):
    return 'null'

def db_resultset(project,sql,userId):
    print project 
    print sql
    print userId
    
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
    #print sql
    param_list=[]
    match = re.compile(r":\w+")
    items = re.findall(match,str(sql))
    #print items
    for item in items:
        #print item
        item = item.replace(':','')
        param_list.append(item)
        
        
    return param_list  


def Queryeditmodal(request,pk,title):
    print title
    print pk
    report = Report.objects.get(id = title) 
    query=Query.objects.get(pk=pk)
    print query.sql
    element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])
    project_title = element.project_id.title
    projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])

    if element:

        projectid = element.project_id.id
        dbprofile = element.db_profileid_id
        request.session['projectid'] = element.project_id.id
        #print projectid
        #print dbprofile
        #print request.session['projectid'] 

        #ADMIN DB    
    dbProfileData = Db_profile.objects.get(pk=dbprofile)  
    #print dbProfileData  
    appDbId = dbProfileData.appdb_id
    #print adminDbId    
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
    if request.POST:
        form=QueryForm(request.POST, instance = query)
        query_title = request.POST.get('title')

        if form.is_valid():
            queryupdate=form.save(commit=False)
            queryupdate.report_id = title
            queryupdate.save()

            if queryupdate.is_main_query==True and queryupdate.sql is not None:
                paramdel = ReportParamField.objects.get(query_id = pk) 
                print 'paradel',paramdel
                paramdel.delete()
                report_query_sql = request.POST.get('sql')
                param_list = parse_params(report_query_sql)
                print param_list

                for param in param_list:
                    print 'param', param
                    report_parameter_slug=param.lower()
                    print 'slug',report_parameter_slug
                    #report = Report.objects.get(id = title) 
                    rpt_param_fields = ReportParamField.objects.filter(report_id = report).order_by('display_order')
                    print rpt_param_fields
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
                                           print report_param_field.report_id
                                           report_param_field.save()

                    else:
                                print report_param_field_form.errors


                            #else:
                               # pass                                    
                                #param_array.append(param)
                    
                   
                    reportquery = request.POST.get('is_main_query')
                    print reportquery
                    #result = db_resultset(report.project,fieldquery.sql,request.user)
                    fielddel = ReportField.objects.filter(query_id = pk).delete() 
                    print 'fielddel',fielddel
                    #fielddel.delete()
                    print 'report_query_sql',report_query_sql
                    sql_string = str(report_query_sql)
                    match = re.compile(r":\w+")
                    items = re.findall(match,sql_string)
                    for item in items:
                        print item
                        sql_string = str(sql_string).replace(item, sql_value_replace(str(item)),1)
                        print sql_string
                         
                    cursor.execute(sql_string)
                    field_list = cursor.description
                    print field_list


                for result_field in field_list:
                        print result_field
                        report = Report.objects.get(id = title)
                        report_field_slug=result_field[0].lower()
                        #reportfield = ReportField.objects.get(report_fields__iexact=result_field[0],query=fieldquery,report_id=repoid)
                        #reportfield.save()
                        report_fields_order = ReportField.objects.filter(report_id=report).order_by("display_order")
                        #print report_fields_order
                        # if report_fields_order.count() != 0:
                        #         report_field_order = report_fields_order.first().display_order                                
                        #         field_disp_order = report_field_order+1
                        if report_fields_order:
                                field_disp_order = report_fields_order.last().display_order+1
                                #print  field_disp_order                               
                                #display_order = field_disp_order+1
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
    print 'delete',title
    query = Query.objects.get(pk = title)
    paramdelete = ReportParamField.objects.filter(query_id=title)
    fielddelete = ReportField.objects.filter(query_id=title)
    paramdelete. delete()
    fielddelete. delete()
    query. delete()
    return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))



def reportact(request,title):
    print 'hi'

    return render(request,"reportactions.html",locals())
          


def reportviewjson(request,reportid):
    print reportid
    rpt =Report.objects.get(id=reportid)
    rptt = rpt.title
    print rptt
    filePath = settings.MEDIA_ROOT
    reportgroup = Report.objects.filter(id = reportid)
    reportgroup_serializer = ReportviewSerializer(instance=reportgroup,many=True)
    reportserialzier =reportgroup_serializer.data
    if reportserialzier.__len__() > 0:
        report_serializer_json = json.dumps(reportgroup_serializer.data[0])
        #print report_serializer_json
        json_file= open(filePath+"static/json/data/data.json","w")
        json_file.write(report_serializer_json)
        json_file.close()
        element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])
        project_title = element.project_id.title
        projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])

    if element:
            projectid = element.project_id.title
            dbprofile = element.db_profileid_id
            request.session['projectid'] = element.project_id.id

    dbProfileData = Db_profile.objects.get(pk=dbprofile)  
    adminDbId = dbProfileData.admindb_id
    #print adminDbId    
    adminDbData = Db_connections_info.objects.get(pk=adminDbId)
        
    host = adminDbData.host
    #print host
    username = adminDbData.username
    #print username
    password = adminDbData.password
    #print password
    database = adminDbData.dbname
            #print database
    db = MySQLdb.connect(host,username,password,database)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM rprtmetadata WHERE report_id =  %s",[rpt.title])
    mobileMetaData = cursor.fetchall()
    print "mobilemetadata", mobileMetaData

    #converting tuple to str
    mobileSqlMetaDataStr = []
    for str in mobileMetaData:
        mobileSqlMetaDataStr.append(str[0])
    print 'mobileSqlMetaDataStr',mobileSqlMetaDataStr
    now = datetime.datetime.now()
    addComponent =  "INSERT INTO rprtmetadata (metadata,project_id,report_id,created,modified) VALUES (%(metadata)s,%(project_id)s,%(report_id)s,%(created)s,%(modified)s)"
    updateComponent =  "UPDATE rprtmetadata SET metadata=%(metadata)s, modified=%(modified)s WHERE report_id = %(report_id)s"
    data_comp_list = []
    data_comp_dict = {}
    comp_identifiers= []
    isThere = False    
    metaData = report_serializer_json
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
            #print data_comp_dict

            try:
                #print data_comp_list
                cursor.executemany(addComponent,data_comp_list)
                db.commit()
                print "commit"
            except Exception as e:
                print e
                db.rollback()
                print "rollback"

        else:
            for component in metaData:
                rptid=rpt
            #print "update"
            data_comp_dict = {
                'metadata': metaData,
                'modified':now.strftime("%Y-%m-%d %H:%M"),
                'report_id':rptid,
            }
            try:
                print data_comp_dict
                cursor.execute(updateComponent,data_comp_dict)
                db.commit()
                print "commit"
            except Exception as e:
                print e
                db.rollback()
                print "rollback"



    return HttpResponse(report_serializer_json)




def card(details):
    print 'details',details    
    
    cardbody=""
    cardinner=""
    bodystart="""<ion-list style="background-color: cornflowerblue;">"""
    bodyend ="""</ion-list>"""
    cardstart ="""<ion-card style="width:100%;height:155px;margin-top: 98px " >"""
    cardend="""</ion-card><button ion-button type="submit" style="margin-left:292px" ion-button (click)="getreport()">View Report</button>"""
    if details:
        for item in details:
            #cardbody +="""<ion-label>"""+item['sl']+"""</ion-label>"""
            card_type = item['wt']
            print 'card_type',card_type

            if card_type =='Select':
                cardinner+=cardbody+typeselect(item)
            if card_type =='Button':
                cardinner+=cardbody+typebutton(item)    
            if card_type =='Checkbox':
                cardinner+=cardbody+typecheckbox(item)
            if card_type =='Date':
                cardinner+=cardbody+typedate(item)
            if card_type =='Email':
                cardinner+=cardbody+typeemail(item)
            if card_type =='Password':
                cardinner+=cardbody+typepassword(item)
            if card_type =='Number':
                cardinner+=cardbody+typenumber(item)
            if card_type =='Text':
                cardinner+=cardbody+typetext(item)
            if card_type =='Time':
                cardinner+=cardbody+typetime(item)
            if card_type =='Textarea':
                cardinner+=cardbody+typetextarea(item)
            if card_type =='Radiobox':
                cardinner+=cardbody+typeradiobox(item)        
            if card_type =='List':
                cardinner+=cardbody+typelist(item) 
    else:
        cardinner=""""""   
          
    cardhtml = cardstart+bodystart+cardinner+bodyend+cardend
    return cardhtml

def typetext(text):
    print "TEXT",text
    cardbody=""
    typetext=""
    if text:
        typetext+=""" <ion-item><ion-label style = "width: 200px">"""+text['cap']+"""</ion-label><ion-input placeholder=""id=\""""+text['idt']+"""\"name=\""""+text['idt']+"""\" ></ion-input></ion-item>"""
        return typetext

def typeselect(select):
    print select
    cardbody=""
    typeselect=""
    if select:
        typeselect+=""" <ion-item><ion-label style = "width: 200px">"""+select['cap']+"""</ion-label><ion-select ><ion-option>"""+select['cap']+"""</ion-option></ion-select></ion-item>"""
        return typeselect

def typedate(date):
    #print select
    cardbody=""
    typedate=""
    if date:
        typedate+=""" <ion-item><ion-label style = "width: 200px">"""+date['cap']+"""</ion-label> <ion-datetime displayFormat="MM/DD/YYYY" id="dateinput"name="dateinput"></ion-datetime></ion-item>"""
        return typedate

def grid(fgrid):
    fgridbody =""
    contentbody=""
    fgridstart = """<ion-scroll scrollX="true" scrollY="true" style="width:100%;height:100%;margin-top: -10px;background-color: lightgray " ><table ><tr >"""
    fgridend =""" </tr ></table></ion-scroll>"""
    if fgrid:
        for grids in fgrid:
            #print grids        
            fgridbody +="""<th style="border:0.2px solid;background-color: lightgray">"""+grids['sl']+"""</th>"""
        gridhtml = fgridstart+fgridbody+fgridend
        return gridhtml

def reportprocess(request,title,pk):    
    query = get_object_or_404(Query,pk = pk)
    print query.id , query.sql
    rpt =Report.objects.get(id=title)
    print rpt.title
    fieldWSQL=[]
    comp_identifiers= []
    element =Projectwiseusersetup.objects.get(userid=request.session['userid'],project_id = request.session['projectid'])
    project_title = element.project_id.title
    projectselect =Projectwiseusersetup.objects.filter(userid=request.session['userid'])
    if element:
        projectid = element.project_id.title
        dbprofile = element.db_profileid_id
        request.session['projectid'] = element.project_id.id      

        #ADMIN DB    
    dbProfileData = Db_profile.objects.get(pk=dbprofile)  
    #print dbProfileData  
    adminDbId = dbProfileData.admindb_id
    #print adminDbId    
    adminDbData = Db_connections_info.objects.get(pk=adminDbId)
        
    host = adminDbData.host
    #print host
    username = adminDbData.username
    #print username
    password = adminDbData.password
    #print password
    database = adminDbData.dbname
    #print database
    db = MySQLdb.connect(host,username,password,database)
    cursor = db.cursor()
    try:
        #queryData = get_object_or_404(Query,pk = pk)
        queryData =Query.objects.filter(id=query.id)       
    except Query.DoesNotExist:
        queryData = None

    print "query", queryData

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
        print query.id ,'query.id'
        cursor.execute("SELECT * FROM rprtmobilesqlmetadata WHERE query_id = %s",[query.id])
        mobileSqlMetaData = cursor.fetchall()
        print "mobilemetadata", mobileSqlMetaData

    #converting tuple to str
        mobileSqlMetaDataStr = []
        for str in mobileSqlMetaData:
            print str,'str'
            mobileSqlMetaDataStr.append(str[0])
        print 'mobileSqlMetaDataStr',mobileSqlMetaDataStr

    except:
        mobileSqlMetaData = ()
        print "mobilemetadata",mobileSqlMetaData

    now = datetime.datetime.now()
    addComponent =   "INSERT INTO rprtmobilesqlmetadata (sqltext,sqltitle,report_sql_type,project_id,report_id,created,modified,query_id) VALUES (%(sqltext)s,%(sqltitle)s,%(report_sql_type)s,%(project_id)s,%(report_id)s,%(created)s,%(modified)s,%(query_id)s)"
    updateComponent =  "UPDATE rprtmobilesqlmetadata SET sqltext=%(sqltext)s, modified=%(modified)s WHERE query_id = %(query_id)s"
    data_comp_list = []
    data_comp_dict = {}
    comp_identifiers= []

    isThere = False
 

    if len(mobileSqlMetaData)== 0:
            for component in queryData:
                print component.sql,component.id
                rptid = rpt
                print rptid
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
            print data_comp_list

            try:                
                cursor.executemany(addComponent,data_comp_list)
                db.commit()
                print "commit"
            except Exception as e:
                print e
                db.rollback()
                print "rollback"

    else:
        print 'Updatenow'
        for component in queryData:
            print 'component.sql',component.sql
            #print "update"
            data_comp_dict = {
                'sqltext': component.sql,
                'modified':now.strftime("%Y-%m-%d %H:%M"),
                'query_id': component.id,
            }
            try:
                print data_comp_dict
                cursor.execute(updateComponent,data_comp_dict)
                db.commit()
                print "commit"
            except Exception as e:
                print e
                db.rollback()
                print "rollback"
        

    return HttpResponseRedirect('/reportview/editReport/%s'%(request.session['reportid']))

@myuser_login_required
def generatepage(request,reportid):
    print "generatingpage"
    reporthtml=""
    completehtml=""    
    paramshtml=""
    gridhtml=""
    cardhtml=""
    ionhtml=""
    filePath = settings.MEDIA_ROOT
    projectid = request.session['projectid']
    project = Project.objects.get(pk = projectid)
    ptitle = project.title
    #print ptitle,'ptitle'
    view = Report.objects.get(id = reportid)
    viewid = view.id
    print viewid
    view.createpage = True
    view.save()
    reportgroup = Report.objects.filter(id = reportid)
    reportgroup_serializer = ReportviewSerializer(instance=reportgroup,many=True)
    reportserialzier =reportgroup_serializer.data
    if reportserialzier.__len__() > 0:
        report_serializer_json = json.dumps(reportgroup_serializer.data[0])
        #print "report_serializer_json",report_serializer_json

    fileName = reportgroup_serializer.data[0]['tit'].lower().replace(" ","")
    print "fileName",fileName
    print "ptitle",ptitle
    projectid = reportgroup_serializer.data[0]['pid']
    formhtml = reportgroup_serializer.data[0]
    home = Homepage.objects.filter(project_id_id = projectid)
    print "home",home[0].menutype
    if home[0].menutype == "sidemenu":
        headerhtml="""<ion-header><ion-navbar color="primary"><ion-buttons """+home[0].sidemenu+"""><button ion-button menuToggle><ion-icon name="menu"></ion-icon></button></ion-buttons><ion-title>"""+reportgroup_serializer.data[0]['tit']+"""</ion-title></ion-navbar></ion-header><ion-content><form id="myForm" name="myForm">"""
    else:
        headerhtml="""<ion-header><ion-navbar color="primary"><ion-title>"""+reportgroup_serializer.data[0]['tit']+"""</ion-title></ion-navbar></ion-header><ion-content><form id="myForm" name="myForm">"""

    footerhtml="""</form></ion-content>"""    
    
    #print jsonMeta,"jsonMeta"

    data =open(filePath+"static/ionicmeta/"+ptitle+"/"+fileName+"/"+fileName+".json").read()
    jsonData = json.loads(data)    
    print type(jsonData)
    reportparam= jsonData.get('reportparamfield_meta')
    #print "paramhtml",reportparam
    paramhtml=  card(reportparam)
    ionhtml = paramhtml  
    reportfld =jsonData.get('reportfield_meta')
    #print jsonData[0].get('rh1')   
    repdatahtml =  grid(reportfld)
        #return HttpResponse(reportparam)
    completehtml = repdatahtml
    reporthtml = headerhtml+ionhtml+completehtml+footerhtml
    if not os.path.exists(filePath+"static/ionicmeta/"+ptitle+"/"+fileName):
        os.makedirs(filePath+"static/ionicmeta/"+ptitle+"/"+fileName)

    Html_file= open(filePath+"static/ionicmeta/"+ptitle+"/"+fileName+"/"+fileName+".html","w")
    Html_file.write(reporthtml)
    Html_file.close()
    
    return HttpResponseRedirect('/reportview/repoviewdetails/')   

def ionicmetaJson(repojson,fileName,ptitle):
    filePath = settings.MEDIA_ROOT
    if not os.path.exists(filePath+"static/ionicmeta/"+ptitle+"/"+fileName):
        os.makedirs(filePath+"static/ionicmeta/"+ptitle+"/"+fileName)

    json_file= open(filePath+"static/ionicmeta/"+ptitle+"/"+fileName+"/"+fileName+".json","w")
    json_file.write(repojson)
    json_file.close()
# def formReport(request):
#     repoid = request.session['reportid']
#     print repoid    
#     completehtml=""    
#     paramshtml=""
#     gridhtml=""
#     cardhtml=""
#     ionhtml=""
#     data =open("static/json/data/data.json").read()
#     jsonData = json.loads(data)    
#     print type(jsonData)
#     reportparam= jsonData.get('reportparamfield_meta')
#     #print "paramhtml",reportparam
#     paramhtml=  card(reportparam)
#     ionhtml = paramhtml  
#     reportfld =jsonData.get('reportfield_meta')
#     #print jsonData[0].get('rh1')   
#     repdatahtml =  grid(reportfld)
#         #return HttpResponse(reportparam)
#     completehtml = repdatahtml
#     headerhtml="""<ion-header style="background-color: #8c969254"><ion-navbar><ion-title style="margin-left: 33%;background-color: aqua;" >"""+jsonData['rh1']+""" <p class="subtitle" style="background-color: aqua;">"""+jsonData['rh2']+""" </p> </ion-title></ion-navbar></ion-header>"""
#     footerhtml="""<ion-footer style="background-color: #8c969254"><ion-navbar><ion-title style="margin-left: 33%;" >"""+jsonData['rf1']+""" <p class="subtitle">"""+jsonData['rf2']+""" </p> </ion-title></ion-navbar></ion-footer>"""
#     repohtml = headerhtml+ionhtml+completehtml+footerhtml
#     Html_file= open("ionichtml/repodata.html","w")
#     Html_file.write(repohtml)
#     Html_file.close()
#     return HttpResponse(repohtml)