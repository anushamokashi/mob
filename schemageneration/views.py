# -*- coding: utf-8 -*-
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
from slugify import slugify


from .models import Transaction
from authentication.models import userprofile
from project.models import Project, Projectwiseusersetup
from transaction.models import Transaction,Txtabledetails,Txtablecomponentdetails 
from schema.models import Db_connections_info, Db_profile
from .models import GenerateSchemaTableComponent,GenerateSchemaComponent
from transaction.forms import UserTransForm,TableDetailsform,TableComponentform
from transaction.serializers import TransactionSerializer,TxtabledetailsSerializer,TxtablecomponentdetailsSerializer

logger = logging.getLogger(__name__)

# Create your views here.
#errors =[]

def generate_schema(request,transaction_id,project_id,userid):
    errors = []
    regex_pattern = r'[^-a-z0-9_]+'
    try:
        server_engine = get_server_engine(userid,project_id,errors)
        client_engine = get_client_engine(userid,project_id,errors)
               
    except Exception as e:
        errors.append(e)
        return errors

    print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    print "SERVER ENGINE ", server_engine.name
    print "CLIENT ENGINE ", client_engine.name 

    server_meta = schema.MetaData(server_engine)
    client_meta = schema.MetaData(client_engine)

    projObj = Project.objects.get(id=project_id)
    is_table_underscore_type =  projObj.table_append_by_underscore
    
    if server_engine and client_engine is not None:

        tablecomponents = get_table_components(transaction_id,project_id,userid)
        primaryTable= getPrimaryTable(tablecomponents)
        
        
        #meta.bind = engine
        table_dict = {}
        column = None
        data_type = None     
        
        if server_engine.name=="oracle":            
            db_keyword_sql = "select * from v$reserved_words"        
        elif server_engine.name=="mysql" and client_engine.name == "sqlite":
            db_keyword_sql = "select * from mysql.help_keyword"
        elif server_engine.name=="postgresql":
            db_keyword_sql = "select * from pg_get_keywords()" 
       

    
        connection = None
        try:
            connection = server_engine.connect()
            if db_keyword_sql:
                result = connection.execute(db_keyword_sql)           
        except Exception as e:
            result = None
            errors.append(e)            
            return errors
        finally:
            if connection:
                connection.close()

        if result:
            if server_engine.name=="oracle":
                reserved_key_dict = dict([(row['keyword'],row) for row in result])
            elif server_engine.name=="mysql":
                reserved_key_dict = dict([(row['name'],row) for row in result])
            elif server_engine.name=="sqlite":
                reserved_key_dict = dict([(row['name'],row) for row in result])
        else:
            reserved_key_dict = []

        #--------------------------------------------
        #  DELETE TABLE FROM DATABASE
        #--------------------------------------------

        try:
            del_status_table = Txtabledetails.objects.filter(projectid_id= project_id,transactionid_id = transaction_id,status="deleted")
        except Txtabledetails.DoesNotExist:
            del_status_table = None
        print "TABLE WITH DELETE STATUS  ",del_status_table
        
            
        if del_status_table:
            with db_trans.atomic():
                
                #DELETE CHILDERN TABLE FIRST  
                
                for tab_comp in del_status_table:
                    if tab_comp.isprimary == False:
                        def deletingTable(tab_comp,engine,db_type):
                            print "DELETING CHILD TABLE",tab_comp.table_slug
                            try:

                                try:
                                    insp = reflection.Inspector.from_engine(engine)
                                    table_names = insp.get_table_names()  
                                except:
                                    insp = None
                                    table_names = None
                                
                                if not tab_comp.table_slug in table_names:
                                    print "TABLE_NAMES",table_names
                                    print "CHILD_TABLE",tab_comp.table_slug
                                    errors.append(engine.name+": You are tring to delete a table "+tab_comp.table_slug.upper()+" that DOES NOT EXIST in database" )
                                    return errors
                                else:
                                    connection = None
                                    if engine.name=="oracle":
                                        delete_table_sql = "DROP TABLE %s CASCADE CONSTRAINTS" %(tab_comp.table_slug)
                                    
                                    elif engine.name=="mysql" or "sqlite":                
                                        delete_table_sql = "DROP TABLE %s" %(tab_comp.table_slug)
                                    
                                    else:
                                        delete_table_sql = None
                                    
                                    if  delete_table_sql:
                                        execute_sql(engine, delete_table_sql,errors)
                                    
                                    if db_type != "both":
                                        tab_comp.delete()
                                    else:
                                        if engine.name=="sqlite":
                                            tab_comp.delete()

                            except Exception as e:
                                errors.append(e)
                                if connection:
                                    connection.close() 
                                return errors

                        db_type = tab_comp.db_type 
                        
                        if db_type == "server":
                            engine = server_engine
                            deletingTable(tab_comp,engine,db_type)
                        elif db_type == "client":
                            engine = client_engine
                            deletingTable(tab_comp,engine,db_type)
                        elif db_type == "both":
                            deletingTable(tab_comp,server_engine,db_type)
                            deletingTable(tab_comp,client_engine,db_type)
                

                #DELETE PARENT TABLE
                try:
                    del_primary_table_comp = Txtabledetails.objects.get(projectid_id= project_id,transactionid_id = transaction_id,isprimary=True,status="deleted")
                except Txtabledetails.DoesNotExist:
                    del_primary_table_comp = None
                print "DEl STATUS PRIMARTY TABLE",del_primary_table_comp
                
                if del_primary_table_comp:
                    print "DELETING PARENT TABLE",del_primary_table_comp.table_slug
                    
                    def deletePrimaryTable(primayTable,engine,db_type):
                        try:
                            insp = reflection.Inspector.from_engine(engine)
                            table_names = insp.get_table_names()  
                        except:
                            insp = None
                            table_names = None
                        
                        if not del_primary_table_comp.table_slug in table_names:
                            print "TABLE NAMES",table_names
                            print "PARENT DEl TABLE",del_primary_table_comp.table_slug
                            errors.append( engine.name+": You are tring to delete a table "+primayTable.table_slug.upper()+" that DOES NOT EXIST in database" )
                            return errors
                        
                        else:
                            print "TABLE NAMES",table_names
                            print "PARENT DEl TABLE",del_primary_table_comp.table_slug
                            delete_table_sql = "DROP TABLE %s" %(primayTable.table_slug)
                            execute_sql(engine, delete_table_sql,errors)

                            if db_type != "both":
                                primayTable.delete()
                            else:
                                if engine.name=="sqlite":
                                    primayTable.delete()
                            
                            
                    if del_primary_table_comp.db_type == "both":
                       deletePrimaryTable(del_primary_table_comp,server_engine,del_primary_table_comp.db_type)
                       deletePrimaryTable(del_primary_table_comp,client_engine,del_primary_table_comp.db_type)
                   
                    elif del_primary_table_comp.db_type == "server":
                        deletePrimaryTable(del_primary_table_comp,server_engine,del_primary_table_comp.db_type)
                    elif del_primary_table_comp.db_type == "client":
                        deletePrimaryTable(del_primary_table_comp,client_engine,del_primary_table_comp.db_type)

        
        # --------------------------------------------
        # MODIFIY TABLE
        # --------------------------------------------

        try:
            child_modified_tables =  Txtabledetails.objects.filter(projectid_id= project_id,transactionid_id = transaction_id,status="modified",isprimary=False)
        except Txtabledetails.DoesNotExist:
            child_modified_tables = None
        
        if child_modified_tables:
            for tablecomponent in child_modified_tables:
                

                try:
                    generate_schema_table_comp = GenerateSchemaTableComponent.objects.get(projectid_id=project_id,transactionid_id=transaction_id,table_id=tablecomponent.id)                        
                except GenerateSchemaTableComponent.DoesNotExist:
                    errors.append("Something went wrong While Modifing Child Table "+tablecomponent.table_slug.upper())
                    return errors
                except GenerateSchemaTableComponent.MultipleObjectsReturned:
                    errors.append("Multiple Objects Returned While Modifing Child Table "+tablecomponent.table_slug.upper())
                    return errors
                    
                if generate_schema_table_comp and generate_schema_table_comp.tablename:

                    print "!!!!MODIFY CHILD TABLE!!!! ",generate_schema_table_comp
                    print "----------------------------"
                    
                    if generate_schema_table_comp.table_slug == tablecomponent.table_slug:
                        tablecomponent.status = "updated"
                        tablecomponent.save()
                        generate_schema_table_comp.delete()
                        print "NO NEED TO RENAME CHILD TABLE TABLE ",generate_schema_table_comp.table_slug
                    
                    else:
                        with db_trans.atomic():

                            if tablecomponent.table_slug.upper() not in reserved_key_dict:
                                
                                print "RENAMING  CHILD TABLE",generate_schema_table_comp.table_slug 

                                def renameTable(engine,meta,generate_schema_table_comp,tablecomponent,db_type):
                                    try:
                                        if is_table_underscore_type == True:
                                            oldTablePk = generate_schema_table_comp.table_slug+"_id"
                                            newTablepk = tablecomponent.table_slug+"_id"
                                        else: 
                                            oldTablePk = tablecomponent.table_slug+"id"
                                            newTablepk = tablecomponent.table_slug+"id"

                                        if engine.name=="oracle" or engine.name == "mysql":
                                            rename_table_sql = "ALTER TABLE %s RENAME TO %s"%(generate_schema_table_comp.table_slug,tablecomponent.table_slug)    
                                            execute_sql(engine, rename_table_sql,errors)
                                                                            
                                        if engine.name=="oracle": 
                                            rename_column_sql = "ALTER TABLE %s RENAME COLUMN %s TO %s" %(tablecomponent.table_slug,oldTablePk,newTablepk)
                                            execute_sql(engine, rename_column_sql,errors)
                                        
                                        elif engine.name=="mysql":
                                            rename_column_sql = "ALTER TABLE %s CHANGE %s %s BIGINT" %(tablecomponent.table_slug,oldTablePk,newTablepk)
                                            execute_sql(engine, rename_column_sql,errors)

                                        elif engine.name=="sqlite":
                                            drop_table_sql =  "DROP TABLE %s" %(generate_schema_table_comp.table_slug)
                                            execute_sql(engine, drop_table_sql,errors)
                                            new_meta = schema.MetaData(engine)
                                            new_meta.reflect(bind=engine)
                                            newtable = schema.Table(tablecomponent.table_slug,new_meta) 
                                            create_sqlite_tab(engine,newtable,tablecomponent,primaryTable,reserved_key_dict,errors,project_id,is_table_underscore_type)
                                            
                                            rename_column_sql = ""                           
                                        
                                        
                                        if db_type == "both":
                                            if engine.name == "sqlite":
                                                tablecomponent.status = "updated"
                                                tablecomponent.save()
                                                generate_schema_table_comp.delete()
                                        else:
                                            tablecomponent.status = "updated"
                                            tablecomponent.save()
                                            generate_schema_table_comp.delete()

                                    
                                    except Exception as e:
                                        errors.append(e)
                                        return errors
                                    
                                if tablecomponent.db_type == "server":
                                    renameTable(server_engine,server_meta,generate_schema_table_comp,tablecomponent,"server")
                                
                                elif tablecomponent.db_type == "client":
                                    renameTable(client_engine,client_meta,generate_schema_table_comp,tablecomponent,"client")
                                
                                elif tablecomponent.db_type == "both":
                                    renameTable(server_engine,server_meta,generate_schema_table_comp,tablecomponent,"both")
                                    renameTable(client_engine,client_meta,generate_schema_table_comp,tablecomponent,"both")
                            else:
                                errors.append(engine.name+": "+tablecomponent.table_slug.upper()+" is keyword.Cannot Rename Table.Restroing to previous name")
                                
                                tablecomponent.table_slug = generate_schema_table_comp.table_slug
                                tablecomponent.tablename = generate_schema_table_comp.tablename
                                tablecomponent.status = "updated"
                                tablecomponent.save()
                                generate_schema_table_comp.delete()
                                return errors

                            

        try:
            parent_modified_table =  Txtabledetails.objects.get(projectid_id= project_id,transactionid_id = transaction_id,status="modified",isprimary=True)
        except Txtabledetails.DoesNotExist:
            parent_modified_table = None
        
        if parent_modified_table:
            
            try:
                generate_schema_table_comp = GenerateSchemaTableComponent.objects.get(projectid_id=project_id,transactionid_id=transaction_id,table_id=parent_modified_table.id)                        
            except GenerateSchemaTableComponent.DoesNotExist:
                errors.append("Something went wrong While Modifing Parent Table"+parent_modified_table.table_slug)
                return errors
            except GenerateSchemaTableComponent.MultipleObjectsReturned:
                errors.append("Multiple Objects Returned While Modifing Parent Table"+parent_modified_table.table_slug)
                return errors   

            if generate_schema_table_comp.table_slug == parent_modified_table.table_slug:
                print "NO NEED TO RENAME PARENT TABLE ",generate_schema_table_comp.table_slug

                parent_modified_table.status = "updated"
                parent_modified_table.save()
                generate_schema_table_comp.delete()
                    
            else:
                with db_trans.atomic():     
                    if parent_modified_table.table_slug.upper() not in reserved_key_dict:            
                        
                        print "RENAMING PRIMARY TABLE",parent_modified_table.table_slug
                        if is_table_underscore_type == True:
                            old_pk_column_name = generate_schema_table_comp.table_slug+"_id"
                            new_pk_column_name = parent_modified_table.table_slug+"_id"
                        else:
                            old_pk_column_name = generate_schema_table_comp.table_slug+"id"
                            new_pk_column_name = parent_modified_table.table_slug+"id"
                        try:

                            #RENAMING CHILD TABLE FK COLUMN
                            for tablecomp in tablecomponents:
                                if tablecomp != primaryTable:
                                    print "RENAMING CHILD TABLE FK COLUMN ", tablecomp.table_slug
                                        
                                    def renameChildTable(engine,tablecomp):
                                        
                                        if engine.name == "mysql": 
                                            fetch_constarint_sql = "SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE CONSTRAINT_SCHEMA = SCHEMA() AND TABLE_NAME = '%s' AND REFERENCED_COLUMN_NAME = '%s'" %(tablecomp.table_slug,old_pk_column_name)
                                            connection = engine.connect()
                                            result = connection.execute(fetch_constarint_sql)

                                            for row in result:
                                                print row
                                                constraint = row['CONSTRAINT_NAME'] 
                                            
                                                drop_fk_sql = "ALTER TABLE %s DROP FOREIGN KEY %s"%(tablecomp.table_slug,constraint)
                                                execute_sql(engine, drop_fk_sql,errors)
                                            alter_child_column_name = "ALTER TABLE %s CHANGE %s %s BIGINT" %(tablecomp.table_slug,old_pk_column_name,new_pk_column_name)
                                            execute_sql(engine, alter_child_column_name,errors)
                                        
                                        elif engine.name == "sqlite":
                                            drop_child_table_sql =  "DROP TABLE %s" %(tablecomp.table_slug)
                                            execute_sql(engine, drop_child_table_sql,errors)
                                    
                                    if tablecomp.db_type == "server":
                                        renameChildTable(server_engine,tablecomp)
                                    
                                    elif tablecomp.db_type == "client":
                                        renameChildTable(client_engine,tablecomp)
                                    
                                    elif tablecomp.db_type == "both":
                                        renameChildTable(server_engine,tablecomp)
                                        renameChildTable(client_engine,tablecomp)

                            #RENAMING PARENT TABLE
                            def renameparentTable(engine,generate_schema_table_comp,parenttablecomponent,meta):
                                
                                if engine.name == "mysql":
                                    rename_table_sql = "ALTER TABLE %s RENAME TO %s"%(generate_schema_table_comp.table_slug,parenttablecomponent.table_slug)    
                                    execute_sql(engine, rename_table_sql,errors)
                                    
                                    if is_table_underscore_type == False:
                                        alter_parent_column_name = "ALTER TABLE %s CHANGE %s %s BIGINT" %(parenttablecomponent.table_slug,old_pk_column_name,new_pk_column_name)
                                        execute_sql(engine, alter_parent_column_name,errors)
                                
                                elif engine.name == "sqlite":
                                    drop_child_table_sql =  "DROP TABLE %s" %(generate_schema_table_comp.table_slug)
                                    execute_sql(engine, drop_child_table_sql,errors)

                                    # new_meta = schema.MetaData(engine)
                                    # new_meta.reflect(bind=engine)
                                    newtable = schema.Table(parenttablecomponent.table_slug, meta) 
                                    create_sqlite_tab(engine,newtable,parenttablecomponent,primaryTable,reserved_key_dict,errors,project_id,is_table_underscore_type)


                           
                            if parent_modified_table.db_type == "server":
                                renameparentTable(server_engine,generate_schema_table_comp,parent_modified_table,server_meta)
                            
                            elif parent_modified_table.db_type == "client":
                                renameparentTable(client_engine,generate_schema_table_comp,parent_modified_table,client_meta)
                            
                            elif parent_modified_table.db_type == "both":
                                renameparentTable(server_engine,generate_schema_table_comp,parent_modified_table,server_meta)
                                renameparentTable(client_engine,generate_schema_table_comp,parent_modified_table,client_meta)
                            
                            
                            #ADDING FK CONSTARINT
                            for tableitem in tablecomponents:
                                if tableitem != primaryTable:
                                    
                                    def addFkToChildTabColumn(engine,tableitem,meta):
                                        if is_table_underscore_type == True:
                                            parentTabPk = "id"
                                        else:
                                            parentTabPk = new_pk_column_name

                                        if engine.name == "mysql":
                                            add_fk_sql = "ALTER TABLE %s ADD CONSTRAINT %s_%s_fk FOREIGN KEY (%s) REFERENCES %s(%s)"%(tableitem.table_slug,slugify(tableitem.tablename, separator='_', regex_pattern=regex_pattern),new_pk_column_name,new_pk_column_name,parent_modified_table.table_slug,parentTabPk)
                                            execute_sql(engine, add_fk_sql,errors)
                                        elif engine.name == "sqlite":
                                            # new_meta = schema.MetaData(engine)
                                            # new_meta.reflect(bind=engine)
                                            newtable = schema.Table(tableitem.table_slug, meta) 
                                            create_sqlite_tab(engine,newtable,tableitem,primaryTable,reserved_key_dict,errors,project_id,is_table_underscore_type)
                                
                                
                                    if tableitem.db_type == "server":
                                        addFkToChildTabColumn(server_engine,tableitem,server_meta)
                                    
                                    elif tableitem.db_type == "client":
                                        addFkToChildTabColumn(client_engine,tableitem,client_meta)
                                    
                                    elif tableitem.db_type == "both":
                                        addFkToChildTabColumn(server_engine,tableitem,server_meta)
                                        addFkToChildTabColumn(client_engine,tableitem,client_meta)
                                            
                                        
                            
                            parent_modified_table.status = "updated"
                            parent_modified_table.save()
                            generate_schema_table_comp.delete()
                    
                        except Exception as e:
                                errors.append(e)
                                return errors
                    else:
                        errors.append(parent_modified_table.table_slug.upper()+" is keyword. Cannot Rename Table. So restroing to old slug.")
                       
                        parent_modified_table.tablename = generate_schema_table_comp.tablename
                        parent_modified_table.table_slug = generate_schema_table_comp.table_slug
                        parent_modified_table.status = "updated"
                        parent_modified_table.save()
                        generate_schema_table_comp.delete()
                        return errors

                            

        # --------------------------------------------
        # UPDATE TABLE
        # --------------------------------------------  
        
        tablecomponents_after_del = get_table_components(transaction_id,project_id,userid)
        primaryTable_after_del = getPrimaryTable(tablecomponents_after_del)
        
        print "ALL EXISTING TABLE COMPONETS TO CHECK"
        if tablecomponents_after_del:
            for tablecomponent in tablecomponents_after_del:
            
                def updateTable(tablecomponent,engine,meta,db_type):
                
                    try:
                        insp = reflection.Inspector.from_engine(engine)
                        table_names = insp.get_table_names()  
                    except:
                        insp = None
                        table_names = None  
                    
                    if engine.begin.__get__('name'):      
                        create_table(tablecomponent,transaction_id,project_id,primaryTable_after_del,reserved_key_dict,engine,meta,table_dict,table_names,insp,db_type,errors,is_table_underscore_type)
                                
                               
                if tablecomponent.db_type == "server":
                    updateTable(tablecomponent,server_engine,server_meta,"server")
                elif tablecomponent.db_type == "client":
                    updateTable(tablecomponent,client_engine,client_meta,"client")
                elif tablecomponent.db_type == "both":
                    updateTable(tablecomponent,server_engine,server_meta,"both")
                    updateTable(tablecomponent,client_engine,client_meta,"both")            
           

        # create db schema
        try:
            with db_trans.atomic():
                
                # print "CREATE META"
                # print "***********"
                # meta.create_all(bind=engine, checkfirst=True)

                print "ENGINE NAME ", server_engine.name
                print "***********"
               
                server_meta.create_all(bind=server_engine, checkfirst=True)

                print "ENGINE NAME " , client_engine.name
                print "***********"
                
                client_meta.create_all(bind=client_engine, checkfirst=True)

               
                            
           
                    
            
        except sqlalchemy.exc.NoReferencedTableError , err:
            err_tuple= ("ForeignKey referenced table does not exist. please migrate the required transaction and try again.", err)
            errors.append( err_tuple )
            logger.exception(err_tuple)        
    
        except sqlalchemy.exc.SQLAlchemyError , err :
            err_tuple =( "sqlalchemy error while db schema migration", err)
            errors.append( err_tuple )
            logger.exception(err_tuple)        
    
        except Exception , err:
            err_tuple= ("general error while db schema migration", err)
            errors.append( err_tuple )
            logger.exception(err_tuple) 
    else:
        errors.append("Please check database connection")
    return errors
   
    


