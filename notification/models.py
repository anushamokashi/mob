# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django_extensions.db.models import TimeStampedModel

from rolesetup.models import Role
from project.models import Project
import datetime
from transactionview.models import Transactionview,Component


ACTION_TYPE_CHOICES = (
    ('Buttons','Buttons'),
	('Message','Message'),
	)




# Create your models here.
class Notification(TimeStampedModel,models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500,null=True, blank=True)
    projectid = models.ForeignKey(Project,on_delete=models.CASCADE)
    creatingJson = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

    class Meta:
		unique_together = ["title", "projectid"]


class NotificationConfiguration(TimeStampedModel,models.Model):
    notification = models.ForeignKey(Notification,on_delete=models.CASCADE)
    stage_name = models.CharField(max_length=100)
    role = models.ForeignKey(Role,on_delete=models.SET_NULL,null=True, blank=True)
    status_process_type = models.CharField(max_length=50, choices=ACTION_TYPE_CHOICES,null=True,blank=True)
    status_process = models.CharField(max_length=100,null=True, blank=True)
    choosed_status_process = models.CharField(max_length=100,null=True, blank=True)
    action_event = models.CharField(max_length=100,null=True,blank=True)
    message =  models.CharField(max_length=500,null=True,blank=True) 
    from_date = models.ForeignKey(Component,on_delete=models.SET_NULL,null=True, blank=True,related_name='from_date_field')
    to_date = models.ForeignKey(Component,on_delete=models.SET_NULL,null=True, blank=True,related_name='to_date_field')
    basicid_field = models.ForeignKey(Component,on_delete=models.SET_NULL,null=True, blank=True,related_name='to_basicid_field')
    user_field = models.ForeignKey(Component,on_delete=models.SET_NULL,null=True, blank=True,related_name='to_user_field')
   
    def __str__(self):
        return self.stage_name

    class Meta:
		unique_together = ["stage_name", "notification"]

class NotificationButtons(TimeStampedModel,models.Model):
    notification_configuration = models.ForeignKey(NotificationConfiguration,on_delete=models.CASCADE,related_name='current_stage')
    button_name = models.CharField(max_length=100)
    notification = models.ForeignKey(Notification,on_delete=models.CASCADE)
    stage = models.ForeignKey(NotificationConfiguration,on_delete=models.SET_NULL,null=True, blank=True,related_name='referred_stage')
    
    def __str__(self):
		return self.button_name

    class Meta:
		unique_together = ["notification_configuration", "button_name"]