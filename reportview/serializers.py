from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from .models import Report
from .models import Query
from .models import ReportField,ReportParamField,ReportGrouping,ReportAction,ReportPrintFormatAction,ReportPDF,ReportCSV,ReportHTML,ReportSubmit,ReportEpostMap,Payment,NewAction
from transactionview.serializers import epostcompSerializer
from printformat.serializers import PrintFormatSerializer
from printformat.models import PrintFormat
from transactionview.models import Component



class ReportviewSerializer(serializers.ModelSerializer):
	idt=serializers.CharField(source='identifiers')
	pid =serializers.CharField(source='project_id')
	tit = serializers.CharField(source='title')
	eh = serializers.CharField(source='enable_header')
	sl = serializers.CharField(source='slug')
	proj = serializers.CharField(source='project')
	rh1 = serializers.CharField(source='report_header_line1')
	rh2 = serializers.CharField(source='report_header_line2')
	rf1 = serializers.CharField(source='report_footer_line1')
	rf2 = serializers.CharField(source='report_footer_line2')
	dorf=serializers.CharField(source='dont_repeat_reference_field')
	roc = serializers.CharField(source='row_count')
	ih = serializers.CharField(source='is_hidden')
	rt = serializers.CharField(source='report_type')
	lp = serializers.CharField(source='lines_per_page')
	stl = serializers.CharField(source='show_grand_total')
	tem_type = serializers.CharField(source='template_type')
	template=serializers.CharField(source='rowtemplate')
	rep_des = serializers.CharField(source = 'report_description')
	xcoord=serializers.CharField(source = 'xcoordinates')
	ycoord=serializers.CharField(source = 'ycoordinates')
	sxy=serializers.CharField(source='showxyaxis')
	gtype=serializers.CharField(source = 'graphtype')

	eh = serializers.SerializerMethodField()
	sl = serializers.SerializerMethodField()
	ih = serializers.SerializerMethodField()
	stl = serializers.SerializerMethodField()

	def get_eh(self,obj):

		if obj.enable_header:
			return 'T'
		else:
			return 'F'

	def get_sl(self,obj):
		print obj.slug
		
		if obj.slug == None:
			return ''

	def get_ih(self,obj):

		if obj.is_hidden:
			return 'T'
		else:
			return 'F'

	def get_stl(self,obj):

		if obj.show_grand_total:
			return 'T'
		else:
			return 'F'
	def get_sxy(self,obj):

		if obj.showxyaxis:
			return 'T'
		else:
			return 'F'
	reportfield_meta = serializers.SerializerMethodField()
	reportparamfield_meta = serializers.SerializerMethodField()
	query_meta = serializers.SerializerMethodField()
	repgrouping_meta = serializers.SerializerMethodField()
	repaction_meta = serializers.SerializerMethodField()

	def get_reportfield_meta(self,obj):
		print obj.id
		repfield_meta = ReportField.objects.filter(report_id=obj.id)
		repfield_main_category_serialized = ReportFieldSerializer(instance=repfield_meta,many=True)
		return repfield_main_category_serialized.data


	def get_reportparamfield_meta(self,obj):
		print obj.id
		repparamfield_meta = ReportParamField.objects.filter(report_id=obj.id)
		repparamfield_main_category_serialized = ReportParamFieldSerializer(instance=repparamfield_meta,many=True)
		return repparamfield_main_category_serialized.data

	def get_query_meta(self,obj):
		print 'object',obj.id
		repquery_meta = Query.objects.filter(report_id=obj.id)
		print 'object',repquery_meta
		query_main_category_serialized = QuerySerializer(instance=repquery_meta,many=True)
		return query_main_category_serialized.data

	def get_repgrouping_meta(self,obj):
		print obj.id
		repgrouping_meta = ReportGrouping.objects.filter(report_id=obj.id)
		repgrouping_main_category_serialized = ReportGroupingSerializer(instance=repgrouping_meta,many=True)
		return repgrouping_main_category_serialized.data

		ReportActionSerializer

	def get_repaction_meta(self,obj):
		print obj.id
		repaction_meta = ReportAction.objects.filter(report_id=obj.id)
		repaction_meta_category_serialized = ReportActionSerializer(instance=repaction_meta,many=True)
		return repaction_meta_category_serialized.data	



	class Meta:
		model= Report
		fields=('tit',
			    'eh',
			    'sl',
			    'proj',
			    'pid',
			    'idt',
			    'rh1',
			    'rh2',
			    'rf1',
			    'rf2',
			    'roc',
			    'ih',
			    'rt',
			    'lp',
			    'stl',
				'dorf',
			    'rep_des',
			    'reportfield_meta',
			    'reportparamfield_meta',
			    'query_meta',
			    'repgrouping_meta',
			    'repaction_meta',
			    'tem_type',
			    'template',
				'xcoord',
				'ycoord',
				'sxy',
				'gtype'
			    # 'repbusinessrule_meta',
			    )