def get_server_engine(userid,project_id,errors):
    
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
        server_vendor = appDbData.vendor

        filePath = settings.MEDIA_ROOT

       
        
        
        #SERVER ENGINE
        if server_vendor == 'oracle':
        
            if database:
                database_url = "%s:%s@%s:%s/?service_name=%s" % (
                    username, password, host, port, database)
    
            else:
                database_url = "%s:%s@%s:%s/?service_name=%s" % (
                    username, password, host, port, 0000)  #0000 SID
    
            server_engine = create_engine('oracle+cx_oracle://' +
                                database_url, echo=True)
    
        elif server_vendor == 'postgres':
            database_url = "%s:%s@%s:%s/%s" % (
                
                username, password, host, port, database)
    
            server_engine = create_engine("postgresql://" + database_url, echo=True)
    
        
        elif server_vendor == 'mysql':
            database_url = "%s:%s@%s:%s/%s" % (
                
                username, password, host, port, database)
            
            server_engine = create_engine("mysql://"+ database_url, echo=True)
    
    
        elif server_vendor == 'sqlite':
            
            
            if not os.path.exists(filePath+'static/ionicmeta/'+projectObj.slug+'/db/'):
                os.makedirs(filePath+'static/ionicmeta/'+projectObj.slug+'/db/')
            
            
            server_engine = create_engine('sqlite:///'+filePath+'static/ionicmeta/'+projectObj.slug+'/db/'+projectObj.slug+'.db', echo=True)

    
        
        else:
            
            
            if not os.path.exists(filePath+'static/ionicmeta/'+projectObj.slug+'/db/'):
                os.makedirs(filePath+'static/ionicmeta/'+projectObj.slug+'/db/')
            
            server_engine = create_engine('sqlite:///'+filePath+'static/ionicmeta/'+projectObj.slug+'/db/'+'test.db', echo=True)

        
    except Exception as e:
        print e
        errors.append(e)
        server_engine = None
        
        
    return server_engine


