from django.conf.urls import patterns, include, url
from django.contrib import admin
from sharetools import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    # url(r'^$', 'toolsharesite.views.home', name='home'),
    
    url(r'^admin/', include(admin.site.urls)),
	url(r'^shed/(\d+)$', views.shed, name='shed'),
	url(r'^tool/(\d+)$', views.tool, name='tool'),
)
