# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from project.models import Project
from django_extensions.db.models import TimeStampedModel
from rolesetup.models import Role

# Create your models here.
LOGIN_TYPE_CHOICES = (
        ('otp','OTP'),
        ('form','Form'),
        ('bar','Barcode')
)
BGCOLOR_TYPE_CHOICES = (
        ('blue','Blue'),
        ('green','Green'),
        ('red','Red')
)

DB_TYPE_CHOICES = (
        ('new','new'),
		('edited','edited'),
        ('updated','updated'),
		('deleted','deleted')
)

DATA_TYPE_CHOICES = (
        ('integer','Integer'),
		('string','String'),
        ('decimal','Decimal'),
		('date','Date'),
		('datetime','DateTime'),
		('sql','SQL')
)

class Login(TimeStampedModel,models.Model):
	
	title = models.CharField(max_length=100, null=True)
	login_type = models.CharField(max_length=20, choices=LOGIN_TYPE_CHOICES, null=True)
	bgcolor = models.CharField(max_length=250, choices=BGCOLOR_TYPE_CHOICES)
	regeisterion_page = models.BooleanField(default=False)
	logoimg = models.FileField(upload_to = 'static/ionicsrc/images/logo',null=True, blank=True)
	project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
	createpage = models.BooleanField(default=True)

	def __str__(self):
		return self.title

class UserList(TimeStampedModel,models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100,blank=True,null=True)
	mobile_number = models.CharField(max_length=100)
	email_id = models.EmailField(max_length=100)
	password = models.CharField(max_length=100)
	confirm_password = models.CharField(max_length=100)
	is_active = models.BooleanField(default=False)
	role = models.ForeignKey(Role, on_delete=models.CASCADE)
	db_status = models.CharField(max_length=250, choices=DB_TYPE_CHOICES)
	project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

	def __str__(self):
		return self.email_id

	class Meta:
		unique_together = ["project_id", "email_id"]

class GeneralInfo(TimeStampedModel,models.Model):
	key = models.CharField(max_length=100)
	value = models.CharField(max_length=100) 
	db_status = models.CharField(max_length=250, choices=DB_TYPE_CHOICES)
	project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

	def __str__(self):
		return self.key

	class Meta:
		unique_together = ["project_id", "key"]

class EditedUsersList(TimeStampedModel,models.Model):
	user_id = models.CharField(max_length=100)
	user_old_email = models.CharField(max_length=100)
	pid = models.CharField(max_length=100)

	def __str__(self):
		return self.user_old_email

class EditedInfo(TimeStampedModel,models.Model):
	key_id = models.CharField(max_length=100)
	old_key = models.CharField(max_length=100)
	pid = models.CharField(max_length=100)

	def __str__(self):
		return self.old_key






	 