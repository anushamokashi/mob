# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django_extensions.db.models import TimeStampedModel

from project.models import Project,Projectwiseusersetup
from transaction.models import Txtabledetails, Txtablecomponentdetails, Transaction
from authentication.models import userprofile

# Create your models here.

DDL_TYPES = (

	('add','add',),
	('modify','modify',),
	('delete','delete',),
	)




class GenerateSchemaTableComponent(TimeStampedModel):

	projectid = models.ForeignKey(Project,on_delete=models.CASCADE,blank=True, null=True)
	transactionid =  models.ForeignKey(Transaction,on_delete=models.CASCADE,blank=True, null=True)
	user = models.ForeignKey(userprofile,on_delete=models.CASCADE,blank=True, null=True)
	table = models.ForeignKey(Txtabledetails, on_delete=models.SET_NULL, blank=True, null=True)
	tablename = models.CharField(max_length=100,blank=True, null=True)
	table_slug = models.CharField(max_length=100,blank=True, null=True)
	isprimary = models.BooleanField(default=False)
	ddl_type = models.CharField(choices=DDL_TYPES, max_length=10,blank=True, null=True)
	db_type = models.CharField(max_length=100,blank=True, null=True)
	

	def __str__(self):
		return self.table_slug 



class GenerateSchemaComponent(TimeStampedModel):

	gen_schema_table = models.ForeignKey(GenerateSchemaTableComponent,on_delete=models.CASCADE,blank=True, null=True)
	column = models.ForeignKey(Txtablecomponentdetails,  on_delete=models.SET_NULL, blank=True, null=True)
	columnname = models.CharField(max_length=100)	
	datatype = models.CharField(max_length=50)	
	maxlength = models.BigIntegerField()
	no_of_decimal_digits = models.BigIntegerField(null=True,blank=True)
	field_slug = models.CharField(max_length=100)
	isdbfield = models.BooleanField(default=False)	
	isnull = models.BooleanField(default=False) 
	ddl_type = models.CharField(choices=DDL_TYPES, max_length=10,blank=True, null=True)
	db_type = models.CharField(max_length=100,blank=True, null=True)


	def __str__(self):
		return self.field_slug
