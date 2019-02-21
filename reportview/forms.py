from django.forms import ModelForm

from django.forms import formset_factory
from django import forms
from .models import Report,ReportParamField,ReportField,Query,ReportGrouping,Query,ReportAction,ReportPrintFormatAction,ReportPDF,ReportCSV,ReportHTML,ReportSubmit,ReportEpostMap,Payment,NewAction
from transactionview.models import Transactionview,Component
    
from rest_framework import  viewsets

from django.forms import fields, models, formsets, widgets

from django.db.models import Q
from django.forms.widgets import HiddenInput
import re

class CleanUniqueField:
    
    def __init__(self, form, name, value):
       
        self.form = form
        self.name = name
        self.value = value

    def validate(self):
        

        queryset = self.form._meta.model.objects
        if self.form.instance.pk:
            queryset = queryset.exclude(pk=self.form.instance.pk)

        try:
            queryset.get(**{self.name: self.value})
        except self.form._meta.model.DoesNotExist:
            pass
            
        else:
            print "asf"
            raise forms.ValidationError(
                u'The %s is already exists.' % self.name)

    


class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields='__all__'
        exclude=['project','identifiers']


class ReportParamFieldForm(ModelForm):
    class Meta:
         model =ReportParamField
         fields = '__all__'
         exclude = ['report'] 
         
    def __init__(self,  *args, **kwargs):
        super(ReportParamFieldForm, self).__init__(*args, **kwargs)
        self.fields['display_order'].required =False
        

class ReportFieldForm(ModelForm):
    class Meta:
        model = ReportField        
        fields = ('__all__')
        exclude = ['report']
        
    def __init__(self,  *args, **kwargs):
        super(ReportFieldForm, self).__init__(*args, **kwargs)
        self.fields['display_order'].required =False


class QueryForm(ModelForm):
    class Meta:
        model=Query
        fields = ['title', 'description','report','is_main_query','join_type','sql']
        exclude = ['report','slug']


class ReportGroupingForm(ModelForm):
    class Meta:
        model = ReportGrouping
        fields ="__all__"
        exclude = ['report']   
        
ACTION_TYPE_CHOICES=(
        ('print_format','Print_Format'),
        ('pdf','pdf'),
        ('csv','csv'),
        ('html','html'),
        ('submit','Submit'),
        ('payment','Payment'),
        ('new','New')
)

class ReportActionForm(forms.ModelForm):
    class Meta:
        model=ReportAction
        fields="__all__"
        exclude = ['action_type','report','title','description']

    report_action = forms.MultipleChoiceField(choices=ACTION_TYPE_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class': 'flat-red'}))


class ReportPrintFormatActionForm(ModelForm):
    class Meta:
        model= ReportPrintFormatAction 
        fields=['pfconfig']
        exclude=['report_action']     

class ReportPDFForm(ModelForm):
    class Meta:
        model=ReportPDF
        fields="__all__"

class ReportCSVForm(ModelForm):
    class Meta:
        model=ReportCSV
        fields="__all__"



class ReportHTMLForm(ModelForm):
    class Meta:
        model=ReportHTML
        fields="__all__"  

class PaymentForm(ModelForm):
    class Meta:
        model=Payment
        fields="__all__"
        exclude = ['report','report_action']       

class NewActionForm(ModelForm):
    class Meta:
        model=NewAction
        fields="__all__"
        exclude = ['report','report_action']                                    
    
class ReportSubmitForm(ModelForm):
    class Meta:
        model=ReportSubmit
        fields="__all__"
        exclude = ['report','report_action']

    def __init__(self, *args, **kwargs):
        self.pid = kwargs.pop('pid')
        super(ReportSubmitForm, self).__init__(*args, **kwargs)
        view_list = Transactionview.objects.filter(projectid_id = self.pid)
        self.fields['epost_target'].queryset = view_list

class ReportEpostMapForm(ModelForm):
    class Meta:
        model = ReportEpostMap
        fields = '__all__'
        exclude = ['reportsubmit']

    def __init__(self, *args, **kwargs):
        self.reportid = kwargs.pop('reportid')
        self.tx = kwargs.pop('tx')
        super(ReportEpostMapForm, self).__init__(*args, **kwargs)
        view_list = ReportField.objects.filter(report_id = self.reportid)
        self.fields['source_ui_field'].queryset = view_list
        #print("%s txview" %(self.tx))
        if self.tx:
            self.fields['target_ui_field'].queryset = Component.objects.filter(transactionviewid_id = self.tx)
        else:
            self.fields['target_ui_field'].queryset = Component.objects.none()
