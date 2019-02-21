# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.
from django_extensions.db.models import TimeStampedModel

from django_extensions.db.models import TitleSlugDescriptionModel, \
	TimeStampedModel, TitleDescriptionModel

from project.models import Project


PRINT_ACTION_TYPE_CHOICES  = (
	('Server','Server'),
	('Client','Client')
)
SQL_TYPE_CHOICES = (
	('Nongrid','Nongrid'),
	('Grid','Grid')
)    


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'static/ionicmeta/{0}/mustachehtml/{1}'.format(instance.project.slug,filename)

class PrintFormat(TitleDescriptionModel):
	slug = models.CharField(max_length=100)
	project = models.ForeignKey(Project,on_delete=models.CASCADE)
	action_type = models.CharField(choices=PRINT_ACTION_TYPE_CHOICES,max_length=100)
	htmlfile =  models.FileField(upload_to = user_directory_path)
    
	def __str__(self):
	    return self.title

	class Meta:
		unique_together = ["project", "slug"]

class PrintFormatSQL(models.Model):
	printformat = models.ForeignKey(PrintFormat,on_delete=models.CASCADE)
	sql = models.CharField(max_length=500,blank=True,null=True)
	do = models.PositiveSmallIntegerField(default=0)
	sql_type = models.CharField(choices=SQL_TYPE_CHOICES,max_length=100) 

	class Meta:
		unique_together = ["printformat", "do"]