def get_client_engine(userid,project_id,errors):
    try:
        element =Projectwiseusersetup.objects.get(userid=userid,project_id = project_id)              
        
        dbprofile = element.db_profileid_id
        dbProfileData = Db_profile.objects.get(pk=dbprofile)

        projectObj = Project.objects.get(id=project_id)

        #Get CLIENT DB details
        clientDbId = dbProfileData.clientdb_id
        clientDbData = Db_connections_info.objects.get(pk=clientDbId)
            
        client_dbTitle = clientDbData.title
        client_vendor = clientDbData.vendor
        
        filePath = settings.MEDIA_ROOT

        if client_vendor == 'sqlite':
            
            if not os.path.exists(filePath+'static/ionicmeta/'+projectObj.slug+'/db/'):
                os.makedirs(filePath+'static/ionicmeta/'+projectObj.slug+'/db/')
            
            client_engine = create_engine('sqlite:///'+filePath+'static/ionicmeta/'+projectObj.slug+'/db/'+projectObj.slug+'.db', echo=True)

    
        
        else:

            if not os.path.exists(filePath+'static/ionicmeta/'+projectObj.slug+'/db/'):
                os.makedirs(filePath+'static/ionicmeta/'+projectObj.slug+'/db/')
            
            client_engine = create_engine('sqlite:///'+filePath+'static/ionicmeta/'+projectObj.slug+'/db/'+'test.db', echo=True)
    except Exception as e:
        print e
        errors.append(e)
        client_engine = None
        
    return client_engine

def get_table_components(transaction_id,project_id,user_id):
    try:
        tablecomponents =Txtabledetails.objects.filter(transactionid_id=transaction_id,projectid_id=project_id).select_related()
    except Txtabledetails.DoesNotExist:
        tablecomponents = None


    return tablecomponents


def getPrimaryTable(tablecomponents):
    
    for tablecomponent in tablecomponents:
        
        if tablecomponent.isprimary:
            
            return tablecomponent



def get_field_components(tableCompId):

    components = Txtablecomponentdetails.objects.filter(txtabledetailid_id=tableCompId , isdbfield=True).select_related()
    return components

