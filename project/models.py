# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from authentication.models import userprofile
from schema.models import Db_profile
from django_extensions.db.models import TimeStampedModel

# Create your models here.
PROJECT_TYPE_CHOICES = (
        ('ecommerce','E-Commerce'),
        ('business','Business'),
    )

PROTOCOL_TYPE_CHOICES = (
        ('http://','HTTP'),
        ('https://','HTTPS'),
    )
    
APPLICATION_TYPE_CHOICES = (
    ('android','Android'),
    ('iOS','iOS'),
    ('windows','Windows')
)

DB_TYPE_CHOICES = (
        ('new','new'),
		('edited','edited'),
        ('updated','updated'),
		('deleted','deleted')
)

TIME_TYPE_CHOICES = (
   ('1800000','30 Minutes'),
   ('900000','15 Minutes'),
   ('600000','10 Minutes'),
)

TRACKING_TYPE_CHOICES = (
  ('true','Yes'),
  ('false','No')
)

class Project(TimeStampedModel,models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)    
    ptype = models.CharField(max_length=50, choices=PROJECT_TYPE_CHOICES)
    application_type = models.CharField(max_length=50, choices=APPLICATION_TYPE_CHOICES)
    admin_id = models.ForeignKey(userprofile, on_delete=models.CASCADE)
    prmcolor = models.CharField(max_length=100,null=True, blank=True ,default="#488aff")    
    seccolor = models.CharField(max_length=100,null=True, blank=True,default="#32db64")
    dark = models.CharField(max_length=100,null=True, blank=True,default="#000000")
    slug = models.CharField(max_length=150,null=True, blank=True)
    table_append_by_underscore = models.BooleanField(default=False)
    ismultitenant = models.BooleanField(default=False)
    imei_based_login = models.BooleanField(default=False)
    # projectid = models.CharField(max_length=100)
	
    def __str__(self):
        return self.title

class Projectwiseusersetup(TimeStampedModel,models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    userid = models.ForeignKey(userprofile, on_delete=models.CASCADE)
    db_profileid = models.ForeignKey(Db_profile, on_delete=models.CASCADE)
    setasdefaultproject = models.BooleanField(default=False)

    def __str__(self):
        return self.project_id.title

class IonicProjectConfig(TimeStampedModel,models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    itype = models.CharField(max_length=100,null=True, blank=True)
    platform = models.CharField(max_length=100,null=True, blank=True)
    plugin = models.CharField(max_length=200,null=True, blank=True)
    providers = models.CharField(max_length=200,null=True, blank=True)
    

class IonicImages(TimeStampedModel,models.Model):
    splashimg = models.FileField(upload_to = 'static/ionicsrc/images/splash',null=True, blank=True)
    iconimg =   models.FileField(upload_to = 'static/ionicsrc/images/icon',null=True, blank=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

class IonicFonts(TimeStampedModel,models.Model):
    fontname = models.CharField(max_length=100,null=True, blank=True)
    fontfile =   models.FileField(upload_to = 'static/ionicsrc/images/fonts',null=True, blank=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

class IonicServices(TimeStampedModel,models.Model):
    protocol = models.CharField(max_length=50,choices=PROTOCOL_TYPE_CHOICES)
    host = models.CharField(max_length=200,null=True, blank=True)
    port = models.CharField(max_length=200,null=True, blank=True)
    context = models.CharField(max_length=200,null=True, blank=True)
    serviceurl = models.CharField(max_length=200,null=True, blank=True)
    basicid = models.CharField(max_length=100,null=True, blank=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

class IonicNotification(TimeStampedModel,models.Model):
    apikey = models.CharField(max_length=200,null=True, blank=True)
    senderid = models.CharField(max_length=200,null=True, blank=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)     

class GoogleAPISetup(TimeStampedModel,models.Model):
    apikey = models.CharField(max_length=200,null=True, blank=True)
    clientid = models.CharField(max_length=200,null=True, blank=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

class GeolocationSetup(TimeStampedModel,models.Model):
    tracking = models.CharField(max_length=50, choices=TRACKING_TYPE_CHOICES)
    time_interval = models.CharField(max_length=50, choices=TIME_TYPE_CHOICES)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

class EmailConfiguration(TimeStampedModel,models.Model):
    server = models.CharField(max_length=50,null=True,blank=True)
    port = models.BigIntegerField(null=True,blank=True)
    email_id = models.CharField(max_length=50,null=True,blank=True)
    pwd = models.CharField(max_length=50,null=True,blank=True)
    Domain = models.CharField(max_length=50,null=True,blank=True)
    default_email_id = models.CharField(max_length=200,null=True, blank=True)
    protocol = models.CharField(max_length=200,null=True, blank=True)
    is_aunthentication_req  = models.BooleanField(default=False)
    support_tls = models.BooleanField(default=False)
    db_status = models.CharField(max_length=250, choices=DB_TYPE_CHOICES)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)   

