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


from .models  import EditedTableMap,SyncTableDetails,SyncColumnDetails,EditedColumnMap
from .forms import SyncTableDetailsForm,SyncColumnDetailsForm
from authentication.models import userprofile
from project.models import Project, Projectwiseusersetup
from schema.models import Db_connections_info, Db_profile


errors =[]

def update_syncmaster_table(request,userid,project_id,db_type):
    errors = []
    try:
        engine = get_engine(request,userid,project_id,db_type)
        print "ENGINE ", engine
       
    except Exception as e:
        errors.append(e)
        return errors
    meta = schema.MetaData(engine)

    #--------------------------------------------
    # CREATE TABELS
    #--------------------------------------------

    table = Table('mastermap', meta,
        Column('moduleid', Integer, nullable=False, primary_key=True, autoincrement=True),
        Column('stname', String(60), nullable=False),
        Column('ttname', String(60), nullable=False),
        Column('url', String(60), nullable=True),
        Column('dependson', String(60), nullable=True),
        Column('orderno', Integer, nullable=True),
        Column('wherecon', String(60), nullable=True),
        Column('project_slug', String(60), nullable=False)
    )
    table.create(engine,checkfirst=True)

    columnmap_table = Table('mastermapdetail', meta,
        Column('mastermapdetailid', Integer, nullable=False, primary_key=True, autoincrement=True),
        Column('moduleid', Integer, ForeignKey("mastermap.moduleid"), nullable=False),
        Column('sfname', String(60), nullable=False),
        Column('tfname', String(60), nullable=False),
        Column('shortid', Integer, nullable=True),
        Column('project_slug', String(60), nullable=False)
    )
    columnmap_table.create(engine,checkfirst=True)

    update_tablemap(meta,engine,project_id,table,columnmap_table,db_type)
    update_columnmap(meta,engine,project_id,table,columnmap_table,db_type)

    return errors

    
    


def get_engine(request,userid,project_id,db_type):
    
    try:
        element =Projectwiseusersetup.objects.get(userid=userid,project_id = project_id)              
        dbprofile = element.db_profileid_id
        dbProfileData = Db_profile.objects.get(pk=dbprofile)
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

        elif db_type == "client":
            #Get CLIENT DB details

            clientDbId = dbProfileData.clientdb_id
            clientDbData = Db_connections_info.objects.get(pk=clientDbId)
            
            vendor = clientDbData.vendor



        projectObj = Project.objects.get(id=project_id)

          
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
            
            if not os.path.exists(filePath+'static/ionicmeta/'+projectObj.title+'/db/'):
                os.makedirs(filePath+'static/ionicmeta/'+projectObj.title+'/db/')
            
            engine = create_engine('sqlite:///'+filePath+'static/ionicmeta/'+projectObj.title+'/db/'+projectObj.title+'.db', echo=True)

    
        
        else:

            if not os.path.exists(filePath+'static/ionicmeta/'+projectObj.title+'/db/'):
                os.makedirs(filePath+'static/ionicmeta/'+projectObj.title+'/db/')
            
            engine = create_engine('sqlite:///'+filePath+'static/ionicmeta/'+projectObj.title+'/db/test.db', echo=True)
    
    except Exception as e:
        print e
        errors.append(e)
        engine= None
        
    return engine