def create_table(tablecomponent,transaction_id,project_id,primaryTable,reserved_key_dict,engine,meta,table_dict,table_names,insp,db_type,errors,is_table_underscore_type):
    
    print "UPDATE ALL TABLE"
    fieldComponents = get_field_components(tablecomponent)
    with db_trans.atomic():
        if tablecomponent.status == "new":
           
            if tablecomponent.table_slug in table_names:
                
                print "MODIFY  NEW TABLE", tablecomponent.table_slug
                table = create_table_schema(tablecomponent,transaction_id,project_id,primaryTable,engine,meta,table_dict,table_names,db_type,errors,"exist",is_table_underscore_type)
                if insp is not None:                
                    # table_columns = dict( [(column['name'],column) for column in insp.get_columns(tablecomponent.table_slug, schema=None)])  
                    table_columns = []
                    for column in insp.get_columns(tablecomponent.table_slug, schema=None):
                        table_columns.append(column['name'])

                alter_table_columns(engine,tablecomponent,fieldComponents, table, table_dict ,table_columns, meta,primaryTable,reserved_key_dict,transaction_id,project_id,db_type,errors,is_table_underscore_type)
                errors.append(engine.name+": As you are trying to add new table "+tablecomponent.table_slug.upper()+" that already Exist in Database, columns alone has been upadted!!")
            else:
                print "NEW TABLE", tablecomponent.table_slug
                table = create_table_schema(tablecomponent,transaction_id,project_id,primaryTable,engine,meta,table_dict,table_names,db_type,errors,"new",is_table_underscore_type)
                create_columns(engine,fieldComponents, table, meta,primaryTable,reserved_key_dict,table_dict,db_type,errors)
            
            if db_type == "both":
                if engine.name == "sqlite":
                    tablecomponent.status = "updated"
                    tablecomponent.save()
            else:
                tablecomponent.status = "updated"
                tablecomponent.save()

                
        else:
            if tablecomponent.table_slug in table_names:
                print "MODIFY TABLE", tablecomponent.table_slug
                table = create_table_schema(tablecomponent,transaction_id,project_id,primaryTable,engine,meta,table_dict,table_names,db_type,errors,"exist",is_table_underscore_type)
                if insp is not None:                
                    # table_columns = dict( [(column['name'],column) for column in insp.get_columns(tablecomponent.table_slug, schema=None)])  
                    table_columns = []
                    for column in insp.get_columns(tablecomponent.table_slug, schema=None):
                        table_columns.append(column['name'])

                alter_table_columns(engine,tablecomponent,fieldComponents, table, table_dict ,table_columns, meta,primaryTable,reserved_key_dict,transaction_id,project_id,db_type,errors,is_table_underscore_type)
                
            else:
                errors.append(engine.name+": You are trying to change a table "+tablecomponent.table_slug.upper()+" that does not exist in database!!.")
                return errors
         
    
def create_table_schema(tablecomponent,transaction_id,project_id,primaryTable,engine,meta,table_dict,table_names,db_type,errors,tabletype,is_table_underscore_type):
    print "CREATE TABLE SCHEMA"
    
    if tablecomponent.table_slug:    

        #Create Table    
        if engine.name=="oracle":
            table = schema.Table(tablecomponent.table_slug, meta)    
        elif engine.name=="mysql":
            table = schema.Table(tablecomponent.table_slug, meta,mysql_engine='InnoDB') 
        elif engine.name=="sqlite":
            table = schema.Table(tablecomponent.table_slug, meta)
        
        if db_type == "both":
            if engine.name == "sqlite":
                table_dict[tablecomponent.table_slug] = table  
        else:
            table_dict[tablecomponent.table_slug] = table   
        
        if is_table_underscore_type == True:
            if primaryTable != tablecomponent:
                tablePK = "%s_id" % tablecomponent.table_slug
            else:
                tablePK = "id"
        else:
            tablePK = "%sid" % tablecomponent.table_slug
        
        #Id For Table With Table Name
        if engine.name=="oracle":
            column = schema.Column(
                tablePK, Integer, primary_key=True)
        elif engine.name=="mysql":
            column = schema.Column(
                tablePK, BigInteger, primary_key=True) 
        elif engine.name=="sqlite":
            column = schema.Column(
                tablePK, Integer, primary_key=True, nullable=False) 
        
        table.append_column(column)
        
        #Primary column
        isPrimaryExist = False

        if primaryTable.table_slug in table_names:
            isPrimaryExist = True
        
        print "IS PRIMARY TABLE EXIST", isPrimaryExist
        
        if tabletype == "new":
            
            if primaryTable:
                
                if primaryTable != tablecomponent:

                    if isPrimaryExist == True or primaryTable.db_type=="both" or tablecomponent.db_type == primaryTable.db_type :
                      
                        primary_column_name = primaryTable.table_slug+"id"

                        if is_table_underscore_type == True:
                            primary_column_name = primaryTable.table_slug+"_id"
                            parentTabColumn = "id"
                        else:
                            primary_column_name = primaryTable.table_slug+"id"
                            parentTabColumn = primaryTable.table_slug+"id"
                        
                        
                        #Initially creating the Primary column
                        print "CREATING PRIMARY COLUMN FOR NEWLY ADDING TABLE"
                        try:
                            if engine.name=="oracle":
                                column = schema.Column(primary_column_name, Integer,  ForeignKey(
                                    "%s.%s" % (primaryTable.table_slug, parentTabColumn)), nullable=False,)
                            elif engine.name=="mysql":
                                column = schema.Column(primary_column_name, BigInteger,  ForeignKey(
                                    "%s.%s" % (primaryTable.table_slug, parentTabColumn)), nullable=False,)
                            elif engine.name=="sqlite":
                                column = schema.Column(primary_column_name, Integer,  ForeignKey(
                                    "%s.%s" % (primaryTable.table_slug, parentTabColumn)), nullable=False,)
                            table.append_column(column)

                            print "Primary Column ",column
                            
                        except Exception as e:
                            errors.append(e)
                            return errors
                        
                    else:
                        print "PRIMARY TABLE NOT EXIST IN THIS DATABASE"
                else:
                    print "PRIMARY AND TABLECOMP IS EQUAL"

            else:
                print "No primary Table", tablecomponent.table_slug

    else:
        table=None
    
    return table  

       


def create_columns(engine,fieldComponents, table, meta,primaryTable,reserved_key_dict,table_dict,db_type,errors):
    print "***ADD COLUMN FRESHLY***"
    column = None
    data_type = None
    is_nullable=False

    for component in fieldComponents:
        if component.columnname.upper() not in reserved_key_dict:
            data_type = get_data_type(engine,component)
            print data_type

            if data_type == None:
                print "data type is none"
                continue
    
            if component.isnull:
                is_nullable = True
            
            if table is not None:
                print table
                print engine.name
                column = schema.Column(component.field_slug, data_type, nullable=is_nullable)
                table.append_column(column)
                print column

                if db_type == "both":
                    if engine.name == "sqlite":
                        component.status = 'updated'  
                        component.save()
                else:
                    component.status = 'updated'
                    component.save()
                           
        else:
            print "Db schema migration aborted. %s is database reserved keyword" % component.columnname
            errors.append(engine.name+": column name "+component.columnname.upper()+" is database reserved keyword")
            return errors
    
    

