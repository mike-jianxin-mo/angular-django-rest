from rest_framework import serializers
from models import Product, Photo

class ProductSerializer(serializers.ModelSerializer):
	photos = serializers.HyperlinkedIdentityField('photos', view_name='productphoto-list')
	thumb_photo = serializers.SerializerMethodField('getThumbPhoto')
	ingredients = serializers.CharField(required = False)
	desc = serializers.CharField(required = False)

	class Meta:
		model = Product
		fields= ('order', 'id', 'name', 'code', 'desc', 'category', 'form', 'ingredients', 'site', 'thumb_photo', 'photos')

	def getThumbPhoto(self, obj):
		return obj.getThumbPhoto

	def get_validation_exclusions(self):
		# Need to exclude `author` since we'll add that later based off the request
		exclusions = super(ProductSerializer, self).get_validation_exclusions()
		return exclusions + ['order']


class PhotoSerializer(serializers.ModelSerializer):
	image_url = serializers.SerializerMethodField('getImageUrl')
	thumbnail_url = serializers.SerializerMethodField('getThumbImageUrl')

	class Meta:
		model = Photo
		fields= ('id', 'name', 'product', 'image_url', 'thumbnail_url', 'is_default', 'image')

	def getImageUrl(self, obj):
		return obj.image.url

	def getThumbImageUrl(self, obj):
		return obj.thumbnail.url
