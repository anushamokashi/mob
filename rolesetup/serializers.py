from rest_framework import serializers
from .models import Role,ViewsForRole
from transactionview.models import Transactionview
from reportview.models import Report


class ViewsForRoleSerializer(serializers.ModelSerializer):
   
    tx = serializers.CharField(source='txview')
    rp = serializers.CharField(source='reportview')
    class Meta:
		model= ViewsForRole
		fields=(
			'tx',
			'rp'
			)

class RoleSerializer(serializers.ModelSerializer):
   
    rn = serializers.CharField(source='rolename')
    views = serializers.SerializerMethodField()
	
    def get_views(self,obj):
        roleView = ViewsForRole.objects.filter(role_id=obj.id)	
        roleViewSerializer = ViewsForRoleSerializer(instance=roleView,many=True)
        return roleViewSerializer.data
    
    class Meta:
		model= Role
		fields=(
			'rn',
			'views'
			)