from django import forms 
from django.forms import ModelForm
from .models import Login,UserList,GeneralInfo
    
class LoginForm(ModelForm):
    class Meta:
        model = Login
        fields = ['title','login_type','bgcolor','regeisterion_page','logoimg']
        exclude = ['project_id','createpage']


class UserListForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value = True))
    confirm_password = forms.CharField(widget=forms.PasswordInput(render_value = True))
    class Meta:
        model = UserList
        fields = ['first_name','last_name','mobile_number','email_id','password','confirm_password','is_active','role']
        exclude = ['project_id']


class GeneralInfoForm(ModelForm):
    class Meta:
        model = GeneralInfo
        fields = ['key','value']
        exclude = ['project_id','db_status']
        