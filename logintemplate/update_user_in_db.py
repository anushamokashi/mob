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
import pandas
from sqlalchemy import schema
from django.conf import settings
import os
import requests


from .models  import UserList,GeneralInfo,Login,EditedUsersList,EditedInfo
from .forms import LoginForm,GeneralInfoForm,UserListForm
from authentication.models import userprofile
from project.models import Project, Projectwiseusersetup,IonicServices
from schema.models import Db_connections_info, Db_profile
from rolesetup.models import Role



errors =[]

def update_user_and_generalinfo(request,userid,project_id,db_type):
    resturl = ""
    errors=[]

    try:
        resturl = IonicServices.objects.get(project_id_id = project_id)
    except Exception as e:
        resturl = None
    print resturl
    

    try:
        engine = get_engine(request,userid,project_id,db_type)
        print "ENGINE ", engine
       
    except Exception as e:
        errors.append(e)
        return errors

    if resturl == None:
        errors.append(engine.name.upper()+": Please complete Ionic Service setup in admin. Then creat users.")
        return errors
    
    meta = schema.MetaData(engine)

    update_users(meta,engine,project_id,db_type)
    update_general_info(meta,engine,project_id,db_type)

    return errors

    
    


def get_engine(request,userid,project_id,db_type):
    
    try:
        element =Projectwiseusersetup.objects.get(userid=userid,project_id = project_id)              
        dbprofile = element.db_profileid_id
        dbProfileData = Db_profile.objects.get(pk=dbprofile)
        projectObj = Project.objects.get(id=project_id)

        filePath = settings.MEDIA_ROOT

        if db_type == "server":
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
        
        if db_type == "client":
            #Get CLIENT DB details
            clientDbId = dbProfileData.clientdb_id
            clientDbData = Db_connections_info.objects.get(pk=clientDbId)
            
            vendor = clientDbData.vendor

       
          
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

def update_users(meta,engine,project_id,db_type):
    
    table = Table('muser', meta,
                Column('muserid', Integer, nullable=False, primary_key=True, autoincrement=True),
                Column('first_name', String(60), nullable=False),
                Column('last_name', String(60), nullable=True),
                Column('mobile_number', BIGINT, nullable=False),
                Column('email_id', String(60), key='email',nullable=False),
                Column('pwd', String(150), nullable=False),
                Column('confirm_password', String(150), nullable=False),
                Column('role', String(50), nullable=True),
                Column('onesignalplayer_id', String(250), nullable=True),
                Column('is_active', Boolean, default=True),
                Column('imei_no', BIGINT, nullable=True)
            )
    table.create(engine,checkfirst=True)

    print "**Table**"
    print table

    print "UPDATE USER DETAILS"
    print "-------------------"

    

    #Deleting users
    try:
        delete_status_users = UserList.objects.filter(db_status='deleted',project_id_id=project_id)
    except UserList.DoesNotExist:
        delete_status_users = None

    if delete_status_users:
        print "***DELETING USERS***"
        
        try:
            for user in delete_status_users:
                print user.email_id
                print "------"
                d = table.delete(table.c.email == user.email_id)
                d.execute()
                
                if db_type == "client":
                    user.delete()
        except Exception as e:
            errors.append(e)
            print e
    else:
        print "No USERS TO DELETE"
        
    
    # Adding NEW users
    try:
        new_users = UserList.objects.filter(db_status='new',project_id_id=project_id)
    except UserList.DoesNotExist:
        new_users = None

    if new_users:
        print "***ADDING USERS***"
        
        try:
           for user in new_users:
                print user
                print "------"
                
                url = 'http://192.168.125.75:32923/mservice/mobileserviceapi/encryptStr'
                data = {"data" : user.password}
                response = requests.post(url, params=data)
                
                roleId = user.role_id
                roleObj = Role.objects.get(id=roleId)
                
                if db_type == "server":
                    ins = table.insert().values(first_name=user.first_name, last_name=user.last_name, mobile_number=user.mobile_number, email=user.email_id, pwd=response.text, confirm_password=response.text, is_active=user.is_active, role=roleObj.rolename,onesignalplayer_id="TEST")
                if db_type == "client":
                    ins = table.insert().values(first_name=user.first_name, last_name=user.last_name, mobile_number=user.mobile_number, email=user.email_id, pwd=user.password, confirm_password=user.password, is_active=user.is_active, role=roleObj.rolename,onesignalplayer_id="TEST")
                
                ins.execute()
                
                if db_type == "client":
                    user.db_status='updated'
                    user.save()
        except Exception as e:
            errors.append(e)
            print e
    else:
        print "NO USERS TO ADD"

    
    
    # Edit users
    try:
        edited_users = EditedUsersList.objects.filter(pid=project_id)
    except EditedUsersList.DoesNotExist:
        edited_users = None

    if edited_users:
        print "***EDIT USERS***"
        print edited_users
        
        try:
            for user in edited_users:
                print user.user_old_email
                print "------"
                
                try:
                    user_obj = UserList.objects.get(id=user.user_id)
                except UserList.DoesNotExist:
                    user_obj = None
                
                if user_obj:

                    url = 'http://192.168.125.75:32923/mservice/mobileserviceapi/encryptStr'
                    data = {"data" : user_obj.password}
                    response = requests.post(url, params=data)

                    roleId = user_obj.role_id
                    roleObj = Role.objects.get(id=roleId)
                    
                    if db_type == "server":
                         updateColumn = table.update().where(table.c.email==user.user_old_email).values(first_name=user_obj.first_name, last_name=user_obj.last_name, mobile_number=user_obj.mobile_number, email=user_obj.email_id, pwd=response.text, confirm_password=response.text, is_active=user_obj.is_active, role=roleObj.rolename,onesignalplayer_id="TEST")
                    if db_type == "client":
                         updateColumn = table.update().where(table.c.email==user.user_old_email).values(first_name=user_obj.first_name, last_name=user_obj.last_name, mobile_number=user_obj.mobile_number, email=user_obj.email_id, pwd=user_obj.password, confirm_password=user_obj.password, is_active=user_obj.is_active, role=roleObj.rolename,onesignalplayer_id="TEST")

                   
                    updateColumn.execute()
                    
                    if db_type == "client":
                        user_obj.db_status = 'updated'
                        user_obj.save()
                        user.delete()
                else:
                    if db_type == "client":
                        user.delete()

        except Exception as e:
            errors.append(e)
            print e
    else:
        print "NO USERS TO Edit"

