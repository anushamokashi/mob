
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import userprofile
from django.contrib.auth.forms import AuthenticationForm

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = userprofile
        fields= ("email","first_name","last_name","company","password","mobile_number","is_admin","is_user") 
        exclude = ['adminuserid']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].reqiured = True	