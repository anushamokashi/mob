from django.forms import ModelForm

from django.forms import formset_factory
from django import forms
from .models import PrintFormat,PrintFormatSQL

class PrintFormatForm(ModelForm):
    class Meta:
        model= PrintFormat 
        fields=['title','action_type','htmlfile']
        exclude=['project','slug']     

class PrintFormatSQLForm(ModelForm):
    class Meta:
        model= PrintFormatSQL 
        fields=['sql','do','sql_type']
        exclude=['printformat']    