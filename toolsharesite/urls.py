from django.conf.urls import patterns, include, url
from django.contrib import admin
import sharetools.views, messaging.views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
	url(r'^messages/', include('messaging.urls', namespace='messaging', app_name='messaging')),
    url(r'^', include('sharetools.urls', namespace='sharetools', app_name='sharetools')),
)