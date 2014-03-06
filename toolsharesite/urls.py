from django.conf.urls import patterns, include, url
from django.contrib import admin
from sharetools import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    # url(r'^$', 'toolsharesite.views.home', name='home'),
    
    url(r'^admin/', include(admin.site.urls)),
	url(r'^register/$', views.register_view, name='register'),
	url(r'^login/$', views.login_view, name='login'),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^shed/(\d+)$', views.shed_view, name='shed'),
	url(r'^tool/(\d+)$', views.tool_view, name='tool'),
	url(r'^profile/(\D+)$', views.profile_view, name='tool'),
    url(r'^$', views.index_view, name='index'),
)