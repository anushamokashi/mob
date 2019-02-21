# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from project.models import Project
from mptt.models import MPTTModel, TreeForeignKey
from django_extensions.db.models import TimeStampedModel
from authentication.models import userprofile

# Create your models here.
RELATIONSHIP_TYPE_CHOICES = (
		('one-to-one','One-to-One'),
		('one-to-many','One-to-Many'),
	)

FIELD_DATA_TYPE_CHOICES = (
	('AutoField','AutoField'),
	('BinaryField','BinaryField'),
	('BooleanField','BooleanField'),
	('DateField','DateField'),
	('DateTimeField','DateTimeField'),
	('DecimalField','DecimalField'),
	('EmailField','EmailField'),
	('FileField','FileField'),
	('ImageField','ImageField'),
	('IntegerField','IntegerField'),
	('TextField','TextField'),
	('CharField','CharField'),
	('UUIDField','UUIDField'),
	('ForeignKey_int','ForeignKey_int'),
	('ForeignKey_char','ForeignKey_char'),
	('ForeignKey_date','ForeignKey_date'),
	('Enum_Int','Enum_Int'),
	('Enum_Char','Enum_Char'),
	('Enum_Date','Enum_Date'),
	('ButtonField','ButtonField'),
	('MacroField','MacroField'),
	('OneToOneField','OneToOneField'),
)

STATUS_CHOICES = (
	('new','new'),
	('modified','modified'),
	('updated','updated'),
	('deleted','deleted')
)

DBTYPE_CHOICES = (
	('server','server'),
	('client','client'),
	('both','both')
)
class Transaction(TimeStampedModel,models.Model):

	txname = models.CharField(max_length=100)
	txdescription = models.CharField(max_length=200,null=True,blank=True)
	projectid = models.ForeignKey(Project,on_delete=models.CASCADE)	

	def __str__(self):
		return self.txname 

class enumtitle(TimeStampedModel,models.Model):
	enum_title = models.CharField(max_length=100)
	description = models.CharField(max_length=500,null=True,blank=True)
	project_id = models.ForeignKey(Project,on_delete=models.CASCADE)	

	def __str__(self):
		return self.enum_title 

class enumkeyvalue(TimeStampedModel,models.Model):
	key = models.CharField(max_length=100)
	value = models.CharField(max_length=100)
	enum_title_fk = models.ForeignKey(enumtitle,on_delete=models.CASCADE)

	def __str__(self):
		return self.key 

class Txtabledetails(MPTTModel,models.Model):
	
	title = models.CharField(max_length=100)
	tablename = models.CharField(max_length=100)
	description = models.CharField(max_length=500,null=True,blank=True)
	relationshiptype = models.CharField(max_length=50, choices=RELATIONSHIP_TYPE_CHOICES,null=True, blank=True)
	transactionid =  models.ForeignKey(Transaction,on_delete=models.CASCADE ,related_name='custom_url_params')
	projectid = models.ForeignKey(Project,on_delete=models.CASCADE)
	isprimary = models.BooleanField(default=True) 
	table_slug = models.CharField(max_length=100)
	db_type = models.CharField(max_length=50, choices=DBTYPE_CHOICES,default='both')
	status = models.CharField(max_length=20, choices=STATUS_CHOICES,null=True, blank=True)
	parent = models.ForeignKey('self',on_delete=models.CASCADE,blank=True, null=True)
	user = models.ForeignKey(userprofile,on_delete=models.CASCADE,blank=True, null=True)

	def __str__(self):
		return self.tablename 
	
	class Meta:
		unique_together = ["table_slug", "projectid"]

class Txtablecomponentdetails(TimeStampedModel,models.Model):

	title = models.CharField(max_length=100)	
	txtabledetailid = models.ForeignKey(Txtabledetails,on_delete=models.CASCADE,related_name='custom_url_params')
	columnname = models.CharField(max_length=100)	
	datatype = models.CharField(max_length=50, choices=FIELD_DATA_TYPE_CHOICES)	
	maxlength = models.BigIntegerField()
	no_of_decimal_digits = models.BigIntegerField(null=True,blank=True)
	field_slug = models.CharField(max_length=100)
	isdbfield = models.BooleanField(default=True)	
	isnull = models.BooleanField(default=True) 
	is_system_component = models.BooleanField(default=False)
	enum = models.ForeignKey(enumtitle,on_delete=models.SET_NULL,blank=True, null=True)
	db_type = models.CharField(max_length=50, choices=DBTYPE_CHOICES,default='both')
	status = models.CharField(max_length=20, choices=STATUS_CHOICES,null=True, blank=True)
	user = models.ForeignKey(userprofile,on_delete=models.CASCADE,blank=True, null=True)


	def __str__(self):
		return self.columnname 
	
	class Meta:
		unique_together = ["field_slug", "txtabledetailid"]

	

