# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from project.models import Project
from django_extensions.db.models import TimeStampedModel

# Create your models here.


DB_TYPE_CHOICES = (
	('new','new'),
	('edited','edited'),
	('updated','updated'),
	('deleted','deleted')
)



class SyncTableDetails(TimeStampedModel,models.Model):
	sourcetable = models.CharField(max_length=200,blank= True,null = True)
	targettable = models.CharField(max_length=200,blank= True,null = True)
	url = models.CharField(max_length=200,blank= True,null = True)
	dependson = models.CharField(max_length=200,blank= True,null = True)
	orderno = models.BigIntegerField(null=True, blank=True)
	wherecon = models.CharField(max_length=500,blank= True,null = True)
	projectid = models.ForeignKey(Project,on_delete=models.CASCADE ,related_name='syncproject')
	db_status = models.CharField(max_length=250, choices=DB_TYPE_CHOICES)

	def __str__(self):
		return self.sourcetable
	
	class Meta:
		unique_together = ["sourcetable","targettable","projectid"]

class SyncColumnDetails(TimeStampedModel,models.Model):
	sourcefield = models.CharField(max_length=200,blank= True,null = True)
	targetfield = models.CharField(max_length=200,blank= True,null = True)
	shortid = models.CharField(max_length=500,blank= True,null = True)
	syncTable = models.ForeignKey(SyncTableDetails,on_delete=models.CASCADE ,related_name='synccolumn')
	db_status = models.CharField(max_length=250, choices=DB_TYPE_CHOICES)
	projectid = models.ForeignKey(Project,on_delete=models.CASCADE)

	def __str__(self):
		return self.sourcefield
	
	class Meta:
		unique_together = ["syncTable","sourcefield","targetfield","projectid"]



class EditedTableMap(TimeStampedModel,models.Model):
	synctable_id = models.CharField(max_length=100)
	old_sourcetable = models.CharField(max_length=100)
	old_targettable = models.CharField(max_length=100)
	pid = models.CharField(max_length=100)

	def __str__(self):
		return self.old_sourcetable

class EditedColumnMap(TimeStampedModel,models.Model):
	synccolumn_id = models.CharField(max_length=100)
	synctable_id = models.CharField(max_length=100)
	old_sourcefield = models.CharField(max_length=100)
	old_targetfield = models.CharField(max_length=100)
	pid = models.CharField(max_length=100)

	def __str__(self):
		return self.old_sourcefield
