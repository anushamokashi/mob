from django import forms 
from django.forms import ModelForm
from .models import Project, Projectwiseusersetup,IonicProjectConfig,IonicImages,IonicFonts,IonicServices,IonicNotification,EmailConfiguration,GoogleAPISetup,GeolocationSetup


    
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title','description','ptype','application_type','table_append_by_underscore','ismultitenant','imei_based_login']
        exclude = ['admin_id','prmcolor','seccolor']
        
class ProjectwiseusersetupForm(ModelForm):
    class Meta:
        model = Projectwiseusersetup
        fields = ['project_id','userid','db_profileid','setasdefaultproject']

class IonicProjectConfigForm(ModelForm):
    class Meta:
        model = IonicProjectConfig
        fields = ['project_id','itype','platform','plugin','providers']

class IonicImagesForm(ModelForm):
    class Meta:
        model = IonicImages
        fields =['splashimg','iconimg']
        exclude = ['project_id']

class IonicFontsForm(ModelForm):
    class Meta:
        model = IonicFonts
        fields =['fontname','fontfile']
        exclude = ['project_id']

class IonicServicesForm(ModelForm):
    class Meta:
        model = IonicServices
        fields =['protocol','host','port','context','basicid']
        exclude = ['serviceurl','project_id']

class IonicNotificationForm(ModelForm):
    class Meta:
        model = IonicNotification
        fields =['apikey','senderid']
        exclude = ['project_id']

class GoogleAPISetupForm(ModelForm):
    class Meta:
        model = GoogleAPISetup
        fields =['apikey','clientid']
        exclude = ['project_id']

class GeolocationSetupForm(ModelForm):
    class Meta:
        model = GeolocationSetup
        fields ='__all__'
        exclude = ['project_id']

class EmailConfigurationForm(ModelForm):
    class Meta:
        model = EmailConfiguration
        fields ='__all__'
        exclude = ['project_id','db_status']        