from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password

from sharetools.models import Asset, Location, UserProfile, User
from sharetools.forms import LoginForm, UserForm, UserEditForm 

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
			form = LoginForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				user = authenticate(username=username, password=password)
				if user is not None and user.is_active:
					login(request, user)
					return redirect('index')

			context = RequestContext(request, {
				'login_error': "The username and email you gave us did not match up"
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
			user_form = UserForm(request.POST)
			# @TODO Check if the user already exist and post good errors
			if user_form.is_valid():
				user = user_from.save(commit=false)
				# if User.objects.filter(username=user.username, email.user.email).exists():
				profile = UserProfile()
				profile.user = user
				profile.save()
				return redirect('login')

		context = RequestContext(request, {
			'form': UserForm()
		})
		template = loader.get_template('base_register.html')
		return HttpResponse(template.render(context))

# Lets anyone view the profile/username/ user's info
def profile_view(request, user_id):
	this_user = get_object_or_404(User, username__iexact=user_id)
	user_profile = this_user.userprofile
	
	template = loader.get_template('base_profile.html')
	context = RequestContext(request, {
		'userProfile': user_profile
	})
	
	return HttpResponse(template.render(context))

# Allows users to modify their profile
# Uses UserEditForm, redirects user to their profile view upon success
# @Phil
def edit_profile_view(request):
	if request.method == 'POST':
		form = UserEditForm(request.POST, instance=request.user)
		if form.is_valid():
			request.user.userprofile.zipcode = form.cleaned_data['zipcode']
			request.user.password = make_password(form.cleaned_data['password'],'pbkdf2_sha256')
			request.user.userprofile.save()
			form.save()
			return HttpResponseRedirect('/profile/'+request.user.username)
	else:
		form = UserEditForm(initial = {
			'first_name':request.user.first_name,
			'last_name':request.user.last_name,
			'zipcode':request.user.userprofile.zipcode,
			'email' : request.user.email
		})
		
	return render(request, 'base_edit_profile.html', {
		'form':form,
	})
	
def myassets_view(request):
	assets = Asset.objects.filter(owner=request.user)
	template = loader.get_template('base_myassets.html')
	context = RequestContext(request, {
		'assets': assets,
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

