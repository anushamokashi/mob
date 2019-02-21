# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from authentication.models import userprofile
from django_extensions.db.models import TimeStampedModel

# Create your models here.
VENDOR_CHOICES =(
        ('mysql','Mysql'),
        ('oracle','Oracle'),
        ('sqlite','Sqlite'),
        ('mongodb','Mongodb'),
		)
class Db_connections_info(TimeStampedModel,models.Model):
	title = models.CharField(max_length=100)
	dbname = models.CharField(max_length=100,blank=True, null=True)
	username = models.CharField(max_length=100,blank=True, null=True)
	password = models.CharField(max_length=100,blank=True, null=True)
	host = models.CharField(max_length=100,blank=True, null=True)
	port = models.CharField(max_length=100,blank=True, null=True)	
	vendor = models.CharField(max_length=100, choices=VENDOR_CHOICES)
	userid = models.ForeignKey(userprofile, on_delete=models.CASCADE)
	sid = models.CharField(max_length=100,blank=True, null=True)

	def __str__(self):
		return self.title


class Db_profile(TimeStampedModel,models.Model):

	title = models.CharField(max_length=100)
	appdb = models.ForeignKey(Db_connections_info, on_delete=models.CASCADE,related_name='+')
	userid	= models.ForeignKey(userprofile, on_delete=models.CASCADE)
	clientdb = models.ForeignKey(Db_connections_info, on_delete=models.CASCADE,blank=True, null=True)
	
	def __str__(self):
		return self.title


