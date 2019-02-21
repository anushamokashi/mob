from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from .models import Transactionview,Container,Component,Eupdate,Epost,EpostMapField
from transaction.models import Transaction,Txtabledetails
from actions.models import Actions
from actions.serializers import ActionsSerializer
import json



class ComponentSerializer(serializers.ModelSerializer):

	class Meta:
		model= Component
		fields=(
			'id',
			'title',
			'caption',
        	'is_readonly',
        	'is_hidden',
        	'is_required',
        	'allow_duplicate',
        	'widgettype',
        	'expression',
        	'validateexp',
        	'sql',
        	'displayorder',
        	'containerid',
        	'transactionviewid',
        	'componentrefer_id',
        	'componenttype',
        	'dbcolumn',
        	'identifiers'
			)

class EpostComponentSerializer(serializers.ModelSerializer):

	identifiers = serializers.SerializerMethodField()

	def get_identifiers(self, obj):
		likes = '['+obj.containerid.title+']-'+obj.title
		return likes


	class Meta:
		model= Component
		fields=(
			'id',
			'identifiers',
			'componentrefer_dt',
			)

class TreecompSerializer(serializers.ModelSerializer):

	 tt = serializers.CharField(source='title')
	 cap = serializers.CharField(source='caption')
	 iro = serializers.CharField(source='is_readonly')
	 ih = serializers.CharField(source='is_hidden')
	 ire = serializers.CharField(source='is_required')
	 ad = serializers.CharField(source='allow_duplicate')
	 wt = serializers.CharField(source='widgettype')
	 exp = serializers.CharField(source='expression')
	 vep = serializers.CharField(source='validateexp')
	 do = serializers.IntegerField(source='displayorder')
	 idt = serializers.CharField(source='identifiers')
	 tid = serializers.CharField(source='transactionviewid_id')
	 cjson = serializers.CharField(source='componentrefer_dt')
	 moe = serializers.CharField(source='modeOfEntry')
	 sug = serializers.CharField(source='suggestive')
	 ct  = serializers.CharField(source='componenttype')
	 isdep = serializers.SerializerMethodField()

	 def get_isdep(self, obj):
		sql = obj.sql
		if sql:
			sqlDict =  json.loads(sql)
			isWherePresents = sqlDict['Sql'].find(":")
			if isWherePresents>0:
				return "True"
			else:
				return "False"
		else:
			return "False"

		

	 class Meta:
		model= Component
		fields=(
			'tt',
			'cap',
			'iro',
			'ih',
			'ire',
			'ad',
			'wt',
			'exp',
			'vep',
			'sql',
			'do',
			'idt',
			'tid',
			'cjson',
			'moe',
			'sug',
			'ct',
			'isdep'
			)

class metacompSerializer(serializers.ModelSerializer):

	 tt = serializers.CharField(source='title')
	 idt = serializers.CharField(source='identifiers')
	 dbtable = serializers.CharField(source='containerid.dbtable')
	 cid = serializers.CharField(source='containerid.identifiers')
	 ctype = serializers.CharField(source ='containerid.containertype')
	 cjson = serializers.CharField(source='componentrefer_dt')

	 class Meta:
		model= Component
		fields=(
			'tt',
			'idt',
			'dbtable',
                         'cid',
			'ctype',
			'cjson'
			)				

class ContainerSerializer(serializers.ModelSerializer):
	component_meta = serializers.SerializerMethodField()
	parent = serializers.ReadOnlyField(source = "parent.title")

	def get_component_meta(self,obj):
		print obj.id
		txcomponent_meta = Component.objects.filter(containerid_id=obj.id)
		print txcomponent_meta
		product_main_category_serialized = ComponentSerializer(instance=txcomponent_meta,many=True)
		return product_main_category_serialized.data 

	class Meta:
		model= Container
		fields=(
			'id',
			'title',
	        'caption',
	        'containertype',
	        'inputtype',
	        'parent',
	        'transactionviewid',
	        'displayorder',
	        'dbtable',
	        'component_meta',
			)

class TreeSerializer(serializers.ModelSerializer):
	 comp_meta = serializers.SerializerMethodField()
	 children = serializers.ListSerializer(child=RecursiveField())
	 tt = serializers.CharField(source='title')
	 cap = serializers.CharField(source='caption')
	 ctype = serializers.CharField(source='containertype')
	 itype = serializers.CharField(source='inputtype')
	 pt = serializers.CharField(source='parent')
	 exp = serializers.CharField(source='expression')
	 do = serializers.IntegerField(source='displayorder')
	 db = serializers.CharField(source='dbtable')
	 idt = serializers.CharField(source='identifiers')



	 def get_comp_meta(self,obj):
		print obj.id
		txcomponent_meta = Component.objects.filter(containerid_id=obj.id)
		print txcomponent_meta
		product_main_category_serialized = TreecompSerializer(instance=txcomponent_meta,many=True)
		return product_main_category_serialized.data 

	 class Meta:
		model= Container
		fields=(
			'tt',
	        'cap',
	        'ctype',
	        'itype',
	        'pt',
	        'exp',
	        'do',
	        'db',
	        'idt',
	        'children',
	        'comp_meta',
	        
			)
