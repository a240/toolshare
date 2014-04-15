from django.conf.urls import patterns, url
from messaging import views

urlpatterns = patterns('messaging.views',
	url(r'^(\d+)+$', views.set_message_read, name='messageRead'),
	url(r'^$', views.messages_view, name='messages'),
)