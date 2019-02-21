
from django import forms
from .models import Actions,SaveAction,NewAction,CancelAction,DeleteAction,SearchAction,TxnPrintFormatAction,GoogleSyncAction
from transactionview.models import Component


ACTION_TYPE_CHOICES=(
	('Cancel','Cancel'),
	('Delete','Delete'),
	('New','New'),
	('Save','Save'),
	('Search','Search'),
	('PrintFormat','PrintFormat'),
	('GoogleSync','GoogleSync')
	)

ICON_TYPE_CHOICES =(
	('','---------'),
	('add','Add'),
	('albums','Albums'),
	('logo-android','Android'),
	('logo-angular','Angular'),
	('aperture','Aperture'),
	('logo-apple','Apple'),
	('apps','Apps'),
	('archive','Archive'),
	('barcode','Barcode'),
	('basket','Basket'),
	('bicycle','Bicycle'),
	('logo-bitcoin','Bitcoin'),
	('bonfire','Bonefire'),
	('book','Book'),
	('bookmark','Bookmark'),
	('bookmarks','Bookmarks'),
	('briefcase','Briefcase'),
	('calculator','Calculator'),
	('calendar','Calendar'),
	('card','Card'),
	('cash','Cash'),
	('clock','Clock'),
	('cloud','Cloud'),
	('close-circle','Close-circle'),
	('codepen','Codepen'),
	('construct','Construct'),
	('contact','Contact'),
	('copy','Copy'),
	('create','Create'),
	('cube','Cube'),
	('desktop','Desktop'),
	('disc','Disc'),
	('document','Document'),
	('done-all','Done-all'),
	('flame','Flame'),
	('flower','Flower'),
	('floder','Floder'),
	('globe','Globe'),
	('grid','Grid'),
	('help-buoy','Help-Buoy'),
	('home','Home'),
	('images','Images'),
	('information-circle','Information-Circle'),
	('keypad','Keypad'),
	('laptop','Laptop'),
	('list-box','List-Box'),
	('lock','Lock'),
	('logo-pinterest','Pinterest'),
	('nuclear','Nuclear'),
	('pie','Pie'),
	('print','Print'),
	('stats','Stats'),
	('stopwatch','Stopwatch'),
	('search','Search'),
	('sync','Sync'),
	('tennisball','Tennisball'),
    ('thumbs-up','Thumbs-up'),
    ('trash','Trash')
		)

class ActionsForm(forms.ModelForm):               
	class Meta:
		model = Actions
		fields = '__all__'
		exclude = ['actiontype','transactionviewid']

	actiontype = forms.MultipleChoiceField(choices=ACTION_TYPE_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class': 'flat-red'}))
	
class SaveActionForm(forms.ModelForm):
	iconcls = forms.ChoiceField(choices = ICON_TYPE_CHOICES)
	class Meta:
		model = SaveAction
		fields = '__all__'
		exclude =['actiontype','transactionview']

	def __init__(self, *args, **kwargs):
		viewid = kwargs.pop('viewid')
		super(SaveActionForm, self).__init__(*args, **kwargs)
		component = Component.objects.filter(transactionviewid_id = viewid)
		self.fields['ui_control_field'].queryset = component
		self.fields['ui_control_field'].required = False	

class NewActionForm(forms.ModelForm):
	iconcls = forms.ChoiceField(choices = ICON_TYPE_CHOICES)
	class Meta:
		model = NewAction
		fields = '__all__'
		exclude =['actiontype','transactionview']

	def __init__(self, *args, **kwargs):
		viewid = kwargs.pop('viewid')
		super(NewActionForm, self).__init__(*args, **kwargs)
		component = Component.objects.filter(transactionviewid_id = viewid)
		self.fields['ui_control_field'].queryset = component
		self.fields['ui_control_field'].required = False 

class CancelActionForm(forms.ModelForm):
	iconcls = forms.ChoiceField(choices = ICON_TYPE_CHOICES)
	class Meta:
		model = CancelAction
		fields = '__all__'
		exclude =['actiontype','transactionview']

	def __init__(self, *args, **kwargs):
		viewid = kwargs.pop('viewid')
		super(CancelActionForm, self).__init__(*args, **kwargs)
		component = Component.objects.filter(transactionviewid_id = viewid)
		self.fields['ui_control_field'].queryset = component	
		self.fields['ui_control_field'].required = False		

class DeleteActionForm(forms.ModelForm):
	iconcls = forms.ChoiceField(choices = ICON_TYPE_CHOICES)
	class Meta:
		model = DeleteAction
		fields = '__all__'
		exclude =['actiontype','transactionview']

	def __init__(self, *args, **kwargs):
		viewid = kwargs.pop('viewid')
		super(DeleteActionForm, self).__init__(*args, **kwargs)
		component = Component.objects.filter(transactionviewid_id = viewid)
		self.fields['ui_control_field'].queryset = component
		self.fields['ui_control_field'].required = False			

class SearchActionform(forms.ModelForm):
	iconcls = forms.ChoiceField(choices = ICON_TYPE_CHOICES)
	class Meta:
		model = SearchAction
		fields ='__all__'
		exclude =['actiontype','transactionview']

class TxnPrintFormatActionForm(forms.ModelForm):
	iconcls = forms.ChoiceField(choices = ICON_TYPE_CHOICES)
	class Meta:
		model = TxnPrintFormatAction
		fields = '__all__'
		exclude = ['actiontype','transactionview']

	def __init__(self, *args, **kwargs):
		viewid = kwargs.pop('viewid')
		super(TxnPrintFormatActionForm, self).__init__(*args, **kwargs)
		component = Component.objects.filter(transactionviewid_id = viewid)
		self.fields['ui_control_field'].queryset = component
		self.fields['ui_control_field'].required = False 
	

class GoogleSyncActionform(forms.ModelForm):
	iconcls = forms.ChoiceField(choices = ICON_TYPE_CHOICES)
	class Meta:
		model = GoogleSyncAction
		fields ='__all__'
		exclude =['actiontype','transactionview']

	def __init__(self, *args, **kwargs):
		viewid = kwargs.pop('viewid')
		super(GoogleSyncActionform, self).__init__(*args, **kwargs)
		component = Component.objects.filter(transactionviewid_id = viewid)
		self.fields['ui_control_field'].queryset = component
		self.fields['ui_control_field'].required = False



