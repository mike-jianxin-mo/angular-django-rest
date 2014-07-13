from django.conf.urls import patterns, include, url
from .views import UserDetail, UserSubSiteList, AuthView

user_urls = patterns('',
	url(r'^(?P<pk>[0-9a-zA-Z_-]+)/sites$', UserSubSiteList.as_view(), name='usersite-list'),
	url(r'^(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='user-detail'),
)

urlpatterns = patterns('',

    url(r'^api/auth/$', AuthView.as_view(), name='authenticate'),

    url(r'^users/', include(user_urls)),
)
