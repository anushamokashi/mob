from rest_framework import serializers
from .models import SMSServer,SMSAttributes

class SMSServerSerializer(serializers.ModelSerializer):
	class Meta:
		model= SMSServer
		fields=(
			'server', 
			'port', 
			'url', 
            'projectid'
			)


class SMSAttributesSerializer(serializers.ModelSerializer):
	
    class Meta:
		model= SMSAttributes
		fields=(
			'key', 
			'value', 
			)