def alter_table_columns(engine,tablecomponent,fieldComponents, table, table_dict ,table_columns,meta,primaryTable,reserved_key_dict,transaction_id,project_id,db_type,errors,is_table_underscore_type):
    column = None
    data_type = None
    is_nullable=False
    db_column_dict = dict( [(comp.field_slug,comp) for comp in fieldComponents])
    
    for component in fieldComponents:
     
        try: 
            generate_schema_comp= GenerateSchemaComponent.objects.get(column_id=component.id)
        except GenerateSchemaComponent.DoesNotExist:
            generate_schema_comp = None
            
        with db_trans.atomic():
    
            #--------------------------------------------
            # DELETE COLUMN 
            #--------------------------------------------
            if component.status == "deleted":
                if component.field_slug  not in table_columns:
                    errors.append(engine.name+": you are trying to DELETE a column "+component.field_slug.upper()+"that not exist in database")
                else:
                    print "DELETEING COLUMN", component.field_slug
                    try:

                        connection = None
                        if engine.name=="oracle":
                            delete_column_sql = "ALTER TABLE %s DROP COLUMN %s CASCADE CONSTRAINTS" %(str(table.name),component.field_slug)
                        
                        elif engine.name=="mysql":
                            select_column_constraint_sql = "select CONSTRAINT_NAME from INFORMATION_SCHEMA.KEY_COLUMN_USAGE where CONSTRAINT_SCHEMA = SCHEMA() and TABLE_NAME = '%s' and COLUMN_NAME = '%s'" %(str(table.name),component.field_slug)
                                
                            connection = engine.connect()
                            if select_column_constraint_sql:
                                result = connection.execute(select_column_constraint_sql)
                                
                            for row in result:
                                print row
                                constraint = row['CONSTRAINT_NAME']
                                print " constraint ",constraint
                                delete_column_constraint_sql = "ALTER TABLE %s DROP FOREIGN KEY %s" %(str(table.name),constraint)
                                execute_sql(engine, delete_column_constraint_sql,errors)                             
                            delete_column_sql = "ALTER TABLE %s DROP %s" %(str(table.name),component.field_slug)
                        
                        elif engine.name=="sqlite":

                            drop_table_sql =  "DROP TABLE %s" %(tablecomponent.table_slug)
                            execute_sql(engine, drop_table_sql,errors)                             

                            print "SQLIITE TABLE DELETED"
                            component.delete()
                            # new_meta = schema.MetaData(engine)
                            # new_meta.reflect(bind=engine)
                            newtable = schema.Table(tablecomponent.table_slug, meta) 
                            create_sqlite_tab(engine,newtable,tablecomponent,primaryTable,reserved_key_dict,errors,project_id,is_table_underscore_type)
                          
                            
                            delete_column_sql = ""
                        else:
                            delete_column_sql = ""

                        
                        if delete_column_sql != "":
                            execute_sql(engine, delete_column_sql,errors)
                            if db_type == "both":
                                if engine.name == "sqlite":
                                    component.delete()  
                            else:
                                component.delete()
                            
                    except Exception as e:
                        print e
                        errors.append(e)
                        if connection:
                            connection.close()


            #--------------------------------------------
            # ADD EXTRA NEWLY ADDED COLUMN
            #--------------------------------------------
            if component.status == "new":
                if component.field_slug in table_columns:
                    errors.append(engine.name+": you are trying to ADD column "+component.field_slug.upper()+"that already exist")
                    if db_type == "both":
                        if engine.name == "sqlite":
                            component.status = "updated"  
                            component.save()
                    else:
                        component.status = "updated" 
                        component.save()
                else:
                    try:
                        print "ADDING NEW EXTRA COLUMN", component.field_slug
                        print engine.name
                        if engine.name=="oracle":
                            
                            data_type = oracle_data_type(engine,component)  
                            print data_type                  
                            if data_type:
                                
                                if component.isnull:
                                    add_column_sql="ALTER TABLE %s ADD %s %s" %(str(table.name),component.field_slug,data_type)    
                                else:
                                    add_column_sql="ALTER TABLE %s ADD %s %s DEFAULT 0 NOT NULL " %(str(table.name),component.field_slug,data_type)     
                            else:     
                                add_column_sql=None 
                        
                        elif engine.name=="mysql":
                            data_type = oracle_data_type(engine,component)  
                            print data_type                    
                            
                            if data_type:
                                if component.isnull:
                                    add_column_sql="ALTER TABLE %s ADD %s %s" %(str(table.name),component.field_slug,data_type)    
                                else:
                                    add_column_sql="ALTER TABLE %s ADD %s %s NOT NULL" %(str(table.name),component.field_slug,data_type)     
                            else:     
                                add_column_sql=None
                        
                        elif engine.name=="sqlite":
                            data_type = oracle_data_type(engine,component)  
                            print data_type                    
                            
                            if data_type:
                               add_column_sql="ALTER TABLE %s ADD COLUMN %s %s" %(str(table.name),component.field_slug,data_type)    
                               
                            else:     
                                add_column_sql=None 

                        else:
                            add_column_sql = None
                            
                            

                        if add_column_sql:
                            print add_column_sql  
                            try:
                                execute_sql(engine, add_column_sql,errors) 
                                print "COLUMN ADDED SUCESSFULLY IN DB" 
                                if db_type == "both":
                                    if engine.name == "sqlite":
                                        component.status = "updated"  
                                        component.save()
                                else:
                                    component.status = "updated" 
                                    component.save()
                            except Exception as e:
                                errors.append(e)
                                return errors
                                
                        
                    except Exception as e:
                        errors.append(e)
                        return errors
            #--------------------------------------------
            # MODIFY COLUMN 
            #--------------------------------------------

            if generate_schema_comp and component.status == "modified":
                print "ALL COLUMNS", table_columns
                print "COMPONENT SLUG", component.field_slug
                if generate_schema_comp.field_slug in table_columns: 
            
                    try:
                        
                        print "MODIFING COLUMN", component.field_slug
                        
                        #--------------------------------------------
                        # RENAME COLUMN 
                        #--------------------------------------------
                        
                        if  generate_schema_comp.field_slug == component.field_slug:
                            print "NO CHANGE IN COLUMN NANE"
                                            
                        else:
                            if component.field_slug.upper() not in reserved_key_dict:
                            
                                print "^^RENAMING COLUMN NAME^^"
                                column_data_type = oracle_data_type(engine,component)
                                try:
                                        
                                    if engine.name=="oracle": 
                                        rename_column_sql = "ALTER TABLE %s RENAME COLUMN %s TO %s" %(str(table.name),generate_schema_comp.field_slug,component.field_slug)
                                    elif engine.name=="mysql":
                                        rename_column_sql = "ALTER TABLE %s CHANGE %s %s %s" %(str(table.name),generate_schema_comp.field_slug,component.field_slug,column_data_type)
                                    elif engine.name=="sqlite":

                                        drop_table_sql =  "DROP TABLE %s" %(tablecomponent.table_slug)
                                        execute_sql(engine, drop_table_sql,errors)
                                       
                                        
                                        # new_meta = schema.MetaData(engine)
                                        # new_meta.reflect(bind=engine)
                                        
                                        newtable = schema.Table(tablecomponent.table_slug, meta) 
                                        create_sqlite_tab(engine,newtable,tablecomponent,primaryTable,reserved_key_dict,errors,project_id,is_table_underscore_type)
                                        rename_column_sql = None
                                    
                                    if rename_column_sql:
                                        execute_sql(engine, rename_column_sql,errors)                                
                                
                                except Exception as e:
                                    errors.append(e)
                                    return errors
                            else:
                                errors.append(engine.name+": column name "+component.field_slug.upper()+" is database reserved keyword. So restoring to old slug.")
                                component.field_slug = generate_schema_comp.field_slug
                                component.columnname = generate_schema_comp.columnname
                                component.status = "updated"
                                component.save()
                                generate_schema_comp.delete()                             
                                return errors

                        #--------------------------------------------
                        # CHANGE COLUMN DATATYPE 
                        #--------------------------------------------
                                    
                        if generate_schema_comp.datatype==component.datatype:
                            print "NO CHNAGE IN DATA TYPE"
                        else:
                            print "^^CHANGING COLUMN  DATA TYPE^^"
                            column_data_type = oracle_data_type(engine,component)
                            try:

                                if engine.name == "oracle":        
                                    alter_column_sql = "ALTER TABLE %s MODIFY ( %s %s)" % (str(table.name),component.field_slug,column_data_type)                                
                                elif engine.name == "mysql":
                                    alter_column_sql = "ALTER TABLE %s MODIFY %s %s" % (str(table.name),component.field_slug,column_data_type)  
                                elif engine.name == "postgresql":
                                    alter_column_sql = "ALTER TABLE %s ALTER COLUMN %s TYPE %s" % (str(table.name),component.field_slug,column_data_type) 
                                elif engine.name=="sqlite":

                                    drop_table_sql =  "DROP TABLE %s" %(tablecomponent.table_slug)
                                    execute_sql(engine, drop_table_sql,errors)
                                    
                                    # new_meta = schema.MetaData(engine)
                                    # new_meta.reflect(bind=engine)
                                    
                                    newtable = schema.Table(tablecomponent.table_slug, meta) 
                                    create_sqlite_tab(engine,newtable,tablecomponent,primaryTable,reserved_key_dict,errors,project_id,is_table_underscore_type)
                                    alter_column_sql = None
                                else:
                                    alter_column_sql = None
                                
                                if alter_column_sql: 
                                    execute_sql(engine, alter_column_sql,errors)
                            
                            except Exception as e:
                                errors.append(e)
                                return errors

                                
                        #--------------------------------------------
                        # CHANGE COLUMN NULL CONSTARINT
                        #--------------------------------------------

                        if generate_schema_comp.isnull==component.isnull:
                            print "NO CHANGE IN NULL CONSTARINT"
                        else:
                            print "^^CHANGING COLUMN NULL CONSTARIN^^"
                            column_data_type = oracle_data_type(engine,component)
                            try:
                                if component.isnull:
                                    if engine.name == "oracle":        
                                        alter_column_sql = "ALTER TABLE %s MODIFY %s NULL" % (str(table.name),component.field_slug)                                
                                    elif engine.name == "mysql":
                                        alter_column_sql = "ALTER TABLE %s MODIFY %s %s NULL" % (str(table.name),component.field_slug,column_data_type)  
                                    elif engine.name == "postgresql":
                                        alter_column_sql = "ALTER TABLE %s ALTER COLUMN %s TYPE %s DROP NOT NULL" % (str(table.name),component.field_slug,column_data_type)
                                    elif engine.name=="sqlite":

                                        drop_table_sql =  "DROP TABLE %s" %(tablecomponent.table_slug)
                                        execute_sql(engine, drop_table_sql,errors)
                                        
                                        # new_meta = schema.MetaData(engine)
                                        # new_meta.reflect(bind=engine)
                                        
                                        newtable = schema.Table(tablecomponent.table_slug, meta) 
                                        create_sqlite_tab(engine,newtable,tablecomponent,primaryTable,reserved_key_dict,errors,project_id,is_table_underscore_type)

                                        alter_column_sql = None
                                    else:
                                        alter_column_sql = None
                                else:
                                    column_data_type = oracle_data_type(engine,component)
                                    if engine.name == "oracle":        
                                        alter_column_sql = "ALTER TABLE %s MODIFY %s NOT NULL" % (str(table.name),component.field_slug)                                
                                    elif engine.name == "mysql":
                                        alter_column_sql = "ALTER TABLE %s MODIFY %s %s NOT NULL" % (str(table.name),component.field_slug,column_data_type)
                                    elif engine.name == "postgresql":
                                        alter_column_sql = "ALTER TABLE %s ALTER COLUMN %s TYPE %s SET NOT NULL" % (str(table.name),component.field_slug,column_data_type)         
                                    elif engine.name=="sqlite":

                                        drop_table_sql =  "DROP TABLE %s" %(tablecomponent.table_slug)
                                        execute_sql(engine, drop_table_sql,errors)
                                        
                                        # new_meta = schema.MetaData(engine)
                                        # new_meta.reflect(bind=engine)
                                        
                                        newtable = schema.Table(tablecomponent.table_slug, meta) 
                                        create_sqlite_tab(engine,newtable,tablecomponent,primaryTable,reserved_key_dict,errors,project_id,is_table_underscore_type)
                                        alter_column_sql = None
                                    else:
                                        alter_column_sql = None
                                
                                if alter_column_sql:
                                    execute_sql(engine, alter_column_sql,errors)
                        
                            except Exception as e:
                                errors.append(e)
                                return errors
                                
                            
                        #--------------------------------------------
                        # CHANGE MAX LENGTH, NO OF DECIMAL DIGITS
                        #--------------------------------------------
                        
                        if generate_schema_comp.maxlength==component.maxlength and generate_schema_comp.no_of_decimal_digits==component.no_of_decimal_digits:
                            print "NO CHANGE IN MAX LENGTH AND NO OF DECIMAL DIGITS"
                        else:
                            print "^^CHANGING COLUMN  MAX LENGTH^^"
                            column_data_type = oracle_data_type(engine,component)
                            try:               
                                if engine.name == "oracle" or engine.name == "mysql":
                                    modify_column_sql = "ALTER TABLE %s MODIFY %s %s" %(str(table.name),component.field_slug,column_data_type)            
                                    
                                elif engine.name=="sqlite":
                                    drop_table_sql =  "DROP TABLE %s" %(tablecomponent.table_slug)
                                    execute_sql(engine, drop_table_sql,errors)
                                    
                                    # new_meta = schema.MetaData(engine)
                                    # new_meta.reflect(bind=engine)
                                    
                                    newtable = schema.Table(tablecomponent.table_slug, meta) 
                                    create_sqlite_tab(engine,newtable,tablecomponent,primaryTable,reserved_key_dict,errors,project_id,is_table_underscore_type)

                                    modify_column_sql = None
                                
                                else:
                                    modify_column_sql = None 

                                if modify_column_sql:
                                    execute_sql(engine, modify_column_sql,errors)                              
                            
                            except Exception as e:
                                errors.append(e)
                                return errors
                        
                        if db_type == "both":
                            if engine.name == "sqlite":
                                component.status = "updated"  
                                component.save()
                                generate_schema_comp.delete()
                        else:
                            component.status = "updated" 
                            component.save()
                            generate_schema_comp.delete()  
                        
                    except Exception as e:
                        errors.append(e) 
                        print e 
                        return errors
                else:
                    errors.append(engine.name+": You are trying to alter column "+component.field_slug+" that does not exist in database")
            else:
                print "NO NEED TO MODIFY COLUMN"
           
       



