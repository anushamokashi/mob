# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from transactionview.models import Transactionview,Component
from django_extensions.db.models import TimeStampedModel
from printformat.models import PrintFormat

# Create your models here.
SORT_TYPE_CHOICES = (
	('ascending','Ascending'),
	('descending','Descending'),
	)

	
class Actions(TimeStampedModel,models.Model):
	actiontype = models.CharField(max_length=50,null=True, blank=True)
	displayorder = models.BigIntegerField(null=True, blank=True)
	transactionviewid = models.ForeignKey(Transactionview,blank=True, null=True,on_delete=models.SET_NULL,related_name='actions_type')	

class SaveAction(TimeStampedModel,models.Model):
	title = models.CharField(max_length=100,null=True,blank=True)
	expression = models.TextField(null=True,blank=True)	
	expression_postfix = models.TextField(null = True,blank=True)
	ui_control_field = models.ForeignKey(Component,on_delete=models.CASCADE ,related_name='save_ui',null = True,blank=True)
	iconcls = models.CharField(max_length=50,null=True, blank=True)
	actiontype = models.ForeignKey(Actions,on_delete =models.CASCADE,related_name = 'save_action')
	transactionview = models.ForeignKey(Transactionview,on_delete=models.CASCADE ,related_name='save_trans')


class DeleteAction(TimeStampedModel,models.Model):
	title = models.CharField(max_length=100,null=True,blank=True)
	expression = models.TextField(null=True,blank=True)	
	expression_postfix = models.TextField(null = True,blank=True)
	ui_control_field = models.ForeignKey(Component,on_delete=models.CASCADE ,related_name='delete_ui',null = True,blank=True) 
	iconcls = models.CharField(max_length=50,null=True, blank=True)
	actiontype = models.ForeignKey(Actions,on_delete =models.CASCADE,related_name = 'delete_action')
	transactionview = models.ForeignKey(Transactionview,on_delete=models.CASCADE ,related_name='delete_trans')


class CancelAction(TimeStampedModel,models.Model):
	title = models.CharField(max_length=100,null=True,blank=True)
	expression = models.TextField(null=True,blank=True)	
	expression_postfix = models.TextField(null = True,blank=True)
	ui_control_field = models.ForeignKey(Component,on_delete=models.CASCADE ,related_name='Cancel_ui',null = True,blank=True) 
	iconcls = models.CharField(max_length=50,null=True, blank=True)
	actiontype = models.ForeignKey(Actions,on_delete =models.CASCADE,related_name = 'Cancel_action')
	transactionview = models.ForeignKey(Transactionview,on_delete=models.CASCADE ,related_name='Cancel_trans')		


class NewAction(TimeStampedModel,models.Model):
	title = models.CharField(max_length=100,null=True,blank=True)
	expression = models.TextField(null=True,blank=True)	
	expression_postfix = models.TextField(null = True,blank=True)
	ui_control_field = models.ForeignKey(Component,on_delete=models.CASCADE ,related_name='new_ui',null = True,blank=True) 
	iconcls = models.CharField(max_length=50,null=True, blank=True)
	actiontype = models.ForeignKey(Actions,on_delete =models.CASCADE,related_name = 'new_action')
	transactionview = models.ForeignKey(Transactionview,on_delete=models.CASCADE ,related_name='new_trans')

class SearchAction(TimeStampedModel,models.Model):
	title = models.CharField(max_length=100,null=True,blank=True)
	sql = models.TextField(null = True,blank=True)
	param_fields = models.CharField(max_length=500,null=True,blank=True)
	sort_type = models.CharField(choices=SORT_TYPE_CHOICES,max_length=50,null=True, blank=True)
	sort_field =  models.CharField( max_length=100, blank=True,null=True)
	search_field =  models.CharField( max_length=100)
	chunk_size =  models.PositiveSmallIntegerField(null = True,blank=True)
	page_size =  models.PositiveSmallIntegerField(null = True,blank=True)
	copy_tx_view = models.BooleanField(default=False)
	iconcls = models.CharField(max_length=50,null=True, blank=True)
	actiontype = models.ForeignKey(Actions,on_delete =models.CASCADE,related_name = 'search_action')
	transactionview = models.ForeignKey(Transactionview,on_delete=models.CASCADE ,related_name='search_trans')
				
	    

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'static/ionicmeta/{0}/{1}/{2}'.format(instance.transactionview.projectid.slug,instance.transactionview.identifiers, filename)

class TxnPrintFormatAction(TimeStampedModel,models.Model):

	pfconfig = models.ForeignKey(PrintFormat,on_delete=models.CASCADE)
	iconcls = models.CharField(max_length=50,null=True, blank=True)
	expression = models.TextField(null=True,blank=True)	
	ui_control_field = models.ForeignKey(Component,on_delete=models.CASCADE ,related_name='txnprintfomat_ui',null = True,blank=True)
	actiontype = models.ForeignKey(Actions,on_delete =models.CASCADE,related_name = 'txnprintfomat_action')
	transactionview = models.ForeignKey(Transactionview,on_delete=models.CASCADE ,related_name='txnprintfomat_trans')

class GoogleSyncAction(TimeStampedModel,models.Model):
	title = models.CharField(max_length=100,null=True,blank=True)
	iconcls = models.CharField(max_length=50,null=True, blank=True)
	expression = models.TextField(null=True,blank=True)	
	ui_control_field = models.ForeignKey(Component,on_delete=models.CASCADE ,related_name='googlesync_ui',null = True,blank=True)
	actiontype = models.ForeignKey(Actions,on_delete =models.CASCADE,related_name = 'googlesync_action')
	transactionview = models.ForeignKey(Transactionview,on_delete=models.CASCADE ,related_name='googlesync_trans')
