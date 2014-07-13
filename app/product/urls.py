from django.conf.urls import patterns, include, url
from .cviews import ProductList, ProductDetail, PhotoList, PhotoDetail, ProductPhotoList, ProductDefaultPhoto
from . import views

product_urls = patterns('',
	url(r'^(?P<pk>[0-9a-zA-Z_-]+)/photos$', ProductPhotoList.as_view(), name='productphoto-list'),
	url(r'^(?P<pk>[0-9]+)/$', ProductDetail.as_view(), name='product-detail'),
	url(r'^$', ProductList.as_view(), name='product-list'),

	url(r'^order/', views.setSiteProductOrder),
)

photo_urls = patterns('',
	url(r'^$', PhotoList.as_view(), name='photo-list'),
	url(r'^(?P<pk>[0-9]+)/$', PhotoDetail.as_view(), name='photo-detail'),	

	url(r'setdefault/(?P<pk>[0-9]+)/$', ProductDefaultPhoto.as_view()),

)

urlpatterns = patterns('',
	url(r'^products/', include(product_urls)),
	url(r'^photos/', include(photo_urls)),
)
