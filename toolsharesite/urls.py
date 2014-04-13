from django.conf.urls import patterns, include, url
from django.contrib import admin
import sharetools.views, messaging.views

admin.autodiscover()

urlpatterns = patterns('',

	#User/Profile  -----------------------------------------------------------
    url(r'^admin/', include(admin.site.urls)),
	url(r'^register/$', sharetools.views.register_view, name='register'),
	url(r'^login/$', sharetools.views.login_view, name='login'),
	url(r'^logout/$', sharetools.views.logout_view, name='logout'),
	url(r'^profile/$', sharetools.views.my_profile_view, name='myProfile'),
	url(r'^profile/edit$', sharetools.views.edit_profile_view, name='editProfile'),
	url(r'^profile/(\w+)$', sharetools.views.profile_view, name='profile'),
	
	#Sheds -------------------------------------------------------------------
	url(r'^sheds/$', sharetools.views.my_sheds_view, name='mySheds'),
	url(r'^sheds/(\d+)$', sharetools.views.shed_view, name='shed'),
	url(r'^sheds/create$', sharetools.views.shed_create_view, name='shedCreation'),
	url(r'^sheds/delete/(\d+)+$', sharetools.views.shed_delete_view, name='shedDeletion'),
	
	#Tools -------------------------------------------------------------------
	url(r'^tools/$', sharetools.views.my_tools_view, name='myTools'),
	url(r'^tools/new$', sharetools.views.make_tool_view,name="newTool"),
	url(r'^tools/all$', sharetools.views.all_tools_view,name="allTool"),
	url(r'^tools/delete/(\d+)$',sharetools.views.tool_delete_view,name='toolDeletion'),
	url(r'^tools/edit/(\d+)$',sharetools.views.tool_edit_view,name='toolEdit'),
	url(r'^tools/(\d+)$', sharetools.views.tool_view, name='tool'),
	
	#Shares ----------------------------------------------------------
	url(r'^shares/$', sharetools.views.shares_view, name='shares'),
	url(r'^shares/new/(\d+)+$', sharetools.views.make_share_view,name='newcontract'),
    url(r'^$', sharetools.views.index_view, name='index'),

    #Messaging --------------------------------------------------------
	url(r'^messages/$', messaging.views.messages_view, name='messages'),
	url(r'^messages/(\d+)+$', messaging.views.set_message_read, name='messageRead'),
	url(r'^messages/delete/(\d+)+$', messaging.views.message_delete_view, name='messageDelete'),
)
