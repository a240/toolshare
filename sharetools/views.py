from django.http import HttpResponse
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from sharetools.models import Asset, Location, UserProfile, User

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

def login_view(request):
	if request.user.is_authenticated():
		return redirect('index')
	else:
		if request.method == 'POST':
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('index')

			error = "Login Failed"

			context = RequestContext(request, {
				'login_error': error
			})
		else:
			context = RequestContext(request, {})

		template = loader.get_template('base_login.html')
		return HttpResponse(template.render(context))

def logout_view(request):
	logout(request)
	return redirect('index')

def register_view(request):
	if request.user.is_authenticated():
		return redirect('index')
	else:
		if request.method == 'POST':
			pass
			# register logic
		context = RequestContext(request, {})
		template = loader.get_template('base_register.html')
		return HttpResponse(template.render(context))

def profile_view(request, user_id):
	this_user = get_object_or_404(User, username__iexact=user_id)
	user_profile = this_user.userprofile
	
	template = loader.get_template('base_profile.html')
	context = RequestContext(request, {
		'userProfile': user_profile
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

