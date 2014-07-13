from django.shortcuts import render
from rest_framework import generics
from .serializers import SubSiteSerializer, SectionSerializer
from .models import SubSite, Section
from app.product.models import Photo, Product
from app.product.serializers import PhotoSerializer

class SubSiteList(generics.ListCreateAPIView):
	queryset = SubSite.objects.all()
	serializer_class = SubSiteSerializer

class SubSiteDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = SubSite.objects.all()
	serializer_class = SubSiteSerializer

class SectionList(generics.ListCreateAPIView):
	queryset = Section.objects.all()
	serializer_class = SectionSerializer

class SectionDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Section.objects.all()
	serializer_class = SectionSerializer

class SubSiteSectionList(generics.ListAPIView):
    model = Section
    serializer_class = SectionSerializer

    def get_queryset(self):
        queryset = super(SubSiteSectionList, self).get_queryset()
        return queryset.filter(site__pk=self.kwargs.get('pk'))

class SubSitePhotoList(generics.ListAPIView):
    model = Photo
    serializer_class = PhotoSerializer

    def get_queryset(self):
        queryset = super(SubSitePhotoList, self).get_queryset()
        pIdList = [ p.id for p in Product.objects.filter(site__pk = self.kwargs.get('pk'))]

        return queryset.filter(product__in=pIdList)
