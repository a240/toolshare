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
	url(r'^sheds/$', views.my_sheds_view, name='mySheds'),
	url(r'^sheds/(\d+)$', views.shed_view, name='shed'),
	url(r'^tools/$', views.my_tools_view, name='myTools'),
	url(r'^tools/(\d+)$', views.tool_view, name='tool'),
	url(r'^profile/$', views.my_profile_view, name='myProfile'),
	url(r'^profile/edit$', views.edit_profile_view, name='editProfile'),
	url(r'^profile/(\w+)$', views.profile_view, name='profile'),
    url(r'^messages/', views.messages_view, name='messages'),
    url(r'^$', views.index_view, name='index'),
)
