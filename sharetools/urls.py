from django.conf.urls import patterns, url
from sharetools import views

urlpatterns = patterns('sharetools.views',

	#User/Profile  -----------------------------------------------------------
	url(r'^register/$', views.RegisterView.as_view(), name='register'),
	url(r'^login/$', views.LoginView.as_view(), name='login'),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^profile/$', views.my_profile_view, name='myProfile'),
	url(r'^profile/edit$', views.EditProfileView.as_view(), name='editProfile'),
	url(r'^profile/(\w+)$', views.ProfileView.as_view(), name='profile'),
	
	#Sheds -------------------------------------------------------------------
	url(r'^sheds/$', views.MyShedsView.as_view(), name='mySheds'),
	url(r'^sheds/(\d+)$', views.ShedView.as_view(), name='shed'),
	url(r'^sheds/create$', views.shed_create_view, name='makeShed'),
	url(r'^sheds/delete/(\d+)+$', views.shed_delete_view, name='shedDeletion'),
	url(r'^sheds/(\d+)/admin$', views.ShedModView.as_view(), name='shedAdmin'),
	url(r'^sheds/(\d+)/admin/approve', views.approve_membership_view, name='approveMem'),
	
	#Tools -------------------------------------------------------------------
	url(r'^tools/$', views.my_tools_view, name='myTools'),
	url(r'^tools/new$', views.make_tool_view,name="newTool"),
	url(r'^tools/all$', views.all_tools_view,name="allTool"),
	url(r'^tools/edit/(\d+)$',views.tool_edit_view,name='toolEdit'),
	url(r'^tools/(\d+)$', views.ToolView.as_view(), name='tool'),
	
	#Shares ----------------------------------------------------------
	url(r'^shares/$', views.shares_view, name='shares'),
	url(r'^shares/new/(\d+)+$', views.MakeShareView.as_view(), name='makeShareContract'),
	url(r'^$', views.IndexView.as_view(), name='index'),
)