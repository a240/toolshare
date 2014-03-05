from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic

from sharetools.models import Shed, Tool

def index(request):
	if request.user.is_authenticated():
		template = loader.get_template('base_index.html')
		context = RequestContext(request, {
		})
		return HttpResponse(template.render(context))
	else:
		template = loader.get_template('landing.html')
		context = RequestContext(request, {
		})
		return HttpResponse(template.render(context))


def shed(request, shed_id):
	shed = get_object_or_404(Shed, pk=shed_id)
	tools = Tool.objects.filter(currentShed=shed)
	template = loader.get_template('base_shed.html')
	context = RequestContext(request, {
		'shed': shed,
		'tools': tools,
	})
	return HttpResponse(template.render(context))

def tool(request, id):
	return HttpResponse("Tool page." + id)