# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
from project.models import Project
from transaction.models import Transaction,Txtabledetails
from mptt.models import MPTTModel, TreeForeignKey
from django_extensions.db.models import TimeStampedModel

# Create your models here.
VIEW_TYPE_CHOICES = (
	('carousel','Carousel'),
	('ng','None_Grid'),
	('grid','Grid'),
	('euptxn','Eupdate Transactionview')
	)
CONTAINER_TYPE_CHOICES=(
	('card','Card'),
	('list','List'),
	('grid','Grid')
	)
INPUT_TYPE_CHOICES=(
	('fixed','Fixed'),
	('floating','Floating'),
	('placeholder','Placeholder'),
	('stacked','Stacked'),
	('boxed','Boxed'),
	)
WIDGET_TYPE_CHOICES=(
	('button','Button'),
	('check','Checkbox'),
	('date','Date'),
	('email','Email'),
	('password','Password'),
	('number','Number'),
	('select','Select'),
	('text','Text'),
	('time','Time'),
	('textarea','Textarea'),
	('radio','Radiobox'),
	('scan','Scan'),
	('upload','Upload'),
	('stot','Speech-To-Text'),
	('dpop',"Dynamic Popup")
	)
MODE_OF_ENTRY = (
	('tbe','ToBeEnter'),
	('tbc','ToBeCalculate'),
)

SAVE_TYPE = (
	('offline','Offline'),
	('online','Online'),
	('both','Both')
)

UPDATE_TYPE = (
	('add','Add'),
	('sub','Sub'),
	('inc','Inc'),
	('dec','Dec'),
	('replace','Replace')
)

HEADER_CHOICES = (
    ('fix','Fixed Header'),
	('flex','Flexible Header'),
	('noheader','No Header')
)

HEADERCOLOR_CHOICES = (
    ('yes','Yes'),
	('no','No')
)
COLOR_CHOICES =(
  ('primary','Primary'),
  ('secondary','Secondary')
)
LABEL_COLOR_CHOICES =(
  ('primary','Primary'),
  ('secondary','Secondary'),
  ('dark','Dark')
)

class Transactionview(TimeStampedModel,models.Model):
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=500)
	viewtype = models.CharField(max_length=50, choices=VIEW_TYPE_CHOICES,null=True, blank=True)
	savetype = models.CharField(max_length=50, choices=SAVE_TYPE,null=True, blank=True)
	transactionid = models.ForeignKey(Transaction,on_delete=models.CASCADE ,related_name='txnview_transaction')
	projectid = models.ForeignKey(Project,on_delete=models.CASCADE ,related_name='txn_projectid')
	createpage = models.BooleanField(default=True)
	identifiers = models.CharField(max_length=150,null=True, blank=True)
	expression = models.CharField(max_length=10000,null=True, blank=True) #### Apply For Whole TxnView 
	postfixexp = models.CharField(max_length=10000,null=True, blank=True)

	def __str__(self):
		return self.title
	
		
class Container(MPTTModel,TimeStampedModel,models.Model):
	title = models.CharField(max_length=100)
	caption = models.CharField(max_length=100)
	containertype = models.CharField(max_length=50, choices=CONTAINER_TYPE_CHOICES,null=True, blank=True)
	inputtype = models.CharField(max_length=50, choices=INPUT_TYPE_CHOICES,null=True, blank=True)
	parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
	transactionviewid =  models.ForeignKey(Transactionview,on_delete=models.CASCADE ,related_name='custom2_url_params')
	expression = models.CharField(max_length=1000,null=True, blank=True)  #### Apply For Grid Container
	displayorder = models.BigIntegerField(null=True, blank=True)
	dbtable = models.ForeignKey(Txtabledetails,on_delete=models.SET_NULL,null = True,blank=True,related_name='container_dbtable')
	identifiers = models.CharField(max_length=150,null=True, blank=True)

	def __str__(self):
		return self.identifiers

	class Meta:
		ordering = ['displayorder']

class Component(TimeStampedModel,models.Model):
	title = models.CharField(max_length=100,null=True, blank=True)
	caption = models.CharField(max_length=100,null=True, blank=True)
	is_readonly = models.BooleanField(default=False)
	is_hidden = models.BooleanField(default=False)
	is_required = models.BooleanField(default=False)
	allow_duplicate = models.BooleanField(default=False)
	widgettype = models.CharField(max_length=50, choices=WIDGET_TYPE_CHOICES,null=True, blank=True)
	expression = models.CharField(max_length=100,null=True, blank=True)  ####  For Particular Component
	validateexp = models.CharField(max_length=100,null=True, blank=True)
	sql = models.CharField(max_length=1000,null=True, blank=True)
	displayorder = models.BigIntegerField(null=True, blank=True)
	containerid = models.ForeignKey(Container,on_delete=models.CASCADE ,related_name='custom3_url_params')
	transactionviewid = models.ForeignKey(Transactionview,on_delete=models.CASCADE ,related_name='custom3_url_params')
	identifiers = models.CharField(max_length=150,null=True, blank=True)
	componentrefer_id = models.BigIntegerField(null=True, blank=True)
	componenttype = models.CharField(max_length=150,null=True, blank=True)
	dbcolumn = models.CharField(max_length=150,null=True, blank=True)  
	componentrefer_dt = models.CharField(max_length=15000,null=True, blank=True)
	modeOfEntry = models.CharField(max_length=50, choices=MODE_OF_ENTRY,null=True, blank=True)
	suggestive = models.BooleanField(default=False)
	click = models.CharField(max_length=200,null=True, blank=True)

	def __str__(self):
		return '[%s]-%s' %(self.containerid.title,self.title)

	class Meta:
		ordering = ['displayorder']

