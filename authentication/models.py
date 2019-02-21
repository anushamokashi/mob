# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel

# Create your models here.

class userprofile(TimeStampedModel,models.Model):

    email = models.EmailField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    mobile_number = models.BigIntegerField()
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    adminuserid =  models.BigIntegerField()

    def __str__(self):
	    return self.email 

    def __unicode__(self):
        return self.email   
    