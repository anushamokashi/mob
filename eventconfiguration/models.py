# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django_extensions.db.models import TimeStampedModel

from django_extensions.db.models import TitleSlugDescriptionModel, \
	TimeStampedModel, TitleDescriptionModel

from project.models import Project
from transactionview.models import Transactionview,Component


class TxnMappingForEvent(TitleDescriptionModel):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    slug = models.CharField(max_length=150,null=True,blank=True)
    txview = models.ForeignKey(Transactionview,on_delete=models.CASCADE)
    event_title = models.ForeignKey(Component,on_delete=models.CASCADE,related_name='event_title')
    event_desc = models.ForeignKey(Component,on_delete=models.SET_NULL,null=True,blank=True,related_name='event_desc')
    event_location = models.ForeignKey(Component,on_delete=models.SET_NULL,null=True,blank=True,related_name='event_location')
    event_start_day = models.ForeignKey(Component,on_delete=models.CASCADE,related_name='event_start_day')
    event_start_time = models.ForeignKey(Component,on_delete=models.CASCADE,related_name='event_start_time')
    event_end_day = models.ForeignKey(Component,on_delete=models.SET_NULL,null=True,blank=True,related_name='event_end_day')
    event_end_time = models.ForeignKey(Component,on_delete=models.SET_NULL,null=True,blank=True,related_name='event_end_time')
    email_reminder = models.CharField(max_length=20,null=True,blank=True)
    popup_reminder = models.CharField(max_length=20,null=True,blank=True)
    
    def __str__(self):
	    return self.title

