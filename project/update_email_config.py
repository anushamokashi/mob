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
from .models  import EmailConfiguration
from .forms import EmailConfigurationForm
from authentication.models import userprofile
from project.models import Project, Projectwiseusersetup
from schema.models import Db_connections_info, Db_profile

filePath = settings.MEDIA_ROOT

errors =[]

def update_email_setup(request,userid,project_id):
    projectObj = Project.objects.get(id=project_id)
    
    try:
        engine = get_engine(request,userid,project_id)
        print "ENGINE ", engine
       
    except Exception as e:
        errors.append(e)
        return errors

   
    meta = schema.MetaData(engine)

    mail_config_table = Table('mailconfig', meta,
                Column('id', Integer, nullable=False, primary_key=True, autoincrement=True),
                Column('project_slug', String(100), nullable=False),
                Column('port', Integer, nullable=True),
                Column('server', String(255), nullable=True),
                Column('is_authentication_required', String(50),nullable=True),
                Column('protocol', String(100), nullable=True),
                Column('support_tls', String(50), nullable=True),
                Column('domain', String(50), nullable=True),
                Column('default_email', String(50), nullable=True)
            )
    mail_config_table.create(engine,checkfirst=True)
    
    system_mailid_config = Table('systemmailidconfig', meta,
                Column('id', Integer, nullable=False, primary_key=True, autoincrement=True),
                Column('smtp_config_id', Integer, nullable=False),
                Column('title', String(100), nullable=True),
                Column('username', String(100), nullable=True),
                Column('email', String(100),nullable=True),
                Column('password', String(100), nullable=True),
                Column('project_id', String(100), nullable=True),
            )
    system_mailid_config.create(engine,checkfirst=True)   

    try:
        emailserverObj = EmailConfiguration.objects.get(project_id_id=project_id)
    except EmailConfiguration.DoesNotExist:
        emailserverObj = None 
    
    if emailserverObj:
        if emailserverObj.db_status == "new":
            add_emailconfig(meta,engine,project_id,mail_config_table,system_mailid_config,projectObj,emailserverObj)
        if emailserverObj.db_status == "edited" or emailserverObj.db_status == "deleted":
            update_emailconfig(meta,engine,project_id,mail_config_table,system_mailid_config,projectObj,emailserverObj)
    
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

def add_emailconfig(meta,engine,project_id,mail_config_table,system_mailid_config,projectObj,emailserverObj):
    
    #Adding NEW
    
    try:
        ins = mail_config_table.insert().values(project_slug=projectObj.slug, port=emailserverObj.port, server=emailserverObj.server, is_authentication_required=emailserverObj.is_aunthentication_req, protocol=emailserverObj.protocol,support_tls=emailserverObj.support_tls, domain=emailserverObj.Domain, default_email=emailserverObj.default_email_id)
        res = ins.execute() 
        print "+++++++++++++++++++++++++++++=="
        print "RESULT"
        print res
        
        Session = sessionmaker()
        Session.configure(bind=engine)
        session1 = Session()
        
        query = session1.query(mail_config_table).filter(mail_config_table.c.project_slug == projectObj.slug)
        row = query.first()
        print row.id

        insAttr = system_mailid_config.insert().values(smtp_config_id = row.id, title = emailserverObj.default_email_id, username=emailserverObj.email_id, email=emailserverObj.email_id,password=emailserverObj.pwd, project_id=projectObj.slug)
        insAttr.execute()

        emailserverObj.db_status='updated'
        emailserverObj.save() 


    except Exception as e:
        errors.append(e)
        print e

def update_emailconfig(meta,engine,project_id,mail_config_table,system_mailid_config,projectObj,emailserverObj):
    
    Session = sessionmaker()
    Session.configure(bind=engine)
    session2 = Session()
    
    query = session2.query(mail_config_table).filter(mail_config_table.c.project_slug == projectObj.slug)
    row = query.first()

    print "DELETE SMS SETUP"
    d = system_mailid_config.delete(system_mailid_config.c.smtp_config_id == row.id)
    d.execute()

    ddd = mail_config_table.delete(mail_config_table.c.id ==  row.id)
    ddd.execute()


    if emailserverObj.db_status == "edited":
        print "EDITED"
        add_emailconfig(meta,engine,project_id,mail_config_table,system_mailid_config,projectObj,emailserverObj)
        emailserverObj.db_dbstatus = "updated"
        emailserverObj.save()
    
    elif emailserverObj.db_status == "deleted":
        emailserverObj.delete()
