from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from sharetools.models import Asset, Location

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

def register(request):
	if request.user.is_authenticated():
		return redirect('index')
	else:
		template = loader.get_template('base_register.html')
		context = RequestContext(request, {
		})
		return HttpResponse(template.render(context))

def shed(request, shed_id):
	shedLocation = get_object_or_404(Location, pk=shed_id)
	assets = Asset.objects.filter(location=shedLocation)
	template = loader.get_template('base_shed.html')
	context = RequestContext(request, {
		'location': shedLocation,
		'assets': assets,
	})
	return HttpResponse(template.render(context))

def tool(request, id):
	return HttpResponse("Tool page." + id)

def logout(request):
	try:
		del request.session['member_id']
	except KeyError:
		return redirect('index')
	else:
		template = loader.get_template('base_logout.html')
		context = RequestContext(request, {
		})
		return HttpResponse(template.render(context))