class TxtabledetailsSerializer(serializers.ModelSerializer):
	tt = serializers.CharField(source='title')
	tb = serializers.CharField(source='tablename')
	rt = serializers.CharField(source='relationshiptype')
	ispm = serializers.CharField(source='isprimary')
	tb_s = serializers.CharField(source='table_slug')

	class Meta:
		model= Txtabledetails
		fields=(
			'tt', 
			'tb', 
			'rt',
			'ispm',
			'tb_s',
			)


class TransactionSerializer(serializers.ModelSerializer):
	prm_meta = serializers.SerializerMethodField()
	tx = serializers.CharField(source='txname')

	def get_prm_meta(self,obj):
		print obj.id
		prcomponent_meta = Txtabledetails.objects.filter(transactionid_id=obj.id,isprimary = 1)
		print prcomponent_meta
		product_main_category_serialized = TxtabledetailsSerializer(instance=prcomponent_meta,many=True)
		return product_main_category_serialized.data 

	class Meta:
		model = Transaction
		fields=(
			'tx',
			'prm_meta',
			)

class EupdateSerializer(serializers.ModelSerializer):
	tr_meta = serializers.SerializerMethodField()
	so_meta = serializers.SerializerMethodField()
	ui_meta = serializers.SerializerMethodField()
	tt = serializers.CharField(source='title')
	upt = serializers.CharField(source='updatetype')
	act = serializers.CharField(source='action_type')
	txview = serializers.CharField(source='targettxview_id')
	ft_c = serializers.CharField(source='filter_clause')

	def get_tr_meta(self,obj):
		comp_meta = Component.objects.filter(id = obj.target_ui_field_id)
		eupdate_main_category_serialized = metacompSerializer(instance=comp_meta,many=True)
		return eupdate_main_category_serialized.data

	def get_so_meta(self,obj):
		comp_meta = Component.objects.filter(id = obj.source_ui_field_id)
		eupdate_main_category_serialized = metacompSerializer(instance=comp_meta,many=True)
		return eupdate_main_category_serialized.data 

	def get_ui_meta(self,obj):
		comp_meta = Component.objects.filter(id = obj.ui_control_field_id)
		eupdate_main_category_serialized = metacompSerializer(instance=comp_meta,many=True)
		return eupdate_main_category_serialized.data 			 

	class Meta:
		model = Eupdate
		fields=(
			'tt',
			'upt',
			'act',
			'txview',
			'tr_meta',
			'so_meta',
			'ui_meta',
			'ft_c'
			)

class epostcompSerializer(serializers.ModelSerializer):
	 
	 pt = serializers.CharField(source='containerid.parent')
	 cnt = serializers.CharField(source='containerid.identifiers')
	 idt = serializers.CharField(source='identifiers')
	 ad = serializers.CharField(source ='allow_duplicate')
	 wt = serializers.CharField(source ='widgettype')
	 dbtable = serializers.CharField(source='containerid.dbtable')
	 ctype = serializers.CharField(source ='containerid.containertype')
	 cjson = serializers.CharField(source='componentrefer_dt')

	 class Meta:
		model= Component
		fields=(
			'pt',
			'ad',
			'wt',
			'cnt',
			'idt',
			'dbtable',
			'ctype',
			'cjson'
			)		

class EpostMapFieldSerializer(serializers.ModelSerializer):
	tr_fld = serializers.SerializerMethodField()
	so_fld = serializers.SerializerMethodField()
	co_fld = serializers.SerializerMethodField()
	go_fld = serializers.SerializerMethodField()
	tfv = serializers.CharField(source='target_fixed_value')
	is_gd = serializers.CharField(source='is_grid_field')
	od = serializers.CharField(source='order_by')

	def get_tr_fld(self,obj):
		comp_meta = Component.objects.filter(id = obj.target_ui_field_id)
		epost_main_category_serialized = epostcompSerializer(instance=comp_meta,many=True)
		return epost_main_category_serialized.data

	def get_so_fld(self,obj):
		comp_meta = Component.objects.filter(id = obj.source_ui_field_id)
		epost_main_category_serialized = epostcompSerializer(instance=comp_meta,many=True)
		return epost_main_category_serialized.data

	def get_co_fld(self,obj):
		comp_meta = Component.objects.filter(id = obj.control_field_id)
		epost_main_category_serialized = epostcompSerializer(instance=comp_meta,many=True)
		return epost_main_category_serialized.data

	def get_go_fld(self,obj):
		comp_meta = Component.objects.filter(id = obj.group_field_id)
		epost_main_category_serialized = epostcompSerializer(instance=comp_meta,many=True)
		return epost_main_category_serialized.data		

	class Meta:
		model = EpostMapField
		fields=(
			'tfv',
			'is_gd',
			'od',
			'tr_fld',
			'so_fld',
			'co_fld',
			'go_fld'
			)


