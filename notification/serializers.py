from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from transactionview.models import Transactionview
from reportview.models import Report
from .models import NotificationButtons,NotificationConfiguration,Notification





class TxviewSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    
    def get_type(self,obj):
        return "Transaction"
    
    def get_value(self,obj):
        val = str(obj.id)+"-Transaction"
        return val
    
    class Meta:
		model= Transactionview
		fields=(
			'id',
			'title', 
            'value',
            'type'
			)

class ReportviewSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    
    def get_type(self,obj):
        return "Report"
    
    def get_value(self,obj):
        val = str(obj.id)+"-Report"
        return val
    
    class Meta:
		model= Report
		fields=(
			'id',
			'title', 
            'value',
            'type'
			)

class ButtonSerializer(serializers.ModelSerializer):
    
    title = serializers.CharField(source='button_name')
    type = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    def get_type(self,obj):
        return "Buttons"
    
    def get_value(self,obj):
        val = str(obj.id)+"-Buttons"
        return val
    
    class Meta:
		model= NotificationButtons
		fields=(
			'id',
			'title',
            'value',
            'type'
			)

class NotificationButtonsSerializer(serializers.ModelSerializer):

    st = serializers.CharField(source='stage')
    ntf = serializers.CharField(source='notification')
    
    class Meta:
		model= NotificationButtons
		fields=(
			'button_name',
            'ntf',
            'st'
			# 'notification_configuration_id',
			)

class NotificationConfigurationSerializer(serializers.ModelSerializer):
   
    sname = serializers.CharField(source='stage_name')
    rl = serializers.CharField(source='role.rolename')
    sptype = serializers.CharField(source='status_process_type')
    sp = serializers.CharField(source='status_process')
    csprocess = serializers.CharField(source='choosed_status_process')
    ae = serializers.CharField(source='action_event')
    msg = serializers.CharField(source='message')
    fdate = serializers.CharField(source='from_date.identifiers',allow_null=True)
    tdate = serializers.CharField(source='to_date.identifiers',allow_null=True)
    idf = serializers.CharField(source='basicid_field.identifiers',allow_null=True)
    uf = serializers.CharField(source='user_field.identifiers',allow_null=True)
    
    buttons = serializers.SerializerMethodField()

    def get_buttons(self,obj):
		button_meta = NotificationButtons.objects.filter(notification_configuration_id=obj.id)
		button_serialized = NotificationButtonsSerializer(instance=button_meta,many=True)
		return button_serialized.data
    
    class Meta:
		model= NotificationConfiguration
		fields=(
			# 'notification',
			'sname',
            'rl',
            'sptype',
            'sp',
            'csprocess',
            'ae',
            'msg',
            'fdate',
            'tdate',
            'idf',
            'uf',
            'buttons',
			)

class NotificationSerializer(serializers.ModelSerializer):
    config = serializers.SerializerMethodField()
    
    def get_config(self,obj):
		stage_meta = NotificationConfiguration.objects.filter(notification_id=obj.id)
		stage_serialized = NotificationConfigurationSerializer(instance=stage_meta,many=True)
		return stage_serialized.data
        
    class Meta:
		model= Notification
		fields=(
			'title',
			# 'projectid',
            'config',
        )
