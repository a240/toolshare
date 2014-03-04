from django.http import HttpResponse
from django.template import RequestContext, loader

from django.shortcuts import render

# Create your views here.

def index(request):
	template = loader.get_template('index.html')
	context = RequestContext(request, {

	})
	return HttpResponse(template.render(context))

def shed(request, id):
	return HttpResponse("Shed page.  Shed id:" + id)

def tool(request, id):
	return HttpResponse("Tool page." + id)