class ReportFieldSerializer(serializers.ModelSerializer):
	
	sl = serializers.CharField(source='slug')
	re = serializers.CharField(source='report')
	quy = serializers.CharField(source='query')
	cap = serializers.CharField(source='caption')
	nod = serializers.CharField(source='no_of_decimal_digits')
	srt = serializers.CharField(source='show_running_total')
	sht = serializers.CharField(source='show_total')
	ih = serializers.CharField(source='is_hidden')
	ac = serializers.CharField(source='apply_comma')
	dor = serializers.CharField(source='dont_repeat')
	ca = serializers.CharField(source='column_alignment')
	dz = serializers.CharField(source='dont_show_zero')
	dio = serializers.CharField(source='display_order')
	wd = serializers.CharField(source='width')
	het = serializers.CharField(source='height')
	data_typ=serializers.CharField(source='data_type')
	icls = serializers.CharField(source='iconcls')
	fielddesc=serializers.CharField(source='description')
	exp = serializers.CharField(source='expression')
	vexp = serializers.CharField(source='validate_expression')

	
	srt = serializers.SerializerMethodField()
	sht = serializers.SerializerMethodField()
	ih = serializers.SerializerMethodField()
	ac = serializers.SerializerMethodField()
	dor = serializers.SerializerMethodField()
	dz = serializers.SerializerMethodField()
	#ca = serializers.SerializerMethodField()

	def get_srt(self,obj):

		if obj.show_running_total:
			return 'T'
		else:
			return 'F'

	def get_sht(self,obj):

		if obj.show_total:
			return 'T'
		else:
		    return 'F'

	def get_ih(self,obj):

		if obj.is_hidden:
			return 'T'
		else:
		    return 'F'

	def get_ac(self,obj):

		if obj.apply_comma:
			return 'T'
		else:
		    return 'F' 

	def get_dor(self,obj):

		if obj.dont_repeat:
			return 'T'
		else:
		    return 'F' 	    


	def get_dz(self,obj):

		if obj.dont_show_zero:
			return 'T'
		else:
		    return 'F' 	    	    	    

	class Meta:
		model= ReportField
		fields=('sl',
		        're',
		        'quy',
		        'cap',
		        'nod',
		        'srt',
		        'sht',
		        'ih',
		        'ac',
		        'dor',
		        'ca',
		        'dz',
		        'dio',
		        'wd',
		        'het',
		        'data_typ',
				'icls',
                'fielddesc',
				'exp'	,
				'vexp'
		        )

class ReportParamFieldSerializer(serializers.ModelSerializer):
	idt = serializers.CharField(source='identifiers')
	sl = serializers.CharField(source='slug')
	cap = serializers.CharField(source='caption')
	rep = serializers.CharField(source='report.identifiers')
	quy = serializers.CharField(source='query')
	do = serializers.CharField(source='display_order')
	ih = serializers.CharField(source='is_hidden')
	nod = serializers.CharField(source='no_of_decimal_digits')
	vf = serializers.CharField(source='value_field')
	df = serializers.CharField(source='display_field')
	ae = serializers.CharField(source='allow_empty')
	exn = serializers.CharField(source='expression')
	ep = serializers.CharField(source='expression_postfix')
	ve = serializers.CharField(source='validate_expression')
	vep = serializers.CharField(source='validate_expression_postfix')
	wt = serializers.CharField(source='widget_type')
	comp =serializers.CharField(source='component_type')
	data_typ=serializers.CharField(source='data_type')


	ih = serializers.SerializerMethodField()
	vf = serializers.SerializerMethodField()
	df = serializers.SerializerMethodField()
	ae = serializers.SerializerMethodField()

	def get_ih(self,obj):

		if obj.is_hidden:
			return 'True'
		else:
			return 'False'

	def get_vf(self,obj):
		print obj.value_field

		if obj.value_field == None:
			return ''

	def get_df(self,obj):
		print obj.display_field

		if obj.display_field == None:
			return ''

	def get_ae(self,obj):

		if obj.allow_empty:
			return 'T'
		else:
			return 'F'

    

	class Meta:
		model= ReportParamField
		fields=('sl',
			    'idt',
			    'cap',
			    'rep',
			    'quy',
			    'do',
			    'ih',
			    'nod',
			    'vf',
			    'df',
			    'ae',
			    'exn',
			    'ep',
			    've',
			    'vep',
			    "comp",
			    "wt",
			    "data_typ",
				'sql'
			    )
		