class Eupdate(TimeStampedModel,models.Model):
	title = models.CharField(max_length=100)
	updatetype = models.CharField(max_length=50, choices=SAVE_TYPE)
	action_type = models.CharField(max_length=50, choices=UPDATE_TYPE)
	targettxview = models.ForeignKey(Transactionview,on_delete=models.CASCADE ,related_name='eupdate_params')
	ui_control_field = models.ForeignKey(Component,on_delete=models.CASCADE ,related_name='ui_control',null=True, blank=True) 
	source_ui_field =  models.ForeignKey(Component,on_delete=models.CASCADE ,related_name='source_ui') 
	target_ui_field =  models.ForeignKey(Component,on_delete=models.CASCADE ,related_name='target_ui') 
	filter_clause = models.CharField(max_length=1000)
	transactionview = models.ForeignKey(Transactionview,on_delete=models.CASCADE ,related_name='eupdate_txview_params')
	projectid = models.ForeignKey(Project,on_delete=models.CASCADE ,related_name='eupdate_project_id')


class Epost(TimeStampedModel,models.Model):
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=500,null=True, blank=True)
	source_tx_view = models.ForeignKey(Transactionview,on_delete=models.SET_NULL,related_name='epost_src_txview',null=True, blank=True)
	target_tx_view = models.ForeignKey(Transactionview,on_delete=models.SET_NULL,related_name='epost_target_txview',null=True, blank=True)
	is_active = models.BooleanField(default=False)
	based_on_container =  models.ForeignKey(Container,on_delete=models.SET_NULL,null=True, blank=True)
	ui_control_field = models.ForeignKey(Component,on_delete=models.SET_NULL,null=True, blank=True)
	projectid = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='epost_projectid')

	def __str__(self):
		return self.title

class EpostMapField(TimeStampedModel,models.Model):
	epost = models.ForeignKey(Epost,on_delete=models.CASCADE)
	source_ui_field =  models.ForeignKey(Component,on_delete=models.SET_NULL ,related_name='epost_source_field',null=True, blank=True) 
	target_ui_field =  models.ForeignKey(Component,on_delete=models.SET_NULL ,related_name='epost_target_field',null=True, blank=True) 
	target_fixed_value = models.CharField(max_length=500,null=True, blank=True)
	is_grid_field = models.BooleanField(default=False)
	control_field =  models.ForeignKey(Component,on_delete=models.SET_NULL ,related_name='epost_control_field',null=True, blank=True) 
	group_field =  models.ForeignKey(Component,on_delete=models.SET_NULL ,related_name='epost_group_field',null=True, blank=True) 
	order_by = models.BigIntegerField(default=0)
	target_row = models.BigIntegerField(default=1)
	
	
	def __str__(self):
		return self.epost

	class Meta:
		unique_together = ["epost", "order_by"]


class FireSql(TimeStampedModel,models.Model):
	transactionview = models.ForeignKey(Transactionview,on_delete=models.CASCADE ,related_name='firesql_txview')
	title = models.CharField(max_length=200)
	slug = models.CharField(max_length=200)
	sql	= models.CharField(max_length=1000)
	
	def __str__(self):
		return self.slug

	class Meta:
		unique_together = ["transactionview", "slug"]

class txnCssutilites(TimeStampedModel,models.Model):
	ionic_header = models.CharField(max_length=100, choices=HEADER_CHOICES,null=True, blank=True)
	header_color = models.CharField(max_length=100, choices=HEADERCOLOR_CHOICES,null=True, blank=True)
	custom_header_title =  models.CharField(max_length=200,null=True, blank=True)
	background =  models.CharField(max_length=100, choices=COLOR_CHOICES,null=True, blank=True)
	header_label_color = models.CharField(max_length=100, choices=LABEL_COLOR_CHOICES,null=True, blank=True,default = 'dark')
	label_color = models.CharField(max_length=100, choices=LABEL_COLOR_CHOICES,null=True, blank=True,default = 'dark')
	transactionview = models.ForeignKey(Transactionview,on_delete=models.CASCADE ,related_name='css_txn')
