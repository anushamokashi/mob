# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django_extensions.db.models import TitleSlugDescriptionModel, TimeStampedModel, TitleDescriptionModel
from django.db import models
#from django_extensions.db.fields import AutoSlugField

#from project.models import Project
from django.contrib.auth.models import User

# Create your models here.
# class SmsSenderId(TitleDescriptionModel):

# 	project = models.ForeignKey(Project, blank=True, null=True)

# 	class Meta:
# 		db_table = "action_smssenderid"
# 		verbose_name = "SmsSenderId"
# 		verbose_name_plural = "SmsSenderIds"

# 	def __str__(self):
# 	    return self.title


# class FromEmailIdentifier(TitleDescriptionModel):
# 	project = models.ForeignKey(Project, blank=True,  null=True)

# 	from_email = models.CharField( max_length=255)
		
# 	class Meta:
# 		db_table = "action_fromemailidentifier"
# 		verbose_name = "FromEmailIdentifier"
# 		verbose_name_plural = "FromEmailIdentifiers"

# 	def __str__(self):
# 	    return self.title


# # class Language(TitleSlugDescriptionModel, TimeStampedModel):
# class Language(TitleDescriptionModel, TimeStampedModel):
# 	project = models.ForeignKey(Project, blank=True, null=True)

# 	slug = AutoSlugField(populate_from='title', max_length=255, unique=True)
# 	# history = HistoricalRecords()
	
# 	class Meta:
# 	    verbose_name = "Language"
# 	    verbose_name_plural = "Languages"

# 	def __str__(self):
# 	    return self.title



class WidgetType(TitleSlugDescriptionModel):
	"""ui widget type
	"""
	# history = HistoricalRecords()

	class Meta:
		db_table= "report_widgettype"
		verbose_name = "WidgetType"
		verbose_name_plural = "WidgetTypes"

	def __str__(self):
	    return self.title


class ComponentType(TitleSlugDescriptionModel):
	
    class Meta:
		db_table ="report_componenttype"
		verbose_name = "ComponentType"
		verbose_name_plural = "ComponentTypes"

    def __str__(self):
        return self.title




# class Customer(TitleSlugDescriptionModel, TimeStampedModel):


# 	# contact info
# 	address_line1 = models.CharField( max_length=255, blank=True,null=True)
# 	address_line2 = models.CharField( max_length=255, blank=True,null=True)

# 	city = models.CharField( max_length=255, blank=True,null=True)
# 	zip = models.CharField( max_length=10, blank=True,null=True)
# 	state = models.CharField( max_length=255, blank=True,null=True)
# 	country = models.CharField( max_length=255, blank=True,null=True)

# 	phone1 = models.CharField( max_length=15, blank=True,null=True)
# 	phone2 = models.CharField( max_length=15, blank=True,null=True)
# 	fax = models.CharField( max_length=15, blank=True,null=True)

# 	email = models.CharField( max_length=255, blank=True,null=True)

# 	website_url = models.URLField(max_length=1024, blank=True, null=True)

# 	contact_name = models.CharField( max_length=255, blank=True,null=True)
# 	contact_phone = models.CharField( max_length=15, blank=True,null=True)
# 	contact_email = models.CharField( max_length=255, blank=True,null=True)


# 	user = models.ForeignKey(User, related_name='+')

# 	class Meta:
# 		db_table = "subscription_customer"
# 		verbose_name = "Customer"
# 		verbose_name_plural = "Customers"

# 	def __str__(self):
# 	    return self.title