class QuerySerializer(serializers.ModelSerializer):

	tit = serializers.CharField(source='title')
	rep = serializers.CharField(source='report')
	sq = serializers.CharField(source='sql')
	imq = serializers.CharField(source='is_main_query')
	jot = serializers.CharField(source='join_type')


	imq = serializers.SerializerMethodField()

	def get_imq(self,obj):

		if obj.is_main_query:
			return 'T'
		else:
			return 'F'


	class Meta:
		model= Query
		fields=('tit',
			    'rep',
			    'sq',
			    'imq',
			    'jot',
			    )


# class ReportBusinessRuleSerializer(serializers.ModelSerializer):
# 	sl = serializers.CharField(source='slug')
# 	rep = serializers.CharField(source='report')
# 	exn = serializers.CharField(source='expression')
# 	exp = serializers.CharField(source='expression_postfix')
# 	rpf = serializers.CharField(source='report_param_field')
# 	rf = serializers.CharField(source='report_field')
# 	vae = serializers.CharField(source='validate_expression')
# 	vep = serializers.CharField(source='validate_expression_postfix')
# 	dfe = serializers.CharField(source='display_format_expression')
# 	dfep = serializers.CharField(source='display_format_expression_postfix')
# 	sq = serializers.CharField(source='sql')
# 	ef = serializers.CharField(source='enable_filter')
# 	mfc = serializers.CharField(source='min_filter_chars')
# 	rcs = serializers.CharField(source='result_chunk_size')

# 	class Meta:
# 		model= ReportBusinessRule
# 		fields=('sl',
# 		        'rep',
# 		        'exn',
# 		        'exp',
# 		        'rpf',
# 		        'rf',
# 		        'vae',
# 		        'vep',
# 		        'dfe',
# 		        'dfep',
# 		        'sq',
# 		        'ef',
# 		        'mfc',
# 		        'rcs',
# 		        )

class ReportGroupingSerializer(serializers.ModelSerializer):
	rep = serializers.CharField(source='report')
	grf = serializers.CharField(source='groupby_field')
	caf = serializers.CharField(source='caption_field')
	hct = serializers.CharField(source='header_caption_template')
	fct = serializers.CharField(source='footer_caption_template')
	sls = serializers.CharField(source='show_line_space')
	do = serializers.CharField(source='display_order')


	sls = serializers.SerializerMethodField()

	def get_sls(self,obj):

		if obj.show_line_space:
			return 'T'
		else:
			return 'F'


	class Meta:
		model= ReportGrouping
		fields=('rep',
			    'grf',
			    'caf',
			    'hct',
			    'fct',
			    'sls',
			    'do',
		        )


class ReportPrintFormatActionSerializer(serializers.ModelSerializer):
	# ce = serializers.CharField(source='click_event')
	pfc = serializers.SerializerMethodField()
	
	def get_pfc(self,obj):
		pfcObj = PrintFormat.objects.get(id = obj.pfconfig_id)
		pfc_serialized = PrintFormatSerializer(instance=pfcObj)
		return pfc_serialized.data


	class Meta:
		model= ReportPrintFormatAction
		fields=(
			# 'ce',
			'pfc',
		)

class ReportPDFSerializer(serializers.ModelSerializer):
	icls = serializers.CharField(source='iconcls')
	tit = serializers.CharField(source='title')
	re = serializers.CharField(source='report')
	

	class Meta:
		model= ReportPDF
		fields=(
			'tit', 			
			're',
			'icls'			
			
			)
class ReportCSVSerializer(serializers.ModelSerializer):
	icls = serializers.CharField(source='iconcls')
	tit = serializers.CharField(source='title')
	re = serializers.CharField(source='report')
	
	class Meta:
		model= ReportCSV
		fields=(
			'tit',
			'icls', 			
			're',			
			
			)
class ReportHTMLSerializer(serializers.ModelSerializer):
	icls = serializers.CharField(source='iconcls')
	tit = serializers.CharField(source='title')
	re = serializers.CharField(source='report')
	
	class Meta:
		model= ReportHTML
		fields=(
			'tt',
			'icls', 			
			're',			
			
			)

class ReportEpostMapSerializer(serializers.ModelSerializer):
	so_fld = serializers.CharField(source='source_ui_field.slug',allow_null = True)
	is_gd = serializers.CharField(source='is_grid_field')
	exp = serializers.CharField(source='expression')
	tr_fld = serializers.SerializerMethodField()


	def get_tr_fld(self,obj):
		comp_meta = Component.objects.filter(id = obj.target_ui_field_id)
		epost_main_category_serialized = epostcompSerializer(instance=comp_meta,many=True)
		return epost_main_category_serialized.data


	class Meta:
		model = ReportEpostMap
		fields=(
			'tr_fld',
			'so_fld',
			'is_gd',
			'exp'
			)

