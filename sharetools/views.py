import hashlib

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password

from sharetools.models import Asset, Location, UserProfile, User, ShareContract
from sharetools.forms import LoginForm, UserForm, UserEditForm, MakeToolForm


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
			if user_form.is_valid():
				user = user_form.save()
				profile = UserProfile()
				profile.user = user
				profile.save()
				return redirect('login')
			else:
				messages.add_message(request, messages.WARNING, 'Form Submission Error.', extra_tags='alert-warning')
				return redirect('register')
		context = RequestContext(request, {
			'form': UserForm()
		})
		template = loader.get_template('base_register.html')
		return HttpResponse(template.render(context))


def my_profile_view(request):
	return profile_view(request, request.user.username)


# Lets anyone view the profile/username/ user's info
def profile_view(request, user_id):
	this_user = get_object_or_404(User, username__iexact=user_id)
	user_profile = this_user.userprofile
	# m = hashlib.md5()
	# m.update(request.user.email)
	# hashedEmail = m.digest()
	# avatarURL = 'http://www.gravatar.com/avatar/' + hashedEmail + '?d=identicon'
	template = loader.get_template('base_profile.html')
	context = RequestContext(request, {
		'userProfile': user_profile,
		#     'avatarURL': hashedEmail,
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
			request.user.password = make_password(form.cleaned_data['password'], 'pbkdf2_sha256')
			request.user.userprofile.save()
			form.save()
			return HttpResponseRedirect('/profile/' + request.user.username)
	else:
		form = UserEditForm(initial={
			'first_name': request.user.first_name,
			'last_name': request.user.last_name,
			'zipcode': request.user.userprofile.zipcode,
			'email': request.user.email
		})

	template = loader.get_template('base_editProfile.html')
	context = RequestContext(request, {
		'user_name': request.user.username,
		'form': form
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


def my_sheds_view(request):
	shedLocations = Location.objects.filter(owner=request.user)
	template = loader.get_template('base_mySheds.html')
	context = RequestContext(request, {
		'shedLocations': shedLocations,
	})
	return HttpResponse(template.render(context))


def my_tools_view(request):
	assets = Asset.objects.filter(owner=request.user)
	template = loader.get_template('base_myTools.html')
	context = RequestContext(request, {
		'assets': assets,
	})
	return HttpResponse(template.render(context))


#Generates a new tool, owner = requesting user
#ToDo: Only present Locations user 
#      is part of in locations form
#@Phil
def make_tool_view(request):
	if request.method == 'POST':
		form = MakeToolForm(request.POST, user=request.user)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/tools/')

	else:
		form = MakeToolForm(user=request.user)

	return render(request, 'base_makeTool.html', {
		'form': form,
	})


def tool_view(request, vid):
	return HttpResponse("Tool page." + vid)


def messages_view(request):
	template = loader.get_template('base_messages_inbox.html')
	requests = ShareContract.objects.filter(lender=request.user, isApproved=False)
	if requests.count() != 0:
		args = {'user_requests': requests}
	else:
		args = {}
	context = RequestContext(request, args)
	return HttpResponse(template.render(context))