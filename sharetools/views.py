from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic

from sharetools.models import Shed

def index(request):
	template = loader.get_template('index.html')
	context = RequestContext(request, {

	})
	return HttpResponse(template.render(context))

def shed(request, shed_id):
	shed = get_object_or_404(Shed, pk=shed_id)
	template = loader.get_template('base_shed.html')
	context = RequestContext(request, {
		'shed': shed
	})
	return HttpResponse(template.render(context))

def tool(request, id):
	return HttpResponse("Tool page." + id)