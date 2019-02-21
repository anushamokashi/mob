
from django import forms
from .models import Transaction,Txtabledetails,Txtablecomponentdetails, enumtitle, enumkeyvalue
from django.contrib.auth.forms import AuthenticationForm

class UserTransForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields= '__all__'
        exclude = ['projectid']

class TableDetailsform(forms.ModelForm):

	class Meta:
		model = Txtabledetails
		fields= ("title","tablename","description","relationshiptype","transactionid","projectid","db_type")
		exclude = ['isprimary','table_slug','parent','status','user']


class TableComponentform(forms.ModelForm):

	class Meta:
		model = Txtablecomponentdetails
		fields =("title","columnname","datatype","maxlength","isdbfield","isnull","no_of_decimal_digits","enum","db_type")
		exclude = ['txtabledetailid','field_slug','is_system_component','status','user']	

class EnumTitleform(forms.ModelForm):

	class Meta:
		model = enumtitle
		fields =("enum_title","description")
		exclude = ['project_id']

class EnumKeyValueform(forms.ModelForm):

	class Meta:
		model = enumkeyvalue
		fields =("key","value")
		exclude = ['enum_title_fk']