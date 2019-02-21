
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from transactionview.models import Transactionview,Component
from .models import TxnMappingForEvent


class ComponentEventSerializer(serializers.ModelSerializer):
    
    class Meta:
		model= Component
		fields=(
			'id',
			'title', 
			)

class TxnMappingForEventSerializer(serializers.ModelSerializer):
	title = serializers.CharField(source ='event_title.identifiers')
	desc = serializers.CharField(source ='event_desc.identifiers',allow_null=True)
	location = serializers.CharField(source ='event_location.identifiers',allow_null=True)
	start_day = serializers.CharField(source ='event_start_day.identifiers',allow_null=True)
	start_time = serializers.CharField(source ='event_start_time.identifiers',allow_null=True)
	end_day = serializers.CharField(source ='event_end_day.identifiers',allow_null=True)
	end_time = serializers.CharField(source ='event_end_time.identifiers',allow_null=True)
	email = serializers.CharField(source ='email_reminder',allow_null=True)
	popup = serializers.CharField(source ='popup_reminder',allow_null=True)
	
	class Meta:
		model= TxnMappingForEvent
		fields=(
			'slug',
			'title', 
			'desc',
			'location',
			'start_day',
			'start_time',
			'end_day',
			'end_time',
			'email',
			'popup'
		)