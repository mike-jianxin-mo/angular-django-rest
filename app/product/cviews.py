from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework import filters
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .models import Product, Photo
from .serializers import ProductSerializer, PhotoSerializer
import json

class ProductList(generics.ListCreateAPIView): 
# not only the generics.ListAPIView, which will cause create action error!!

	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	filter_backends = (filters.OrderingFilter,)
	ordering = ('order')

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer

class PhotoList(generics.ListCreateAPIView):
	queryset = Photo.objects.all()
	serializer_class = PhotoSerializer

class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Photo.objects.all()
	serializer_class = PhotoSerializer

class ProductPhotoList(generics.ListAPIView):
    model = Photo
    serializer_class = PhotoSerializer

    def get_queryset(self):
        queryset = super(ProductPhotoList, self).get_queryset()
        return queryset.filter(product__pk=self.kwargs.get('pk'))

class SubSiteProductList(generics.ListAPIView):
	model = Product
	serializer_class = ProductSerializer

	def get_queryset(self):
		queryset = super(SubSiteProductList, self).get_queryset()
		return queryset.filter(site__pk = self.kwargs.get('pk'))

class ProductDefaultPhoto(generics.UpdateAPIView):
	model = Photo
	serializer_class = PhotoSerializer

	def put(self, *args, **kwargs):
		request = args[0]

		data = request.DATA
		
		id = data['id']
		photo = Photo.objects.get(pk=id)
		photo.is_default = data['is_default']
		# photo.save()
		Photo.objects.filter(product=photo.product).update(is_default=False)
		photo.save(update_fields=["is_default"]) 
		serializer = PhotoSerializer(photo)

		return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