def create_sqlite_tab(engine,newtable,tablecomponent,primaryTable,reserved_key_dict,errors,project_id,is_table_underscore_type):

    #-------------------------------------------------------
    #  CREATING NEW TABLE FOR SQLITE ALTERED TABLE
    #-------------------------------------------------------
    print "CREATING NEW SQLITE TABLE FOR ALTERED TBALE"
    print "TBALECOMPONENT OBJ", tablecomponent.id
    print "TABLE OBJ COLUMN"
    for c in newtable.columns:
            print c.name

    try:
        #PRIMAY KEY COLUMN
        if is_table_underscore_type == True:
            if primaryTable != tablecomponent:
                tablePK = "%s_id" % tablecomponent.table_slug
            else:
                tablePK = "id"
        else:
            tablePK = "%sid" % tablecomponent.table_slug
        
        if engine.name=="oracle":
            column = schema.Column(tablePK, Integer, primary_key=True)
        elif engine.name=="mysql":
            column = schema.Column(tablePK, BigInteger, primary_key=True)
        elif engine.name=="sqlite":
            column = schema.Column(tablePK, Integer, primary_key=True, nullable=False)
        
        newtable.append_column(column)
        
        #FK COLUMN FOR PT
        isPrimaryExist = False

        try:
            insp = reflection.Inspector.from_engine(engine)
            table_names = insp.get_table_names()  
            for table_name in table_names:
                if table_name == primaryTable.table_slug:
                    isPrimaryExist = True
        except:
            insp = None
            table_names = None

        
        
        print "IS PRIMARY TABLE EXIST", isPrimaryExist
        
        if primaryTable:
            
            if primaryTable != tablecomponent:

                if isPrimaryExist == True or primaryTable.db_type=="both" or tablecomponent.db_type == primaryTable.db_type:

                    if is_table_underscore_type == True:
                        primary_column_name = primaryTable.table_slug+"_id"
                        parentTabColumn = "id"
                    else:
                        primary_column_name = primaryTable.table_slug+"id"
                        parentTabColumn = primaryTable.table_slug+"id"
                    
                    #Initially creating the Primary column
                    print "CREATING FK COLUMN FOR SQLITE ALTERDED TABLE"
                    try:
                        if engine.name=="oracle":
                            column = schema.Column(primary_column_name, Integer,  ForeignKey(
                                "%s.%s" % (primaryTable.table_slug, parentTabColumn)), nullable=False,)
                        elif engine.name=="mysql":
                            column = schema.Column(primary_column_name, BigInteger,  ForeignKey(
                                "%s.%s" % (primaryTable.table_slug, parentTabColumn)), nullable=False,)
                        elif engine.name=="sqlite":
                            column = schema.Column(primary_column_name, Integer,  ForeignKey(
                                "%s.%s" % (primaryTable.table_slug, parentTabColumn)), nullable=False,)
                        newtable.append_column(column)

                        print "Primary Column in sqlite table ",column
                        
                    except Exception as e:
                        errors.append(e)
                        return errors
                    
                else:
                    print "PRIMARY TABLE NOT EXIST IN THIS DATABASE"
            else:
                print "PRIMARY AND TABLECOMP IS EQUAL"

        else:
            print "No primary Table", tablecomponent.table_slug
        
        #OTHER COLUMNS
        try:
            componentsObj = Txtablecomponentdetails.objects.filter(txtabledetailid_id=tablecomponent.id , isdbfield=True).select_related()                                       
        except Exception as e:
            print e
            componentsObj = None
        
        if componentsObj:
            print "TABLE OTHER COLUMNS"
            print componentsObj
            print "-------"

            for component in componentsObj:
                if component.columnname.upper() not in reserved_key_dict:
                    data_type = get_data_type(engine,component)
                    
                    if data_type == None:
                        print "data type is none"
                        continue
            
                    if component.isnull:
                        is_nullable = True
                    else:
                        is_nullable = False
                    
                    if table is not None:
                        column = schema.Column(component.field_slug, data_type, nullable=is_nullable)
                        newtable.append_column(column)
                        print column

                else:
                    print "Db schema migration aborted. %s is database reserved keyword" % component.columnname
                    errors.append(engine.name+": column name \""+component.columnname.upper()+" is database reserved keyword")
                    return errors
        newtable.create(checkfirst=True)

        
        
    
    except Exception as e:
        print "*******"
        print e
        errors.append(e)
        return errors


