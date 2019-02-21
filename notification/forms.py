from django import forms
from .models import Notification,NotificationConfiguration,NotificationButtons
from django.contrib.auth.forms import AuthenticationForm
from transactionview.models import Transactionview

import json

class NotificationForm(forms.ModelForm):

    class Meta:
        model = Notification
        fields= '__all__'
        exclude = ['creatingJson']

class NotificationConfigurationForm(forms.ModelForm):
    # status_process = forms.ModelChoiceField(queryset=Transactionview.objects.all())

    class Meta:
        model = NotificationConfiguration
        fields= '__all__'
        
    
    def __init__(self, *args, **kwargs):
        views = kwargs.pop('views')
        super(NotificationConfigurationForm, self).__init__(*args, **kwargs)
        
        try:
            if views['type'] == "Message":
                txviewArray = json.loads(views['txview'])
                reportArray = json.loads(views['report'])
                butttonArray = json.loads(views['buttons'])
                mergedArray = txviewArray+reportArray+butttonArray
                self.fields['status_process'] = forms.ChoiceField(choices=[(view['value'], view['title']) for view in mergedArray])

        except Exception as e:
            self.fields['status_process'] = forms.ChoiceField(choices=[(view['value'], view['title']) for view in views])


class NotificationButtonsForm(forms.ModelForm):

    class Meta:
        model = NotificationButtons
        fields= '__all__'
        exclude = ['notification_configuration','notification']


    def __init__(self, *args, **kwargs):
        self.stage = kwargs.pop('stage')
        super(NotificationButtonsForm, self).__init__(*args, **kwargs)
        self.fields['stage'].queryset = self.stage