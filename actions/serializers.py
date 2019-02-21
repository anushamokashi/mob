from rest_framework import serializers
from .models import Actions,SaveAction,DeleteAction,CancelAction,SearchAction,NewAction,TxnPrintFormatAction,GoogleSyncAction
from printformat.models import PrintFormat
from printformat.serializers import PrintFormatSerializer

class SaveActionSerializer(serializers.ModelSerializer):

	tt = serializers.CharField(source='title')
	exp = serializers.CharField(source='expression')
	pos = serializers.CharField(source='expression_postfix')
	icls = serializers.CharField(source='iconcls')
	u_con = serializers.CharField(source='ui_control_field')

	class Meta:
		model= SaveAction
		fields=(
			'tt', 
			'exp',  
			'pos', 
			'icls',
			'u_con'
			)

class DeleteActionSerializer(serializers.ModelSerializer):
 	
	
	tt = serializers.CharField(source='title')
	exp = serializers.CharField(source='expression')
	pos = serializers.CharField(source='expression_postfix')
	icls = serializers.CharField(source='iconcls')
	u_con = serializers.CharField(source='ui_control_field')
 	
 	class Meta:
		model= DeleteAction
		fields=(
			'tt', 
			'exp',  
			'pos', 
			'icls',
			'u_con'
			)


class CancelActionSerializer(serializers.ModelSerializer):
 	
	
	tt = serializers.CharField(source='title')
	exp = serializers.CharField(source='expression')
	pos = serializers.CharField(source='expression_postfix')
	icls = serializers.CharField(source='iconcls')
	u_con = serializers.CharField(source='ui_control_field')	
 	
	class Meta:
		model= CancelAction
		fields=(
			'tt', 
			'exp',  
			'pos', 
			'icls',
			'u_con'
			)


class NewActionSerializer(serializers.ModelSerializer):
 	
	tt = serializers.CharField(source='title')
	exp = serializers.CharField(source='expression')
	pos = serializers.CharField(source='expression_postfix')
	icls = serializers.CharField(source='iconcls')
	u_con = serializers.CharField(source='ui_control_field')
 	
	class Meta:
		model= NewAction
		fields=(
			'tt', 
			'exp',  
			'pos', 
			'icls',
			'u_con'
			)


class SearchActionSerializer(serializers.ModelSerializer):
	
	tt = serializers.CharField(source='title')
	Sql = serializers.CharField(source='sql')
	pam = serializers.CharField(source ='param_fields')
	sc = serializers.CharField(source ='search_field')
	st = serializers.CharField(source='sort_type')
	sf = serializers.CharField(source='sort_field')
	cs = serializers.CharField(source='chunk_size')	
	ps = serializers.CharField(source='page_size')
	c_tx = serializers.CharField(source='copy_tx_view')
	icls = serializers.CharField(source='iconcls')

	class Meta:
		model= SearchAction
		fields=(
			'tt', 
			'Sql',
			'pam',
			'sc',  
			'st', 
			'sf',
			'cs',
			'ps',
			'c_tx',
			'icls'
			)


class TxnPrintFormatActionSerializer(serializers.ModelSerializer):
 	
	exp = serializers.CharField(source='expression')
	u_con = serializers.CharField(source='ui_control_field')
	icls = serializers.CharField(source='iconcls')
	pfc = serializers.SerializerMethodField()

	def get_pfc(self,obj):
		print obj.pfconfig_id
		try:
			pfc_details = PrintFormat.objects.get(id = obj.pfconfig_id)
			pfc_details_serialized = PrintFormatSerializer(pfc_details)
			return pfc_details_serialized.data 
		except Exception as e:
			print e
			return ""

 	
	class Meta:
		model= NewAction
		fields=(
			'exp',  
			'u_con',
			'icls',
			'pfc',
			)

class GoogleSyncActionSerializer(serializers.ModelSerializer):
 	
	tt = serializers.CharField(source='title')
	exp = serializers.CharField(source='expression')
	icls = serializers.CharField(source='iconcls')
	u_con = serializers.CharField(source='ui_control_field')
 	
	class Meta:
		model= GoogleSyncAction
		fields=(
			'tt', 
			'exp',  
			'icls',
			'u_con'
			)

class ActionsSerializer(serializers.ModelSerializer):
	save = serializers.SerializerMethodField()
	new = serializers.SerializerMethodField()
	cancel = serializers.SerializerMethodField()
	delete = serializers.SerializerMethodField()
	search = serializers.SerializerMethodField()
	printformat = serializers.SerializerMethodField()
	googlesync = serializers.SerializerMethodField()

	def get_save(self,obj):
		print obj
		try:
			saveaction_details = SaveAction.objects.get(actiontype_id = obj.id)
			saveaction_details_serialized = SaveActionSerializer(saveaction_details)
			return saveaction_details_serialized.data 
		except:
			return ""

	def get_new(self,obj):
		try:
			newaction_details = NewAction.objects.get(actiontype_id = obj.id)
			newaction_details_serialized = NewActionSerializer(newaction_details)
			return newaction_details_serialized.data 
		except:
			return ""

	def get_cancel(self,obj):
		try:
			cancelaction_details = CancelAction.objects.get(actiontype_id = obj.id)
			cancelaction_details_serialized = CancelActionSerializer(cancelaction_details)
			return cancelaction_details_serialized.data 
		except:
			return ""

	def get_delete(self,obj):
		try:
			deleteaction_details = DeleteAction.objects.get(actiontype_id = obj.id)
			deleteaction_details_serialized = DeleteActionSerializer(deleteaction_details)
			return deleteaction_details_serialized.data 
		except:
			return ""

	def get_search(self,obj):
		try:
			searchaction_details = SearchAction.objects.get(actiontype_id = obj.id)
			searchaction_details_serialized = SearchActionSerializer(searchaction_details)
			return searchaction_details_serialized.data							
		except:
			return ""	


	def get_printformat(self,obj):
		try:
			printformat_details = TxnPrintFormatAction.objects.get(actiontype_id = obj.id)
			printformat_details_serialized = TxnPrintFormatActionSerializer(printformat_details)
			return printformat_details_serialized.data 
		except Exception as e:
			return ""
	
	def get_googlesync(self,obj):
		try:
			googlesync_details = GoogleSyncAction.objects.get(actiontype_id = obj.id)
			googlesync_details_serialized = GoogleSyncActionSerializer(googlesync_details)
			return googlesync_details_serialized.data 
		except Exception as e:
			return ""
		
	
	at = serializers.CharField(source='actiontype')

	class Meta:
		model = Actions
		fields =(
			'at',
			'save',
			'new',
			'cancel',
			'delete',
			'search',
			'printformat',
			'googlesync'
			)