def update_tablemap(meta,engine,project_id,table,columnmap_table,db_type):
    projectObj = Project.objects.get(id=project_id)
    

    print "**Table**"
    print table

    print "UPDATE TABLE MAP"
    print "-------------------"

    

    #--------------------------------------------
    # DELETE TABLE MAP 
    #--------------------------------------------

    try:
        delete_status_tablemap = SyncTableDetails.objects.filter(db_status='deleted',projectid_id=project_id)
    except UserList.DoesNotExist:
        delete_status_tablemap = None

    if delete_status_tablemap:
        print "***DELETING TABLE MAP***"
        
        try:
            for map in delete_status_tablemap:
                print map.sourcetable
                print "------"

                #------------------------------------------------------------
                # DELETE COLUMN MAP FOR CORESPONDING TABLE MAP BEFORE DELETE
                #------------------------------------------------------------
                
               
           

                ddd = columnmap_table.delete().where(columnmap_table.c.moduleid==select([table.c.moduleid]).where(and_(table.c.stname == map.sourcetable,table.c.ttname == map.targettable,table.c.project_slug == projectObj.slug)).as_scalar())
                ddd.execute()

                # users.delete().where(users.c.name==select([addresses.c.email_address]).where(addresses.c.user_id==users.c.id).as_scalar())
                
                
                
                
                d = table.delete(and_(table.c.stname == map.sourcetable,table.c.ttname == map.targettable,table.c.project_slug == projectObj.slug))
                d.execute()
                
                if db_type == "client":
                    map.delete()
        
        except Exception as e:
            errors.append(e)
            print e
    else:
        print "NO TABLE MAP TO DELETE"
        
    
    #--------------------------------------------
    # ADD NEW TABLE MAP 
    #--------------------------------------------
    try:
        new_tablemap = SyncTableDetails.objects.filter(db_status='new',projectid_id=project_id)
    except UserList.DoesNotExist:
        new_tablemap = None

    if new_tablemap:
        print "***ADDING TABLE MAP***"

        
        
        try:
           for map in new_tablemap:
                print map.sourcetable
                print "------"
                ins = table.insert().values(stname=map.sourcetable, ttname=map.targettable, url=map.url, dependson=map.dependson, orderno=map.orderno,wherecon=map.wherecon,project_slug=projectObj.slug)
                ins.execute()

                if db_type == "client":
                    map.db_status='updated'
                    map.save()
        except Exception as e:
            errors.append(e)
            print e
    else:
        print "NO TABLE MAP TO ADD"

    
    
    #--------------------------------------------
    # UPDATE TABLE MAP 
    #--------------------------------------------
    try:
        edited_tablemap = EditedTableMap.objects.filter(pid=project_id)
    except UserList.DoesNotExist:
        edited_tablemap = None

    if edited_tablemap:
        print "***EDIT TABLE MAP***"
        print edited_tablemap
        
        try:
            for map in edited_tablemap:
                print map.old_sourcetable
                print "------"
                
                try:
                    tablemap_obj = SyncTableDetails.objects.get(id=map.synctable_id)
                except SyncTableDetails.DoesNotExist:
                    tablemap_obj = None
                
                if tablemap_obj:
                    updateColumn = table.update().where(and_(table.c.stname == map.old_sourcetable,table.c.ttname == map.old_targettable,table.c.project_slug == projectObj.slug)).values(stname=tablemap_obj.sourcetable, ttname=tablemap_obj.targettable, url=tablemap_obj.url, dependson=tablemap_obj.dependson, orderno=tablemap_obj.orderno,wherecon=tablemap_obj.wherecon)
                    updateColumn.execute()
                    
                    if db_type == "client":
                        tablemap_obj.db_status = 'updated'
                        tablemap_obj.save()
                        map.delete()
                else:
                    if db_type == "client":
                        map.delete()
        except Exception as e:
            errors.append(e)
            print e
    else:
        print "NO TABLE MAP TO Edit"


