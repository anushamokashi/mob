# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import MySQLdb
import json

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.db.models import Q

from project.models import Project, Projectwiseusersetup
from authentication.models import userprofile
from schema.models import Db_connections_info, Db_profile
from transactionview.models import Component, Transactionview, FireSql
from transaction.models import Transaction
errors =[]
# Create your views here.
def dbconnection(request,txviewid):
    errors = []
    viewid = txviewid
    userid = request.session['userid']
    pid = request.session['projectid']
    
    viewObj = Transactionview.objects.get(id = viewid)
    txnObj = Transaction.objects.get(id= viewObj.transactionid_id)
    element =Projectwiseusersetup.objects.get(userid=userid,project_id = pid)
    projectObj = Project.objects.get(id = pid)
    
    data_comp_list = []
    data_comp_dict = {}
    comp_list = []
    comp_identifiers = []
    mobileSqlMetaDataStr = []
    isThere = False 
    
    #Query
    now = datetime.datetime.now()
    addComponent =  "INSERT INTO txmobilesqlmetadata (sqltext,tx_sql_type,component_id,project_id,transaction_id,tx_view_id,created,modified) VALUES (%(sqltext)s,%(tx_sql_type)s,%(component_id)s,%(project_id)s,%(transaction_id)s,%(tx_view_id)s,%(created)s,%(modified)s)"
    updateComponent =  "UPDATE txmobilesqlmetadata SET sqltext=%(sqltext)s, modified=%(modified)s WHERE component_id = %(component_id)s AND tx_view_id = %(tx_view_id)s"
    

    #META DB    
    dbProfileData = Db_profile.objects.get(pk=element.db_profileid_id)
    appDbData = Db_connections_info.objects.get(pk=dbProfileData.appdb_id)
        
    host = appDbData.host
    username = appDbData.username
    password = appDbData.password
    database = appDbData.dbname 
    
    #Making connection
    db = MySQLdb.connect(host,username,password,database)
    cursor = db.cursor()

    #Components 
    try:
        componentData = Component.objects.filter(transactionviewid_id = viewid).exclude(sql__isnull=True).exclude(sql="")
    except Component.DoesNotExist:
        componentData = None
    
    print "******"
    print componentData
    
    #FireSQL
    try:
        firesqlObjs = FireSql.objects.filter(transactionview_id = viewid)
    except FireSql.DoesNotExist:
        firesqlObjs = None

    print "******"
    print firesqlObjs
    

    #Retriving identifiers
    if componentData:        
        for item in componentData:
            sqlString = item.sql
            sqlDict =  json.loads(sqlString)           
            if sqlDict['sqlDbType'] == "server":
                id_sql_dict = {
                    'id' : item.identifiers.encode('utf8'),
                    'sql' : sqlDict['Sql']
                }
                comp_list.append(id_sql_dict)
                comp_identifiers.append(item.identifiers.encode('utf8'))
    
    if firesqlObjs:
        for item in firesqlObjs:
            id_sql_dict = {
                'id' : item.slug.encode('utf8'),
                'sql' : item.sql
            }
            comp_list.append(id_sql_dict)
            comp_identifiers.append(item.slug.encode('utf8'))

    print "******"
    print comp_list
    print "*****"
    print comp_identifiers

    #Meta data
    try:
        cursor.execute("SELECT * FROM txmobilesqlmetadata WHERE tx_view_id=\""+viewObj.identifiers+"\"")
        mobileSqlMetaData = cursor.fetchall()
        
        #converting tuple to str
        for str in mobileSqlMetaData:
            mobileSqlMetaDataStr.append(str[3])
        
        print "**********"
        print "mobileSqlMetaDataStr",mobileSqlMetaDataStr

    except Exception as e:
        mobileSqlMetaData = ()
        print "mobilemetadata",mobileSqlMetaData
        errors.append(e)
        db.close()
        cursor.close()
        return errors

    

    if len(mobileSqlMetaData)==0:
        for component in comp_list:
            print "Insert All"
            print component  
            
            data_comp_dict = {
                'sqltext': component['sql'],
                'tx_sql_type': "tx-field",
                'component_id': component['id'] ,
                'project_id':projectObj.slug,
                'transaction_id':txnObj.txname,
                'tx_view_id':viewObj.identifiers,
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
            db.close()
            cursor.close()
            errors.append(e)
            return errors

    else:
        #Delete
        for tupleItem in mobileSqlMetaData:
            if not tupleItem[3] in comp_identifiers: 
                print tupleItem[3]
                print comp_identifiers
                print "delete"
                print "DELETE FROM txmobilesqlmetadata WHERE id = '%s'" % (tupleItem[0],)
                delComponent = "DELETE FROM txmobilesqlmetadata WHERE id = '%s'" % (tupleItem[0],)
                cursor.execute(delComponent)
                db.commit() 
                print "commit"

        #Update And Insert
        for component in comp_list:
           
            if component['id'] in mobileSqlMetaDataStr:
                print component['id']
                print "update" 
                data_comp_dict = {
                    'sqltext': component['sql'],
                    'modified': now.strftime("%Y-%m-%d %H:%M"),
                    'component_id': component['id'],
                    'tx_view_id':viewObj.identifiers,
                }
            
                try:
                    cursor.execute(updateComponent,data_comp_dict)
                    db.commit()
                    print "commit" 
                except Exception as e:
                    print e
                    db.rollback()
                    print "rollback"
                    db.close()
                    cursor.close()
                    errors.append(e)
                    return errors

            else:
                print component['id']
                print "insertUU"
               
                data_comp_dict = {
                    'sqltext': component['sql'],
                    'tx_sql_type': "tx-field",
                    'component_id': component['id'],
                    'project_id':projectObj.slug,
                    'transaction_id':txnObj.txname,
                    'tx_view_id':viewObj.identifiers,
                    'created':now.strftime("%Y-%m-%d %H:%M"),
                    'modified':now.strftime("%Y-%m-%d %H:%M"),
                }

                try:
                    cursor.execute(addComponent,data_comp_dict)
                    db.commit()
                    print "commit"
                except Exception as e:
                    print e
                    db.rollback()
                    print "rollback"
                    errors.append(e)
                    db.close()
                    cursor.close()
                    return errors
                  

    db.close()
    cursor.close()
    
    return errors



