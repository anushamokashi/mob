from django import forms
from django.forms import ModelForm
from .models import Homepage, Menu,RootPage,SubMenuConfig
from transactionview.models import Transactionview
from reportview.models import Report


class HomepageForm(ModelForm):
    class Meta:
        model = Homepage
        fields = ['menutype','column','sidemenu']
        exclude = ['project_id']

class MenuForm(ModelForm):
	class Meta:
		model = Menu
		fields = ("__all__")
		exclude = ['homepageid','createpage']

	def __init__(self, *args, **kwargs):
		pid = kwargs.pop('pid')
		super(MenuForm, self).__init__(*args, **kwargs)
		txview = Transactionview.objects.filter(projectid_id = pid)
		self.fields['transactionview'].queryset = txview
		repview = Report.objects.filter(project_id = pid)
		self.fields['reportview'].queryset = repview

class RootPageForm(ModelForm):
    class Meta:
        model = RootPage
        fields = ("__all__")
        exclude = ['project']

    def __init__(self, *args, **kwargs):
        try:
            homeid = kwargs.pop('homeid')
            super(RootPageForm, self).__init__(*args, **kwargs)
            menu = Menu.objects.filter(homepageid_id = homeid)
            self.fields['pageValue'].queryset = menu
        except Exception as e:
            print e


class SubMenuConfigForm(ModelForm):
    class Meta:
        model = SubMenuConfig
        fields = ("__all__")
        exclude = ['homepageid','project']

    def __init__(self, *args, **kwargs):
        try:
            homeid = kwargs.pop('homeid')
            super(SubMenuConfigForm, self).__init__(*args, **kwargs)
            menu = Menu.objects.filter(homepageid_id = homeid)
            self.fields['pageValue'].queryset = menu
        except Exception as e:
            print e