class EpostSerializer(serializers.ModelSerializer):
	map_meta = serializers.SerializerMethodField()
	ucf_meta = serializers.SerializerMethodField()
	tt = serializers.CharField(source='title')
	s_tx = serializers.CharField(source='source_tx_view.identifiers')
	T_tx = serializers.CharField(source='target_tx_view.identifiers')
	is_act = serializers.CharField(source='is_active')
	b_con = serializers.CharField(source='based_on_container')

	def get_map_meta(self,obj):
		map_meta = EpostMapField.objects.filter(epost_id=obj.id)
		map_main_category_serialized = EpostMapFieldSerializer(instance=map_meta,many=True)
		return map_main_category_serialized.data

	def get_ucf_meta(self,obj):
		comp_meta = Component.objects.filter(id = obj.ui_control_field_id)
		epost_main_category_serialized = epostcompSerializer(instance=comp_meta,many=True)
		return epost_main_category_serialized.data

	class Meta:
		model = Epost
		fields=(
			'tt',
			's_tx',
			'T_tx',
			'is_act',
			'b_con',
			'ucf_meta',
			'map_meta'
			)		

class ViewtreeSerializer(serializers.ModelSerializer):
	epost_meta = serializers.SerializerMethodField()
	eupdate_meta = serializers.SerializerMethodField()
	cont_meta = serializers.SerializerMethodField()
	tran_meta = serializers.SerializerMethodField()
	action_meta = serializers.SerializerMethodField()
	tt = serializers.CharField(source='title')
	vt = serializers.CharField(source='viewtype')
	st = serializers.CharField(source='savetype')
	pt = serializers.CharField(source='projectid_id')
	idt = serializers.CharField(source='identifiers')
	exp = serializers.CharField(source='expression')
	pos = serializers.CharField(source='postfixexp')
	
	

	def get_epost_meta(self,obj):
		epost_meta = Epost.objects.filter(source_tx_view_id=obj.id)
		epost_main_category_serialized = EpostSerializer(instance=epost_meta,many=True)
		return epost_main_category_serialized.data

	def get_eupdate_meta(self,obj):
		eupdate_meta = Eupdate.objects.filter(transactionview_id=obj.id)
		eupdate_main_category_serialized = EupdateSerializer(instance=eupdate_meta,many=True)
		return eupdate_main_category_serialized.data  

	def get_cont_meta(self,obj):
		txcomponent_meta = Container.objects.filter(transactionviewid_id=obj.id,parent = None)
		print txcomponent_meta
		product_main_category_serialized = TreeSerializer(instance=txcomponent_meta,many=True)
		return product_main_category_serialized.data 

	def get_tran_meta(self,obj):
		trans_meta = Transaction.objects.filter(pk=obj.transactionid_id)
		print trans_meta
		transaction_main_category_serialized = TransactionSerializer(instance=trans_meta,many=True)
		return transaction_main_category_serialized.data 
	
	def get_action_meta(self,obj):
		act_meta = Actions.objects.filter(transactionviewid_id=obj.id)
		print act_meta
		action_serialized = ActionsSerializer(instance=act_meta,many=True)
		return action_serialized.data 
	

	class Meta:
		model = Transactionview
		fields=(
			'tt',
			'vt',
			'st',
			'pt',
			'idt',
			'exp',
			'pos',
			'tran_meta',
			'cont_meta',
			'eupdate_meta',
			'epost_meta',
			'action_meta',
			)	

class TransactionviewSerializer(serializers.ModelSerializer):
	table_meta = serializers.SerializerMethodField()

	def get_table_meta(self,obj):
		txtabledetails_category = Container.objects.filter(pk = obj.id)
		txtabledetails_category_serialized = TreeSerializer(instance=txtabledetails_category,many=True)
		return txtabledetails_category_serialized.data 

	class Meta:
		model = Transactionview
		fields= (
			 'title',
	         'viewtype',
	         'transactionid_id',
	         'projectid_id',
	         'table_meta',
			)

