# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from project.models import Project
from django_extensions.db.models import TimeStampedModel
from transactionview.models import Transactionview
from reportview.models import Report

# Create your models here.
class Role(TimeStampedModel,models.Model):
    rolename = models.CharField(max_length=100)
    description = models.CharField(max_length=200,blank=True,null=True)
    projectid = models.ForeignKey(Project,on_delete=models.CASCADE)
    def __str__(self):
        return self.rolename
    class Meta:
        unique_together = ["rolename", "projectid"]
    
class ViewsForRole(TimeStampedModel,models.Model):
    role = models.ForeignKey(Role,on_delete=models.CASCADE)
    txview = models.CharField(max_length=100,blank=True,null=True)
    reportview = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.role.rolename