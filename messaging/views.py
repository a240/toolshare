from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from messaging.models import Message

def messages_view(request):
	template = loader.get_template('base_messages_inbox.html')
	messages = Message.objects.filter(msg_to=request.user)
	if messages.count() != 0:
		args = {'user_messages': messages}
		        #'form': MessageForm}
	else:
		args = {}
	context = RequestContext(request, args)
	return HttpResponse(template.render(context))