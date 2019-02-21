from rest_framework import serializers
from .models import Homepage,Menu,RootPage


class RootPageSerializer(serializers.ModelSerializer):

	class Meta:
		Model = RootPage
		fields =(
		    'pageoption',
			'pageValue'
		)



class MenuSerializer(serializers.ModelSerializer):
	transactionview = serializers.ReadOnlyField(source = "transactionview.identifiers")
	reportview = serializers.ReadOnlyField(source = "reportview.identifiers")
	homepageid = serializers.ReadOnlyField(source = "homepageid.menutype")

	class Meta:
		model= Menu
		fields=(
			'title',
			'description',
			'iconcls' ,
			'transactionview',
			'reportview',
			'homepageid',
			'typeofview',
			'createpage'
			)


class HomepageSerializer(serializers.ModelSerializer):
	home_menu = serializers.SerializerMethodField()
	root_page = serializers.SerializerMethodField()
	project_id = serializers.ReadOnlyField(source = "project_id.slug")
	pid = serializers.ReadOnlyField(source = "project_id.id")
	p_title = serializers.ReadOnlyField(source = "project_id.title")


	def get_home_menu(self,obj):
		print obj.id
		home_meta = Menu.objects.filter(homepageid_id=obj.id)
		print home_meta
		product_main_category_serialized = MenuSerializer(instance=home_meta,many=True)
		return product_main_category_serialized.data

	def get_root_page(self,obj):
		try:
			root_meta = RootPage.objects.filter(project_id=obj.project_id_id)
			print home_meta
			root_meta_serialized = RootPageSerializer(instance=root_meta,many=True)
			return root_meta_serialized.data
		except Exception as e:
			print e


	class Meta:
		model= Homepage
		fields=(
			'menutype',
			'column' ,
			'sidemenu',
			'project_id',
			'p_title',
			'pid',
			'home_menu',
			'root_page',
			)
