from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from . import settings

from django.contrib import admin
admin.autodiscover()

from app.entry.views import Entry

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),

    # nk product system
    url(r'^$', Entry.as_view(), name='home'),
    url(r'^auth/', include('app.auth.urls')),
    url(r'^site-api/', include('app.sub_site.urls')),
    url(r'^product-api/', include('app.product.urls')),
    
    # url(r'^front/', include('app.front.urls')),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
