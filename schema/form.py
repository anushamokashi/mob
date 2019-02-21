from django import forms
from .models import Db_connections_info
from .models import Db_profile
# our new form
class DbprofileForm(forms.ModelForm):
    class Meta:
        model = Db_connections_info
        fields = ("__all__")
        exclude = ['userid']


class DbForm(forms.ModelForm):
    class Meta:
        model = Db_profile
        fields = ('title','appdb','clientdb',)  
        exclude = ['userid']      