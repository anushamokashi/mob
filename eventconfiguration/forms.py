from django import forms 
from django.forms import ModelForm
from .models import TxnMappingForEvent

    
class TxnMappingForEventForm(ModelForm):
    class Meta:
        model = TxnMappingForEvent
        fields = ['title','description','slug','txview','event_title','event_desc','event_location','event_start_day','event_start_time','event_end_day','event_end_time','email_reminder','popup_reminder']
        exclude = ['project',]