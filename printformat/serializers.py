from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from models import PrintFormat,PrintFormatSQL


class PrintFormatSQLSerializer(serializers.ModelSerializer):
    st = serializers.CharField(source='sql_type')
    class Meta:
		model= PrintFormatSQL
		fields=(
			'sql',
            'do',
            'st'
        )

class PrintFormatSerializer(serializers.ModelSerializer):

    at = serializers.CharField(source='action_type')
    sql = serializers.SerializerMethodField()
    
    def get_sql(self,obj):
		pfsql = PrintFormatSQL.objects.filter(printformat_id = obj.id)
		pfsql_serialized = PrintFormatSQLSerializer(instance=pfsql,many=True)
		return pfsql_serialized.data
    
    class Meta:
		model= PrintFormat
		fields=(
            'at',
            'sql',
        )