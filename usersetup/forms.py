from django import forms 
from django.forms import ModelForm
from authentication.models import userprofile
from project.models import Project

class UserProfileForm(ModelForm):
    class Meta:
        model = userprofile
        fields= ("email","first_name","last_name","company","password","mobile_number","is_user") 
        exclude = ['adminuserid']


