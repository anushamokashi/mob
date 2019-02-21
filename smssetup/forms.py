from django import forms
from .models import SMSServer, SMSAttributes


class SMSServerForm(forms.ModelForm):
    class Meta:
        model = SMSServer
        fields= '__all__'
        exclude = ['db_status']

class SMSAttributesForm(forms.ModelForm):
    class Meta:
        model = SMSAttributes
        fields= '__all__'
        exclude = ['smsserver','db_status']

        # def clean(self):

        #     try:
        #         Solution.objects.get(key=self.cleaned_data['key'], problem=self.problem)
        #     except Solution.DoesNotExist:
        #         pass
        #     else:
        #         raise ValidationError('Solution with this Name already exists for this problem')

        #     # Always return cleaned_data
        #     return cleaned_data