def execute_sql(engine,sql,errors):
    
    try:
        connection = engine.connect()
        trans = connection.begin()
        if sql:
            result = connection.execute(sql)
            trans.commit()            
    
    except Exception as e:
        errors.append(e)
        trans.rollback()
        print e
        return errors
    
    finally:
        connection.close()




def get_data_type(engine,comp):
    if comp.datatype == 'IntegerField':
        if comp.no_of_decimal_digits:
			if comp.maxlength:
				data_type = Numeric(comp.maxlength, comp.no_of_decimal_digits)
			else:
				# assuming a default precision of 38 and scale of 5.
				data_type = Numeric(38, 5)
        else:        
            if engine.name == "oracle":
                data_type = Integer
            elif engine.name == "mysql":    
                data_type = BigInteger
            elif engine.name == "sqlite":
                data_type = Integer
   
    elif str(comp.datatype) == 'TextField':
        data_type = Text
    
    elif str(comp.datatype) == 'ForeignKey_int':
        if engine.name == "oracle":
            data_type = Integer
        elif engine.name == "mysql":    
            data_type = BigInteger
        elif engine.name == "sqlite":
            data_type = Integer    
        
    elif str(comp.datatype) == 'ForeignKey_char':
        if comp.maxlength == 0:
            data_type = String(255)
        else:
            data_type = String(comp.maxlength)
        
    elif str(comp.datatype) == 'ForeignKey_date':
        data_type = Date            

    
    elif str(comp.datatype) == 'CharField':
       
        if comp.maxlength == 0:
            data_type = String(255)
        else:
            data_type = String(comp.maxlength)

    elif str(comp.datatype) == 'DecimalField':

        if comp.maxlength and comp.no_of_decimal_digits:
            data_type = Numeric(comp.maxlength, comp.no_of_decimal_digits)
        else:
            # assuming a default precision of 38 and scale of 5.
            data_type = Numeric(38, 5)

    elif str(comp.datatype) == 'BooleanField' or str(comp.datatype) == 'NullBooleanField':
        data_type = Boolean

    elif str(comp.datatype) == 'PositiveSmallIntegerField':
        data_type = SmallInteger

    elif str(comp.datatype) == 'PositiveIntegerField':
        if engine.name == "oracle":
            data_type = Integer
        elif engine.name == "mysql":    
            data_type = BigInteger
        elif engine.name == "sqlite":
            data_type = Integer

    elif str(comp.datatype) == 'BigIntegerField':
        data_type = BigInteger

    elif str(comp.datatype) == 'GenericIPAddressField':
        data_type = String(255)

    elif str(comp.datatype) == 'DateField':
        data_type = Date

    elif str(comp.datatype) == 'DateTimeField':
        data_type = DateTime

    elif str(comp.datatype) == 'UUIDField':
        # find out the string length of a guid 
        # It depends on how you format the Guid: *************************

        # Guid.NewGuid().ToString() => 36 characters (Hyphenated)
        # outputs: 12345678-1234-1234-1234-123456789abc

        # Guid.NewGuid().ToString("D") => 36 characters (Hyphenated, same as ToString())
        # outputs: 12345678-1234-1234-1234-123456789abc

        # Guid.NewGuid().ToString("N") => 32 characters (Digits only)
        # outputs: 12345678123412341234123456789abc

        # Guid.NewGuid().ToString("B") => 38 characters (Braces)
        # outputs: {12345678-1234-1234-1234-123456789abc}

        # Guid.NewGuid().ToString("P") => 38 characters (Parentheses)
        # outputs: (12345678-1234-1234-1234-123456789abc)

        # Guid.NewGuid().ToString("X") => 68 characters (Hexadecimal)
        # outputs: {0x12345678,0x1234,0x1234,{0x12,0x34,0x12,0x34,0x56,0x78,0x9a,0xbc}}        
        # ****************************************

        # assuming a length of worst case of 70 chars
        data_type = String(70)

    elif str(comp.datatype) == 'FloatField':
        data_type = Float

    elif str(comp.datatype) == 'FileField':
        # assuming a length  of 1024 chars for file path****
        data_type = BLOB(comp.maxlength)
    
    elif str(comp.datatype) == 'EmailField':
        # data_type = String(45)    
        if comp.maxlength == 0:
            data_type = String(255)
        else:
            data_type = String(comp.maxlength)
    
    elif str(comp.datatype) == 'AutoField':
        data_type = String(255)
    
    elif str(comp.datatype) == 'BinaryField':
        data_type = Binary
    
    elif str(comp.datatype) == 'FilePathField':

        if comp.maxlength == 0:
            data_type = String(255)
        else:
            data_type = String(comp.maxlength)
        
    elif str(comp.datatype) == 'ImageField':
        data_type = BLOB(comp.maxlength)
        
    elif str(comp.datatype) == 'SlugField':
        
        if comp.maxlength == 0:
            data_type = String(255)
        else:
            data_type = String(comp.maxlength)
        
    elif str(comp.datatype) == 'URLField':
       
        if comp.maxlength == 0:
            data_type = String(255)
        else:
            data_type = String(comp.maxlength)
        
    elif str(comp.datatype) == 'CommaSeparatedIntegerField':
        
        data_type = Text
    
    elif str(comp.datatype) == 'SmallIntegerField':
        
        data_type = SmallInteger
        
    elif str(comp.datatype) =='TimeField':
        
        data_type = TIMESTAMP

    # buttonfield is a ui field. there is not point wasting space in db for this. 
    # since nthing is stored here***
    
    # elif str(comp.datatype) =='ButtonField':
    #     data_type = String(25)
        
    elif str(comp.datatype) == 'DurationField':
        data_type = Interval
        
    # elif str(comp.datatype) == 'enum':
    #     data_type = String(255)
        
    elif str(comp.datatype) == 'MacroField':
        data_type = String(1024) 
    
    elif str(comp.datatype) == 'OneToOneField':
        if engine.name == "oracle":
            data_type = Integer
        elif engine.name == "mysql":    
            data_type = BigInteger
        elif engine.name == "sqlite":
            data_type = Integer
    
    elif str(comp.datatype) == 'Enum_Int':
        if engine.name == "oracle":
            data_type = Integer
        elif engine.name == "mysql":    
            data_type = BigInteger
        elif engine.name == "sqlite":
            data_type = Integer
    
    elif str(comp.datatype) == 'Enum_Char':
        if comp.maxlength == 0:
            data_type = String(255)
        else:
            data_type = String(comp.maxlength)
    
    elif str(comp.datatype) == 'Enum_Date':
        data_type = Date                
    
    else:
        # shd we raise a exception here ?********
        data_type = None
        print comp.datatype, "is not supported !!!"

    return data_type

