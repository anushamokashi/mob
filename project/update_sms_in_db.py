from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse,HttpResponseBadRequest
from django.core import serializers
from django.shortcuts import render
from django.db import transaction as db_trans
import json
import logging

import sqlalchemy
from sqlalchemy import *
from sqlalchemy import schema, types,UniqueConstraint
from sqlalchemy import create_engine, dialects, event, DDL
from sqlalchemy import Table, Column, MetaData, ForeignKey

from sqlalchemy.types import String, \
        Integer, \
        Boolean, \
        Date, \
        DateTime, \
        Float, \
        Numeric, \
        BigInteger, \
        Text, \
        BLOB, \
        Unicode, \
        UnicodeText, \
        SmallInteger, \
        Binary,\
        TIMESTAMP,\
        Interval,\
        TypeEngine

from sqlalchemy.dialects import mysql,oracle,postgresql
from sqlalchemy.schema import SchemaVisitor
from sqlalchemy.engine import reflection
from sqlalchemy.sql.compiler import DDLCompiler
from aldjemy.core import get_tables
from sqlalchemy.orm import sessionmaker
from sqlalchemy import schema
from django.conf import settings
import os
import requests

from django.db.models import Q
from smssetup.models  import SMSServer,SMSAttributes
from smssetup.forms import SMSServerForm,SMSAttributesForm
from authentication.models import userprofile
from project.models import Project, Projectwiseusersetup
from schema.models import Db_connections_info, Db_profile
filePath = settings.MEDIA_ROOT

errors =[]

def update_sms_setup(request,userid,project_id):
    projectObj = Project.objects.get(id=project_id)
    
    try:
        engine = get_engine(request,userid,project_id)
        print "ENGINE ", engine
       
    except Exception as e:
        errors.append(e)
        return errors

   
    meta = schema.MetaData(engine)

    sms_config_table = Table('smsconfig', meta,
                Column('id', Integer, nullable=False, primary_key=True, autoincrement=True),
                Column('project_slug', String(60), nullable=False),
                Column('port', Integer, nullable=True),
                Column('server', String(255), nullable=True),
                Column('sms_provider_url', String(255),nullable=True),
                Column('mobile_attr', String(50), nullable=True),
                Column('message_attr', String(255), nullable=True),
                Column('default_sender_id', String(100), nullable=True),
                Column('useproxy', String(20), nullable=True)
            )
    sms_config_table.create(engine,checkfirst=True)
    
    sms_attr_table = Table('smsattributes', meta,
                Column('id', Integer, nullable=False, primary_key=True, autoincrement=True),
                Column('sms_config_id', Integer, nullable=False),
                Column('key_attr', String(100), nullable=True),
                Column('value_attr', String(100), nullable=True),
                Column('order_attr', Integer,nullable=True),
                Column('project_id', String(100), nullable=True),
            )
    sms_attr_table.create(engine,checkfirst=True)

    sms_senderid_table = Table('smssenderidconfig', meta,
                Column('id', Integer, nullable=False, primary_key=True, autoincrement=True),
                Column('sms_config_id', Integer, nullable=False),
                Column('senderid', String(100), nullable=True),
                Column('project_id', String(100), nullable=True),
            )
    sms_senderid_table.create(engine,checkfirst=True)   

    #Create Table
    emessage_send_status = Table('emessage_send_status', meta,
                Column('emessageid', Integer, nullable=True),
                Column('emessageto', Integer, nullable=True),
                Column('emessage_date_time', String(100), nullable=True),
                Column('emessage_project_id', String(100), nullable=True),
                Column('emessage_status', String(100), nullable=True),
                Column('emessage_status_cause', String(100), nullable=True),
                Column('transid', String(100), nullable=True),
                Column('transcause', String(100), nullable=True),
                Column('username', String(100), nullable=True),
            )
    emessage_send_status.create(engine,checkfirst=True) 

   

    try:
        smsserverObj = SMSServer.objects.get(projectid_id=project_id)
    except SMSServer.DoesNotExist:
        smsserverObj = None 
    
    if smsserverObj:
        if smsserverObj.db_status == "new":
            add_smsconfig(meta,engine,project_id,sms_config_table,sms_attr_table,sms_senderid_table,projectObj,smsserverObj)
        if smsserverObj.db_status == "edited" or smsserverObj.db_status == "deleted":
            update_smsconfig(meta,engine,project_id,sms_config_table,sms_attr_table,sms_senderid_table,projectObj,smsserverObj)
    
    #update_smsconfig(meta,engine,project_id,sms_config_table,sms_attr_table,sms_senderid_table,projectObj)

    return errors

    
