# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

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

class SMSServer(TimeStampedModel,models.Model):
    server = models.CharField(max_length=200)
    port = models.BigIntegerField()
    url = models.CharField(max_length=200,blank=True,null=True)
    db_status = models.CharField(max_length=250, choices=DB_TYPE_CHOICES)
    use_proxy = models.BooleanField(default=False)
    projectid = models.ForeignKey(Project,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.server
    
class SMSAttributes(TimeStampedModel,models.Model):
    smsserver = models.ForeignKey(SMSServer,on_delete=models.CASCADE)
    key = models.CharField(max_length=500)
    value = models.CharField(max_length=100)
    do = models.BigIntegerField(blank=True,null=True)
    

    def __str__(self):
        return self.key

    class Meta:
        unique_together = [ "key","smsserver"]