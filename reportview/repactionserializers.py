from rest_framework import serializers
from .models import ReportAction,ReportPrintFormatAction,ReportPDF,ReportCSV,ReportHTML


class ReportActionSerializer(serializers.ModelSerializer):
	ReportPrintFormatAction = serializers.SerializerMethodField()
	ReportPDF = serializers.SerializerMethodField()
	ReportCSV = serializers.SerializerMethodField()
	ReportHTML = serializers.SerializerMethodField()

	def get_ReportPrintFormatAction(self,obj):
		print obj
		try:
			Printformat = ReportPrintFormatAction.objects.get(actiontype_id = obj.id)
			Printformat_serialized = ReportPrintFormatActionSerializer(Printformat)
			return Printformat_serialized.data 
		except:
			return ""

    def get_ReportPDF(self,obj):
		print obj
		try:
			ReportPDF = ReportPrintFormatAction.objects.get(actiontype_id = obj.id)
			ReportPDF_serialized = ReportPDFSerializer(ReportPDF)
			return ReportPDF_serialized.data 
		except:
			return ""

    def get_ReportCSV(self,obj):
		print obj
		try:
			ReportCSV = ReportPrintFormatAction.objects.get(actiontype_id = obj.id)
			ReportCSV_serialized = ReportCSVSerializer(ReportCSV)
			return ReportCSV_serialized.data 
		except:
			return ""

	 def get_ReportHTML(self,obj):
		print obj
		try:
			ReportHTML = ReportPrintFormatAction.objects.get(actiontype_id = obj.id)
			ReportHTML_serialized = ReportHTMLSerializer(ReportHTML)
			return ReportHTML_serialized.data 
		except:
			return ""		

	at = serializers.CharField(source='actiontype')

	class Meta:
		model = Actions
		fields =(
			'at',
			'ReportPrintFormatAction',
			'ReportPDF',
			'ReportCSV',
			'ReportHTML'
			)
	

class ReportPrintFormatActionSerializer(serializers.ModelSerializer):

	tit = serializers.CharField(source='title')
	exp = serializers.CharField(source='expression')
	pos = serializers.CharField(source='expression_postfix')
	re = serializers.CharField(source='report')
	pid =serializers.CharField(source='project_id')
	rt = serializers.CharField(source='report_type')
	rtparam = serializers.CharField(source='report_params')
	rtactid=serializers.CharField(source='report_action_id ')

	class Meta:
		model= SaveAction
		fields=(
			'tit', 
			'exp',  
			'pos', 
			're',
			'pid',
			'rt',
			'rtparam',
			'rtactid'
			)

class ReportPDFSerializer(serializers.ModelSerializer):
	tit = serializers.CharField(source='title')
    re = serializers.CharField(source='report')
    rtactid=serializers.CharField(source='report_action_id ')

	class Meta:
		model= SaveAction
		fields=(
			'tit', 			
			're',			
			'rtactid'
			)
class ReportCSVSerializer(serializers.ModelSerializer):
	tit = serializers.CharField(source='title')
    re = serializers.CharField(source='report')
    rtactid=serializers.CharField(source='report_action_id ')

	class Meta:
		model= SaveAction
		fields=(
			'tit', 			
			're',			
			'rtactid'
			)
class ReportHTMLSerializer(serializers.ModelSerializer):
	tit = serializers.CharField(source='title')
    re = serializers.CharField(source='report')
    rtactid=serializers.CharField(source='report_action_id ')

	class Meta:
		model= SaveAction
		fields=(
			'tit', 			
			're',			
			'rtactid'
			)


