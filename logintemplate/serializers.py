from rest_framework import serializers
from .models import Login

class loginSerializer(serializers.ModelSerializer):
	tt = serializers.CharField(source='title')
	ly = serializers.CharField(source='login_type')
	bgc = serializers.CharField(source='bgcolor')
	reg = serializers.CharField(source='regeisterion_page')
	pid = serializers.CharField(source='project_id')
	

       

	class Meta:
		model= Login
		fields=(
			'tt',
			'ly',
			'bgc',
			'reg',
			'pid'
			)

	
