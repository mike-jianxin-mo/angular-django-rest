from django.conf.urls import patterns, include, url
from .views import SubSiteList, SubSiteDetail, SectionList, SectionDetail, SubSiteSectionList, SubSitePhotoList
from app.product.cviews import SubSiteProductList

subsite_urls = patterns('',
	url(r'^(?P<pk>[0-9a-zA-Z_-]+)/products$', SubSiteProductList.as_view(), name='subsiteproduct-list'),
	url(r'^(?P<pk>[0-9a-zA-Z_-]+)/sections$', SubSiteSectionList.as_view(), name='subsitesection-list'),
	url(r'^(?P<pk>[0-9a-zA-Z_-]+)/photos$', SubSitePhotoList.as_view(), name='subsitephoto-list'),
	url(r'^(?P<pk>[0-9]+)/$', SubSiteDetail.as_view(), name='subsite-detail'),
	url(r'^$', SubSiteList.as_view(), name='subsite-list'),
)

section_urls = patterns('',
	url(r'^$', SectionList.as_view(), name='section-list'),
	url(r'^(?P<pk>[0-9]+)/$', SectionDetail.as_view(), name='section-detail'),	
)

urlpatterns = patterns('',
	url(r'^sites/', include(subsite_urls)),
	url(r'^sections/', include(section_urls)),
)


