
from django import forms
from django.forms import BaseFormSet
from .models import Transactionview,Container,Component,Eupdate,Epost,EpostMapField,FireSql,txnCssutilites
from transaction.models import Txtabledetails
from django.core.exceptions import ValidationError
from django.conf import settings


ACTION_TYPE_CHOICES=(
	('cancel','Cancel'),
	('delete','Delete'),
	('new','New'),
	('save','Save'),
	('search','Search')
	)

class TransactionviewForm(forms.ModelForm):
	class Meta:
		model = Transactionview
		fields =("title","description","viewtype","savetype","expression") 
		exclude = ['transactionid','projectid','createpage','identifiers','postfixexp']

	def __init__(self, *args, **kwargs):
		super(TransactionviewForm, self).__init__(*args, **kwargs)
		self.fields['viewtype'].required = True



class ContainerForm(forms.ModelForm):
	class Meta:
		model = Container
		fields = '__all__'
		exclude = ['transactionviewid','identifiers']

	def __init__(self, *args, **kwargs):
		tranid = kwargs.pop('tranid')
		self.viewid = kwargs.pop('viewid')
		super(ContainerForm, self).__init__(*args, **kwargs)
		tabledetails = Txtabledetails.objects.filter(transactionid_id = tranid)
		self.fields['dbtable'].queryset = tabledetails
		self.fields['dbtable'].required = True
		cont_list = Container.objects.filter(transactionviewid_id = self.viewid)
		self.fields['parent'].queryset = cont_list
		self.fields['parent'].required = False

	def clean_dbtable(self):
		dbtable = self.cleaned_data.get('dbtable')
		queryset = self._meta.model.objects
		if self.instance.pk:
			queryset = queryset.exclude(pk=self.instance.pk)

		try:
			queryset.get(dbtable__tablename=str(dbtable),transactionviewid_id =self.viewid)
		#except self._meta.model.DoesNotExist:
		except Exception as e:
			print e
			pass
		else:
			raise forms.ValidationError("Db Table Already added In Transaction View")

		return dbtable

	def clean_displayorder(self):
		dporder = self.cleaned_data.get('displayorder')
		queryset = self._meta.model.objects
		if self.instance.pk:
			queryset = queryset.exclude(pk=self.instance.pk)

		try:
			queryset.get(displayorder = dporder,transactionviewid_id =self.viewid)
		#except self._meta.model.DoesNotExist:
		except Exception as e:
			print e
			pass
		else:
			raise forms.ValidationError("Displayorder Already Exists.") 

		return dporder
	
	def clean_containertype(self):
		cntype = self.cleaned_data.get('containertype')
		print cntype
		view = Transactionview.objects.get(id = self.viewid)
		if view.viewtype == "ng":
			if cntype == "grid":
				raise forms.ValidationError("View Type Is Non-Grid.please Select other Options.")

		return cntype

class ComponentForm(forms.ModelForm):
	class Meta:
		model = Component
		fields = '__all__'
		exclude = ['transactionviewid','containerid','identifiers','componentrefer_id','componenttype','dbcolumn','componentrefer_dt']


	def __init__(self, *args, **kwargs):
		self.viewid = kwargs.pop('viewid')
		self.contid = kwargs.pop('contid')
		super(ComponentForm, self).__init__(*args, **kwargs)

	def clean_title(self):
		title = self.cleaned_data.get('title')
		queryset = self._meta.model.objects
		if self.instance.pk:
			queryset = queryset.exclude(pk=self.instance.pk)

		try:
			queryset.get(title = title,transactionviewid_id =self.viewid)
		except Exception as e:
			print e
			pass
		else:
			raise forms.ValidationError("Title Already Exist!Please use Other.") 

		return title

    
	def clean_displayorder(self):
		dporder = self.cleaned_data.get('displayorder')
		queryset = self._meta.model.objects
		if self.instance.pk:
			queryset = queryset.exclude(pk=self.instance.pk)

		try:
			queryset.get(displayorder = dporder,containerid_id = self.contid,transactionviewid_id =self.viewid)
		except Exception as e:
			print e
			pass
		else:
			raise forms.ValidationError("Displayorder Already Exists.") 

		return dporder


class EupdateForm(forms.ModelForm):
	class Meta:
		model = Eupdate
		fields = '__all__'
		exclude = ['transactionview','targettxview','projectid']

	def __init__(self, *args, **kwargs):
		self.viewid = kwargs.pop('viewid')
		self.tx = kwargs.pop('tx')
		super(EupdateForm, self).__init__(*args, **kwargs)
		view_list = Component.objects.filter(transactionviewid_id = self.viewid)
		self.fields['source_ui_field'].queryset = view_list
		self.fields['ui_control_field'].queryset = view_list
		if self.tx:
			self.fields['target_ui_field'].queryset = Component.objects.filter(transactionviewid_id = self.tx)
		else:
			self.fields['target_ui_field'].queryset = Component.objects.none()
		self.fields['source_ui_field'].required = True
		self.fields['ui_control_field'].required = True


	def clean_target_ui_field(self):
		target_ui_field = self.cleaned_data.get('target_ui_field')
		print target_ui_field
		queryset = self._meta.model.objects
		if self.instance.pk:
			queryset = queryset.exclude(pk=self.instance.pk)

		try:
			queryset.get(target_ui_field_id = target_ui_field,transactionview_id =self.viewid)
		#except self._meta.model.DoesNotExist:
		except Exception as e:
			print e
			pass
		else:
			raise forms.ValidationError("Target Field Already Exists")

		return target_ui_field	


class EpostForm(forms.ModelForm):
	class Meta:
		model = Epost
		fields = '__all__'
		exclude = ['source_tx_view','projectid']

class EpostMapForm(forms.ModelForm):
	class Meta:
		model = EpostMapField
		fields = '__all__'
		exclude = ['epost']

	def __init__(self, *args, **kwargs):
		self.viewid = kwargs.pop('viewid')
		self.tx = kwargs.pop('tx')
		super(EpostMapForm, self).__init__(*args, **kwargs)
		view_list = Component.objects.filter(transactionviewid_id = self.viewid)
		self.fields['source_ui_field'].queryset = view_list
		self.fields['control_field'].queryset = view_list
		self.fields['group_field'].queryset = view_list
		#print("%s txview" %(self.tx))
		if self.tx:
			self.fields['target_ui_field'].queryset = Component.objects.filter(transactionviewid_id = self.tx)
		else:
			self.fields['target_ui_field'].queryset = Component.objects.none()

class FireSqlForm(forms.ModelForm):
	class Meta:
		model = FireSql
		fields =("title","sql")
		exclude = ['transactionview','slug']

class CssTxnForm(forms.ModelForm):
	class Meta:
		model = txnCssutilites
		fields = '__all__'
		exclude = ['transactionview']