def update_general_info(meta,engine,project_id,db_type):

    info_table = Table('control', meta,
        Column('controlid', Integer, nullable=False, primary_key=True, autoincrement=True),
        Column('key', String(60), nullable=False),
        Column('value', String(60), nullable=False),
    )
    info_table.create(engine,checkfirst=True)

    if db_type == "server":
        notification_status_table = Table('notification_status', meta,
            Column('notification_statusid', Integer, nullable=False, primary_key=True, autoincrement=True),
            Column('role', String(30), nullable=True),
            Column('user_name', String(50), nullable=True),
            Column('basicid', String(100), nullable=True),
            Column('message', String(255), nullable=True),
            Column('valid_from', Date, nullable=True),
            Column('valid_to', Date, nullable=True),
            Column('json', String(20000), nullable=False),
        )
        notification_status_table.create(engine,checkfirst=True)

    print "**Table**"
    print info_table

    print "UPDATE INFO"
    print "-------------------"

    

    #Deleting users
    try:
        delete_status_info = GeneralInfo.objects.filter(db_status='deleted',project_id_id=project_id)
    except GeneralInfo.DoesNotExist:
        delete_status_info = None

    if delete_status_info:
        print "***DELETING INFO***"
        
        try:
            for info in delete_status_info:
                print info.key
                print "------"
                d = info_table.delete(info_table.c.key == info.key)
                d.execute()
                
                if db_type == "client":
                    info.delete()
        except Exception as e:
            errors.append(e)
            print e
    else:
        print "No INFO TO DELETE"
        
    
    # Adding NEW users
    try:
        new_info = GeneralInfo.objects.filter(db_status='new',project_id_id=project_id)
    except GeneralInfo.DoesNotExist:
        new_info = None

    if new_info:
        print "***ADDING INFO***"
        
        try:
           for info in new_info:
                print info.key
                print "------"
                ins = info_table.insert().values(key=info.key, value=info.value)
                ins.execute()
                
                if db_type == "client":
                    info.db_status='updated'
                    info.save()
        except Exception as e:
            errors.append(e)
            print e
    else:
        print "NO INFO TO ADD"

    
    
    # Edit users
    try:
        edited_info = EditedInfo.objects.filter(pid=project_id)
    except EditedInfo.DoesNotExist:
        edited_info = None

    if edited_info:
        print "***EDIT INFO***"
        print edited_info
        
        try:
            for info in edited_info:
                print info.old_key
                print "------"
                
                try:
                    gen_info = GeneralInfo.objects.get(id=info.key_id)
                except GeneralInfo.DoesNotExist:
                    gen_info = None
                
                if gen_info:
                    updateColumn = info_table.update().where(info_table.c.key==info.old_key).values(key=gen_info.key, value=gen_info.value)
                    updateColumn.execute()
                    
                    if db_type == "client":
                        gen_info.db_status = 'updated'
                        gen_info.save()
                        info.delete()
                else:
                    if db_type == "client":
                        info.delete()
        except Exception as e:
            errors.append(e)
            print e
    else:
        print "NO INFO TO Edit"




