from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from sharetools.models import Asset, Location

def index_view(request):
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

def register_view(request):
	if request.user.is_authenticated():
		return redirect('index_view')
	else:
		template = loader.get_template('base_register.html')
		context = RequestContext(request, {
		})
		return HttpResponse(template.render(context))

def shed_view(request, shed_id):
	shedLocation = get_object_or_404(Location, pk=shed_id)
	assets = Asset.objects.filter(location=shedLocation)
	template = loader.get_template('base_shed.html')
	context = RequestContext(request, {
		'location': shedLocation,
		'assets': assets,
	})
	return HttpResponse(template.render(context))

def tool_view(request, id):
	return HttpResponse("Tool page." + id)

def logout_view(request):
	logout(request)
	return redirect('index_view')