def oracle_data_type(engine,component):                      
                   
    if component.datatype == 'IntegerField':
        
        if component.no_of_decimal_digits:
            
            if engine.name == "oracle":
                data_type = "NUMBER("+str(component.maxlength) +", "+ str(component.no_of_decimal_digits)+")"
            
            elif engine.name == "sqlite":
                data_type = "NUMBER("+str(component.maxlength) +", "+ str(component.no_of_decimal_digits)+")"
            
            else:
                data_type = "DECIMAL("+str(component.maxlength) +", "+ str(component.no_of_decimal_digits)+")"    
            
            
        
        else:
            if engine.name == "oracle":
                data_type = "NUMBER" 
            elif engine.name == "mysql":             
                data_type = "BIGINT"
            elif engine.name == "sqlite":
                data_type = "NUMBER"
    
    elif component.datatype == 'TextField':
        
        if engine.name == "oracle":
            data_type = "CLOB"
        elif engine.name == "mysql":             
            data_type = "TEXT"
        elif engine.name == "sqlite":             
            data_type = "TEXT"                

    
    elif component.datatype == 'CharField':
        
        if engine.name == "oracle":       
            if component.maxlength == 0:
                data_type = "VARCHAR2(255 CHAR)"
            else:
                data_type = "VARCHAR2("+str(component.maxlength)+" CHAR)"
        elif engine.name == "mysql":
            if component.maxlength == 0:
                data_type = "VARCHAR(255)"
            else:
                data_type = "VARCHAR("+str(component.maxlength)+")"
        
        elif engine.name == "sqlite":
           data_type = "TEXT"        

    elif component.datatype== 'DecimalField':
        if engine.name == "oracle":
            if component.maxlength and component.no_of_decimal_digits:
                data_type = "NUMBER("+str(component.maxlength) +", "+ str(component.no_of_decimal_digits)+")"
            else:           
                data_type = "NUMBER(38, 5)"
        
        elif engine.name == "mysql":
            if component.maxlength and component.no_of_decimal_digits:
                data_type = "DECIMAL("+str(component.maxlength)+", "+ str(component.no_of_decimal_digits)+")"
            else:           
                data_type = "DECIMAL(38, 5)"
        
        elif engine.name == "sqlite":
            data_type = "NUMERIC"        

    elif component.datatype == 'BooleanField' or component.datatype == 'NullBooleanField':
        if engine.name == "oracle":
            data_type = "VARCHAR2(10 CHAR)"
        elif engine.name == "mysql":
            data_type = "Boolean"
        elif engine.name == "sqlite":
            data_type = "NUMERIC"    

    elif component.datatype == 'PositiveSmallIntegerField':
        if engine.name == "oracle":
            data_type = "NUMBER"
        elif engine.name == "mysql":
            data_type = "BIGINT" 
        elif engine.name == "sqlite":
            data_type = "INTEGER"   
    elif component.datatype == 'PositiveIntegerField':
        if engine.name == "oracle":
            data_type = "NUMBER"
        elif engine.name == "mysql":
            data_type = "BIGINT"
        elif engine.name == "sqlite":
            data_type = "INTEGER"

    elif component.datatype == 'BigIntegerField':
        if engine.name == "oracle":
            data_type = "NUMBER(19, 0)"
        elif engine.name == "mysql":
            data_type = "BIGINT"
        elif engine.name == "sqlite":
            data_type = "INTEGER"    

    elif component.datatype == 'GenericIPAddressField':
        if engine.name == "oracle":
            data_type = "VARCHAR2(255 CHAR)"
        elif engine.name == "mysql":
            data_type = "VARCHAR(255)" 
        elif engine.name == "sqlite":
            data_type = "TEXT"   

    elif component.datatype == 'DateField':
        if engine.name == "oracle":
            data_type = "DATE"
        elif engine.name == "mysql":
            data_type = "DATE" 
        elif engine.name == "sqlite":
            data_type = "NUMERIC"   

    elif component.datatype == 'DateTimeField':
        if engine.name == "oracle":
            data_type = "DATE"
        elif engine.name == "mysql":
            data_type = "DATETIME"
        elif engine.name == "sqlite":
            data_type = "NUMERIC"    

    elif component.datatype == 'UUIDField':
        if engine.name == "oracle":        
            data_type = "VARCHAR2(70 CHAR)"
        elif engine.name == "mysql":
            data_type = "VARCHAR(70)" 
        elif engine.name == "sqlite":
            data_type = "TEXT"   

    elif component.datatype == 'FloatField':
        if engine.name == "oracle":
            data_type = "FLOAT"
        elif engine.name == "mysql":
            data_type = "FLOAT"  
        elif engine.name == "sqlite":
            data_type = "REAL"  

    elif component.datatype == 'FileField':
        if engine.name == "oracle":        
            data_type = "VARCHAR2(1024 CHAR)"
        elif engine.name == "mysql":
            data_type = "BLOB"  
        elif engine.name == "sqlite":
            data_type = "BLOB"  
    
    elif component.datatype == 'EmailField':
        if engine.name == "oracle":            
            if component.maxlength == 0:
                data_type = "VARCHAR2(50 CHAR)"
            else:
                data_type = "VARCHAR2("+str(component.maxlength) +" CHAR)"
        elif engine.name == "mysql":
            if component.maxlength == 0:
                data_type = "VARCHAR(50)"
            else:
                data_type = "VARCHAR("+str(component.maxlength) +")"
        
        elif engine.name == "sqlite":
            data_type = "TEXT"
                    
    elif component.datatype == 'AutoField':
        if engine.name == "oracle":
            data_type = "VARCHAR2(255 CHAR)"
        elif engine.name == "mysql":
            data_type = "VARCHAR(255)" 
        elif engine.name == "sqlite":
            data_type = "TEXT"   
    
    elif component.datatype == 'BinaryField':
        if engine.name == "oracle":
            data_type = "BLOB"
        elif engine.name == "mysql":
            data_type = "BLOB"
        elif engine.name == "sqlite":
            data_type = "BLOB"    
    
    elif component.datatype == 'FilePathField':
        if engine.name == "oracle":        
            if component.maxlength == 0:
                data_type = "VARCHAR2(50 CHAR)"
            else:
                data_type = "VARCHAR2("+str(component.maxlength) +" CHAR)"
        elif engine.name == "mysql":
            if component.maxlength == 0:
                data_type = "VARCHAR(50)"
            else:
                data_type = "VARCHAR("+str(component.maxlength) +")"
        elif engine.name == "sqlite":
            data_type = "TEXT"
                
    elif component.datatype == 'ImageField':
        if engine.name == "oracle":
            data_type = "LONGBLOB"
        elif engine.name == "mysql":    
            data_type = "LONGBLOB"
        elif engine.name == "sqlite":
            data_type = "BLOB(component.maxlength)"
    
    elif component.datatype == 'SlugField':
        
        if engine.name == "oracle":        
            if component.maxlength == 0:
                data_type = "VARCHAR2(50 CHAR)"
            else:
                data_type = "VARCHAR2("+str(component.maxlength) +" CHAR)"
        elif engine.name == "mysql":
            if component.maxlength == 0:
                data_type = "VARCHAR(50)"
            else:
                data_type = "VARCHAR("+str(component.maxlength) +")" 
        elif engine.name == "sqlite":
            data_type = "TEXT"       
        
    elif component.datatype == 'URLField':
        if engine.name == "oracle":        
            if component.maxlength == 0:
                data_type = "VARCHAR2(50 CHAR)"
            else:
                data_type = "VARCHAR2("+str(component.maxlength) +" CHAR)"
        elif engine.name == "mysql":
            if component.maxlength == 0:
                data_type = "VARCHAR(50)"
            else:
                data_type = "VARCHAR("+str(component.maxlength) +")"
        
        elif engine.name == "sqlite":
            data_type = "TEXT"        
        
    elif component.datatype == 'CommaSeparatedIntegerField':
        if engine.name == "oracle":        
            data_type = "CLOB"
        elif engine.name == "mysql":    
            data_type = "TEXT"
        elif engine.name == "sqlite":
            data_type = "TEXT"
    
    elif component.datatype == 'SmallIntegerField':
        if engine.name == "oracle":        
            data_type = "NUMBER"
        elif engine.name == "mysql":
            data_type = "BIGINT"
        elif engine.name == "sqlite":
                data_type = "INTEGER"
            
    elif component.datatype =='TimeField':
        if engine.name == "oracle":               
            data_type = "TIMESTAMP"    
        elif engine.name == "mysql":
            data_type = "TIMESTAMP"
        elif engine.name == "sqlite":
            data_type = "NUMERIC"    
        
    elif component.datatype == 'DurationField':
        if engine.name == "oracle":
            data_type = "INTERVAL DAY(2) TO SECOND(6)"
        elif engine.name == "mysql":
            data_type = "TIMESTAMP"   
        elif engine.name == "sqlite":
            data_type = "NUMERIC" 
        
    #     elif str(component.datatype) == 'enum':
    #         if engine.name == "oracle":
    #             data_type = "VARCHAR2(255 CHAR)"
    #         elif engine.name == "mysql":
    #             data_type = "VARCHAR(255)"    
        
    elif component.datatype == 'MacroField':
        if engine.name == "oracle":
            data_type = "VARCHAR2(1024 CHAR)"
        elif engine.name == "mysql":
            data_type = "BLOB" 
        elif engine.name == "sqlite":
            data_type = "BLOB"   
    
    elif component.datatype == 'OneToOneField':
        if engine.name == "oracle":
            data_type = "NUMBER"
        elif engine.name == "mysql":               
            data_type = "BIGINT"
        elif engine.name == "sqlite":
            data_type = "INTEGER"
    elif component.datatype == 'Enum_Int':
        if engine.name == "oracle":
            data_type = "NUMBER" 
        elif engine.name == "mysql":             
            data_type = "BIGINT"
        elif engine.name == "sqlite":
            data_type = "INTEGER"
        
    elif component.datatype == 'Enum_Char':
        if engine.name == "oracle":       
            if component.maxlength == 0:
                data_type = "VARCHAR2(255 CHAR)"
            else:
                data_type = "VARCHAR2("+str(component.maxlength)+" CHAR)"
        elif engine.name == "mysql":
            if component.maxlength == 0:
                data_type = "VARCHAR(255)"
            else:
                data_type = "VARCHAR("+str(component.maxlength)+")"
        elif engine.name == "sqlite":
            data_type = "TEXT"
        
    elif component.datatype == 'Enum_Date':
        if engine.name == "oracle":
            data_type = "DATE"
        elif engine.name == "mysql":
            data_type = "DATE" 
        elif engine.name == "sqlite":
            data_type = "NUMERIC"       
    else:       
        data_type = None
        print component.datatype, "is not supported !!!"
        logger.exception("%s is not supported !!!" %(component.datatype))

    return data_type