def get_engine(request,userid,project_id):
    
    try:
        element =Projectwiseusersetup.objects.get(userid=userid,project_id = project_id)              
        dbprofile = element.db_profileid_id
        dbProfileData = Db_profile.objects.get(pk=dbprofile)
        projectObj = Project.objects.get(id=project_id)

        #Get APP DB details
        appDbId = dbProfileData.appdb_id
        appDbData = Db_connections_info.objects.get(pk=appDbId)
            
        dbTitle = appDbData.title
        host = appDbData.host
        port = appDbData.port
        username = appDbData.username
        password = appDbData.password
        database = appDbData.dbname        
        vendor = appDbData.vendor
        sid = appDbData.sid
       
          
        print "VENDOR", vendor
            
        if vendor == 'oracle':
        
            if database:
                database_url = "%s:%s@%s:%s/?service_name=%s" % (
                    username, password, host, port, database)
    
            else:
                database_url = "%s:%s@%s:%s/?service_name=%s" % (
                    username, password, host, port, sid)  
    
            engine = create_engine('oracle+cx_oracle://' +
                                database_url, echo=True)
    
        elif vendor == 'postgres':
            database_url = "%s:%s@%s:%s/%s" % (
                
                username, password, host, port, database)
    
            engine = create_engine("postgresql://" + database_url, echo=True)
    
        
        elif vendor == 'mysql':
            database_url = "%s:%s@%s:%s/%s" % (
                
                username, password, host, port, database)
            
            engine = create_engine("mysql://"+ database_url, echo=True)
    
        
        elif vendor == 'sqlite':

            if not os.path.exists(filePath+'static/ionicmeta/'+projectObj.slug+'/db/'):
                os.makedirs(filePath+'static/ionicmeta/'+projectObj.slug+'/db/')
            
            engine = create_engine('sqlite:///'+filePath+'static/ionicmeta/'+projectObj.slug+'/db/'+projectObj.slug+'.db', echo=True)

    
        
        else:

            if not os.path.exists(filePath+'static/ionicmeta/'+projectObj.slug+'/db/'):
                os.makedirs(filePath+'static/ionicmeta/'+projectObj.slug+'/db/')
            
            engine = create_engine('sqlite:///'+filePath+'static/ionicmeta/'+projectObj.slug+'/db/test.db', echo=True)
    
    except Exception as e:
        print e
        errors.append(e)
        engine= None
        
    return engine

def add_smsconfig(meta,engine,project_id,sms_config_table,sms_attr_table,sms_senderid_table,projectObj,smsserverObj):
    
    #Adding NEW
    
    try:
        print "***ADDING NEW SMS SERVER***"
        ins = sms_config_table.insert().values(project_slug=projectObj.slug, port=smsserverObj.port, server=smsserverObj.server, sms_provider_url=smsserverObj.url, mobile_attr='contacts',message_attr='msg', default_sender_id='senderid', useproxy=smsserverObj.use_proxy)
        res = ins.execute() 
        print "+++++++++++++++++++++++++++++=="
        print "RESULT"
        print res
        
        smsserverObj.db_status='updated'
        smsserverObj.save() 
        
        Session = sessionmaker()
        Session.configure(bind=engine)
        session1 = Session()
        
        query = session1.query(sms_config_table).filter(sms_config_table.c.project_slug == projectObj.slug)
        row = query.first()
        print row.id

        print "***ADDING NEW SMSATTR***"
        new_smsattrs = SMSAttributes.objects.filter(smsserver_id=smsserverObj.id)

        print new_smsattrs
        if new_smsattrs:
            for attr in new_smsattrs:
                print attr
                try:
                    smsattrObj = SMSAttributes.objects.get(id=attr.id)
                except SMSAttributes.DoesNotExist:
                    smsattrObj = None

                insAttr = sms_attr_table.insert().values(sms_config_id = row.id, key_attr = smsattrObj.key, value_attr=smsattrObj.value, order_attr=smsattrObj.do, project_id=projectObj.slug)
                insAttr.execute()
        
        print "***ADDING NEW SMS SENDERID TABLE***"
        
        insSenderId = sms_senderid_table.insert().values(sms_config_id = row.id, senderid = 'senderid', project_id=projectObj.slug)
        insSenderId.execute()


    except Exception as e:
        errors.append(e)
        print e

def update_smsconfig(meta,engine,project_id,sms_config_table,sms_attr_table,sms_senderid_table,projectObj,smsserverObj):
    
    Session = sessionmaker()
    Session.configure(bind=engine)
    session2 = Session()
    
    query = session2.query(sms_config_table).filter(sms_config_table.c.project_slug == projectObj.slug)
    row = query.first()

    print "DELETE SMS SETUP"
    d = sms_senderid_table.delete(sms_senderid_table.c.sms_config_id == row.id)
    d.execute()

    dd = sms_attr_table.delete(sms_attr_table.c.sms_config_id == row.id)
    dd.execute()

    ddd = sms_config_table.delete(sms_config_table.c.id ==  row.id)
    ddd.execute()


    if smsserverObj.db_status == "edited":
        print "EDITED"
        add_smsconfig(meta,engine,project_id,sms_config_table,sms_attr_table,sms_senderid_table,projectObj,smsserverObj)
        smsserverObj.db_dbstatus = "updated"
        smsserverObj.save()
    
    elif smsserverObj.db_status == "deleted":
        smsserverObj.delete()
