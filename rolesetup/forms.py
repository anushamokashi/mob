from django import forms
from .models import Role, ViewsForRole


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields= '__all__'
        # fields = ['rolename','projectid']
        # exclude = ['description']

class RoleViewForm(forms.ModelForm):
    class Meta:
        model = ViewsForRole
        fields= '__all__'