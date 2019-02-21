from rest_framework import serializers

from .models import userprofile

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = userprofile
		fields= (
			'email',
			'first_name',
			'last_name',
			'company',
			'mobile_number',

			)

