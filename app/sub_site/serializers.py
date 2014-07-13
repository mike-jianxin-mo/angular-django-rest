from rest_framework import serializers
from .models import SubSite, Section

class SubSiteSerializer(serializers.ModelSerializer):
	sections = serializers.HyperlinkedIdentityField('sections', view_name='subsitesection-list')
	products = serializers.HyperlinkedIdentityField('products', view_name='subsiteproduct-list')
	photos   = serializers.HyperlinkedIdentityField('photos',   view_name='subsitephoto-list')
	
	class Meta:
		model = SubSite
		fields = ('id', 'name', 'email', 'phone', 'contact_person', 'address', 'state', 'lon', 'lat', 'crdate', 'sections', 'owner', 'products', 'photos')

class SectionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Section
		fields = ('id', 'name', 'content', 'type', 'state', 'site')