def update_columnmap(meta,engine,project_id,table,columnmap_table,db_type):
    
    projectObj = Project.objects.get(id=project_id)

   

    print "**COlUMN MAP Table**"
    print columnmap_table

    print "UPDATE COLUMNMAP"
    print "----------------"

    

    #--------------------------------------------
    # DELETE COLUMN MAP 
    #--------------------------------------------
    try:
        delete_status_columnmap = SyncColumnDetails.objects.filter(db_status='deleted',projectid_id=project_id)
    except SyncColumnDetails.DoesNotExist:
        delete_status_columnmap = None

    if delete_status_columnmap:
        print "***DELETING COLUMNMAP***"
        
        try:
            for map in delete_status_columnmap:
                print map.sourcefield
                print "------"
                
                
                #-----------------------------------------------------
                # FIND PARENT TABLE MAP FK FOR CORRESPONDING COLUMN MAP 
                #------------------------------------------------------
                
                tableMapObj = SyncTableDetails.objects.get(id=map.syncTable_id)
                s = select([table.c.moduleid]).where(and_(table.c.stname == tableMapObj.sourcetable,table.c.ttname == tableMapObj.targettable,table.c.project_slug == projectObj.slug))
                result = s.execute()
                tableMapFKId_delete = None
                # print result.rowcount
                # print result.keys()
                
                for row in result:
                    print row.moduleid
                    tableMapFKId_delete = row.moduleid
                    # print repr(row)
                
                d = columnmap_table.delete(and_(columnmap_table.c.sfname == map.sourcefield,columnmap_table.c.tfname == map.targetfield,columnmap_table.c.moduleid == tableMapFKId_delete,columnmap_table.c.project_slug == projectObj.slug))
                d.execute()
                
                if db_type == "client":
                    map.delete()
        except Exception as e:
            errors.append(e)
            print e
    else:
        print "No COLUMN MAP TO DELETE"
        
    
    #--------------------------------------------
    # ADD NEW COLUMN MAP 
    #--------------------------------------------
    try:
        new_cmap = SyncColumnDetails.objects.filter(db_status='new',projectid_id=project_id)
    except SyncColumnDetails.DoesNotExist:
        new_cmap = None

    if new_cmap:
        print "***ADDING COLUMN MAP***"
        
        try:
           for map in new_cmap:
                print map.sourcefield
                print "------"

                #-----------------------------------------------------
                # FIND PARENT TABLE MAP FK FOR CORRESPONDING COLUMN MAP 
                #------------------------------------------------------
                
                tableMapObj = SyncTableDetails.objects.get(id=map.syncTable_id)
                s = select([table.c.moduleid]).where(and_(table.c.stname == tableMapObj.sourcetable,table.c.ttname == tableMapObj.targettable,table.c.project_slug == projectObj.slug))
                result = s.execute()
                tableMapFKId_add = None
                # print result.rowcount
                # print result.keys()
                
                for row in result:
                    print row.moduleid
                    tableMapFKId_add = row.moduleid
                    # print repr(row)


                ins = columnmap_table.insert().values(moduleid = tableMapFKId_add,sfname = map.sourcefield,tfname = map.targetfield,shortid = map.shortid,project_slug = projectObj.slug)
                ins.execute()
                if db_type == "client":
                    map.db_status='updated'
                    map.save()
        except Exception as e:
            errors.append(e)
            print e
    else:
        print "NO COLUMN MAP TO ADD"

    
    
    #--------------------------------------------
    # UPDATE COLUMN MAP 
    #--------------------------------------------
    try:
        edited_cmap = EditedColumnMap.objects.filter(pid=project_id)
    except EditedColumnMap.DoesNotExist:
        edited_cmap = None

    if edited_cmap:
        print "***EDIT COLUMN MAP***"
        print edited_cmap
        
        try:
            for map in edited_cmap:
                print map.old_sourcefield
                print "------"
                
                try:
                    cmapObj = SyncColumnDetails.objects.get(id=map.synccolumn_id)
                except SyncColumnDetails.DoesNotExist:
                    cmapObj = None
                
                if cmapObj:
                    #-----------------------------------------------------
                    # FIND PARENT TABLE MAP FK FOR CORRESPONDING COLUMN MAP 
                    #------------------------------------------------------
                    
                    tableMapObj = SyncTableDetails.objects.get(id=cmapObj.syncTable_id)
                    s = select([table.c.moduleid]).where(and_(table.c.stname == tableMapObj.sourcetable,table.c.ttname == tableMapObj.targettable,table.c.project_slug == projectObj.slug))
                    result = s.execute()
                    tableMapFKId_edit = None
                    # print result.rowcount
                    # print result.keys()
                    
                    
                    for row in result:
                        print row.moduleid
                        tableMapFKId_edit = row.moduleid
                        # print repr(row)

                    updateColumn = columnmap_table.update().where(and_(columnmap_table.c.moduleid==tableMapFKId_edit,columnmap_table.c.sfname==map.old_sourcefield,columnmap_table.c.tfname==map.old_targetfield,columnmap_table.c.project_slug == projectObj.slug)).values(sfname = cmapObj.sourcefield,tfname = cmapObj.targetfield,shortid = cmapObj.shortid)
                    updateColumn.execute()
                    
                    if db_type == "client":
                        cmapObj.db_status = 'updated'
                        cmapObj.save()
                        map.delete()
                
                else:
                    # Column Map has been deleted after edit
                    if db_type == "client":
                        map.delete()

        except Exception as e:
            errors.append(e)
            print e
    else:
        print "NO COLUMN MAP TO EDIT"