class ReportSubmitSerializer(serializers.ModelSerializer):
	tt = serializers.CharField(source='title')
	rep = serializers.CharField(source='report')
	icls = serializers.CharField(source='iconcls')
	exp = serializers.CharField(source ='expression')
	click = serializers.CharField(source ='click_event')
	ep_tx = serializers.CharField(source='epost_target.identifiers')
	rep_epost = serializers.SerializerMethodField()

	def get_rep_epost(self,obj):
		epost_meta = ReportEpostMap.objects.filter(reportsubmit_id = obj.id)
		epost_main_category_serialized = ReportEpostMapSerializer(instance=epost_meta,many=True)
		return epost_main_category_serialized.data
	
	class Meta:
		model= ReportSubmit
		fields=(
			'tt', 			
			'rep',
			'icls',
			'exp',
			'ep_tx',
			'rep_epost',
			'click'			
			)

class Payment_configSerializer(serializers.ModelSerializer):
	tt = serializers.CharField(source='title')
	rep = serializers.CharField(source='report')
	icls = serializers.CharField(source='iconcls')
	exp = serializers.CharField(source ='expression')
	click = serializers.CharField(source ='click_event')
	
	class Meta:
		model= Payment
		fields=(
			'tt', 			
			'rep',
			'icls',
			'exp',
			'click'			
			)		

class NewAction_configSerializer(serializers.ModelSerializer):
	tt = serializers.CharField(source='title')
	rep = serializers.CharField(source='report')
	icls = serializers.CharField(source='iconcls')
	exp = serializers.CharField(source ='expression')
	click = serializers.CharField(source ='click_event')
	
	class Meta:
		model= NewAction
		fields=(
			'tt', 			
			'rep',
			'icls',
			'exp',
			'click'			
			)		


class ReportActionSerializer(serializers.ModelSerializer):
	ReportPrintFormatAction = serializers.SerializerMethodField()
	ReportPDF = serializers.SerializerMethodField()
	ReportCSV = serializers.SerializerMethodField()
	ReportHTML = serializers.SerializerMethodField()
	ReportSubmit = serializers.SerializerMethodField()
	Payconfig  =serializers.SerializerMethodField()
	NewActionConfig = serializers.SerializerMethodField()

	def get_ReportPrintFormatAction(self,obj):
		try:
			Printformat = ReportPrintFormatAction.objects.get(report_action_id = obj.id)
			Printformat_serialized = ReportPrintFormatActionSerializer(Printformat)			
			return Printformat_serialized.data			 
		except:
			return ""

	def get_ReportPDF(self,obj):
		try:
			PDF = ReportPDF.objects.get(report_action_id = obj.id)
			PDF_serialized = ReportPDFSerializer(PDF)
			return PDF_serialized.data 
		except:
			return ""

	def get_ReportCSV(self,obj):
		try:
			CSV = ReportCSV.objects.get(report_action_id= obj.id)
			CSV_serialized = ReportCSVSerializer(CSV)
			return CSV_serialized.data 
		except:
			return ""

	def get_ReportHTML(self,obj):
		try:
			HTML = ReportHTML.objects.get(report_action_id = obj.id)
			HTML_serialized = ReportHTMLSerializer(HTML)
			return HTML_serialized.data 
		except:
			return ""


	def get_ReportSubmit(self,obj):
		try:
			print obj.id
			submit = ReportSubmit.objects.get(report_action_id = obj.id)
			print submit.id
			submit_serialized = ReportSubmitSerializer(submit)
			return submit_serialized.data 
		except Exception as e:
			return ""

	def get_Payconfig(self,obj):
		try:
			pay_config = Payment.objects.get(report_action_id = obj.id)
			pay_config_serialized = Payment_configSerializer(pay_config)
			return pay_config_serialized.data 
		except:
			return ""

	def get_NewActionConfig(self,obj):
		try:
			newaction_config = NewAction.objects.get(report_action_id = obj.id)
			newaction_config_serialized = Payment_configSerializer(newaction_config)
			return newaction_config_serialized.data 
		except:
			return ""				

	at = serializers.CharField(source='report_action')

	class Meta:
		model = ReportAction
		fields =(
			'at',
			'ReportPrintFormatAction',
			'ReportPDF',
			'ReportCSV',
			'ReportHTML',
			'ReportSubmit',
			'Payconfig',
			'NewActionConfig'
			)
