# models.py  - Contains the views for sharetools
# @author David Samuelson, Phillip Lopez, Matthew Anderson, Mike Albert

import urllib, urllib.parse, hashlib

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password

from sharetools.models import Asset, Location, UserProfile, User, ShareContract, Message
from sharetools.forms import UserForm, UserEditForm, MakeToolForm, ShedForm, AddressForm, MakeShareForm

#index_view
#The main landing page
def index_view(request):
	if not request.user.is_authenticated():
		template = loader.get_template('landing.html')
		context = RequestContext(request, {})
		return HttpResponse(template.render(context))
	else:
		template = loader.get_template('base_index.html')
		assets = Asset.objects.exclude(owner=request.user)[:5]
		locations = Location.objects.exclude(owner=request.user)[:5]
		context = RequestContext(request, {
			'assets': assets,
			'locations': locations,
		})
		return HttpResponse(template.render(context))

#########################################################
#          Category: USER PROFILE Manipulation          #
######################################################### 


def login_view(request):
	if request.user.is_authenticated():
		return redirect('index')
	else:
		if request.method == 'POST':
			form = AuthenticationForm(data=request.POST)
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


# my_profile_view
# displays the requesting users profile
def my_profile_view(request):
	return profile_view(request, request.user.username)


# profile_view
# displays the profile
def profile_view(request, user_id):
	this_user = get_object_or_404(User, username__iexact=user_id)
	user_profile = this_user.userprofile
	gravatar_url = 'http://www.gravatar.com/avatar/' + hashlib.md5(
		this_user.email.lower().encode('utf-8')).hexdigest() + '?'
	gravatar_url += urllib.parse.urlencode({
	'd': 'identicon',
	's': 350,
	})
	template = loader.get_template('base_profile.html')
	context = RequestContext(request, {
	'userProfile': user_profile,
	'avatarURL': gravatar_url,
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
			return my_profile_view(request)
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

#########################################################
#             Category: SHED Manipulation               #
######################################################### 

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


def shed_create_view(request):
	if not request.user.is_authenticated():
		return redirect('landing')
	if request.method == 'POST':
		add_form = AddressForm(request.POST)
		sform = ShedForm(request.POST)
		if add_form.is_valid() and sform.is_valid():
			address = add_form.save()
			shed = sform.save(commit=False)
			shed.address = address
			shed.owner = request.user
			shed.save()
			messages.add_message(request, messages.SUCCESS, 'Shed Created Successfully.', extra_tags='alert-success')
			return redirect('/sheds')
		else:
			messages.add_message(request, messages.WARNING, 'Shed Creation Error.', extra_tags='alert-warning')
			return redirect('/sheds/create/')
	context = RequestContext(request, {
	'shed_form': ShedForm(),
	'address_form': AddressForm()
	})
	template = loader.get_template('base_shed_create.html')
	return HttpResponse(template.render(context))


def shed_delete_view(request, shed_id):
	shed = get_object_or_404(Location, pk=shed_id)
	if not request.user.is_authenticated():
		return redirect('landing')
	elif shed.owner == request.user:
		tools = Asset.objects.filter(location=shed)
		for tool in tools:
			shares = ShareContract.objects.filter(asset=tool)
			for share in shares:
				share.delete()
			tool.delete()
		shed.delete()
		messages.add_message(request, messages.SUCCESS, 'Shed Successfully Deleted.', extra_tags='alert-success')
	else:
		messages.add_message(request, messages.WARNING, 'You do not have that permission.', extra_tags='alert-warning')
	return redirect('mySheds')


#########################################################
#            Category: SHARE Manipulation               #
######################################################### 


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


def make_share_view(request, tool_id):
	curr_asset = get_object_or_404(Asset, pk=tool_id)
	if request.method == 'POST':
		form = MakeShareForm(request.POST, user=request.user, asset=curr_asset)
		if form.is_valid():
			messages.add_message(request, messages.SUCCESS, 'Share Contract Created Successfully.', extra_tags='alert-success')
			form.save()
			return redirect('shares')

	else:
		form = MakeShareForm(user=request.user,asset=curr_asset)

	return render(request, 'base_makeShare.html', {
	'form': form,
	'tool_id': tool_id
	})



def shares_view(request):
	template = loader.get_template('base_shares.html')
	requests = ShareContract.objects.filter(lender=request.user, status=ShareContract.PENDING)
	myrequests = ShareContract.objects.filter(borrower=request.user).exclude(status=ShareContract.FULFILLED)
	current = ShareContract.objects.filter(lender=request.user, status=ShareContract.ACCEPTED)
	former = ShareContract.objects.filter(lender=request.user, status=ShareContract.FULFILLED)
	args = {}
	if requests.count() != 0:
		args['user_requests'] = requests
	if myrequests.count() != 0:
		args['user_mypending'] = myrequests
	if current.count() != 0:
		args['user_current'] = current
	if former.count() != 0:
		args['user_former'] = former
	context = RequestContext(request, args)
	return HttpResponse(template.render(context))


def shares_return_view(request, sc_id):
	if not request.user.is_authenticated():
		return redirect('landing')
	sc = ShareContract.objects.filter(id=sc_id)[0]
	if sc.lender == request.user:
		sc.status = ShareContract.FULFILLED
		sc.save()
		messages.add_message(request, messages.SUCCESS, 'Tool returned Successfully.', extra_tags='alert-success')
	else:
		messages.add_message(request, messages.WARNING, 'You do not have that permission.', extra_tags='alert-warning')
	return redirect('shares')

def tool_review_view(request, rq_id, request_code):
	if not request.user.is_authenticated():
		return redirect('landing')
	rq = ShareContract.objects.filter(id=rq_id)[0]
	if (rq.lender != request.user) or (rq.status != ShareContract.PENDING):
		return redirect('shares')
	print(str(request_code))
	if request_code == "0":
		rq.status = ShareContract.DENIED
	else:
		rq.status = ShareContract.ACCEPTED
	rq.save()
	return redirect('shares')

#########################################################
#             Category: Tool Manipulation               #
######################################################### 

def my_tools_view(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))
		
	assets = Asset.objects.filter(owner=request.user)	
	template = loader.get_template('base_myTools.html')
	context = RequestContext(request, {
	'assets': assets,
	})
	return HttpResponse(template.render(context))
	
def all_tools_view(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))
		
	assets_all = Asset.objects.all()
	assets = assets_all.exclude(owner=request.user)
	
	template = loader.get_template('base_allTools.html')
	context = RequestContext(request, {
	'assets': assets,
	})
	return HttpResponse(template.render(context))


#Generates a new tool, owner = requesting user
def make_tool_view(request):
	if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login'))
			
	if request.method == 'POST':
		form = MakeToolForm(request.POST, user=request.user)
		if form.is_valid():
			messages.add_message(request, messages.SUCCESS, 'Tool Created Successfully.', extra_tags='alert-success')
			form.save()
			return HttpResponseRedirect(reverse('myTools'))

	else:
		form = MakeToolForm(user=request.user)

	return render(request, 'base_makeTool.html', {
	'form': form,
	})


def tool_view(request, tool_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))
		
	asset = get_object_or_404(Asset, pk=tool_id)
	sharedset = ShareContract.objects.filter(asset=tool_id, status=ShareContract.ACCEPTED)
	shared = None
	if (sharedset):
		shared = sharedset[0]
	context = RequestContext(request, {
	'user': request.user,
	'asset': asset,
	'shared': shared
	})

	template = loader.get_template('base_tool.html')
	return (HttpResponse(template.render(context)))



def tool_delete_view(request, tool_id):
	tool = get_object_or_404(Asset, pk=tool_id)
	shareCheck = ShareContract.objects.filter(asset=tool_id, status=ShareContract.ACCEPTED)
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))
	elif (shareCheck):
		messages.add_message(request, messages.WARNING, 'Tool is currently borrowed and cannot be deleted.',
		                     extra_tags='alert-warning')
	elif tool.owner == request.user:
		tool.delete()
		shareCheck = ShareContract.objects.filter(asset=tool_id)
		for share in shareCheck:
			share.delete()
		messages.add_message(request, messages.SUCCESS, 'Tool Successfully Deleted.', extra_tags='alert-success')
	else:
		messages.add_message(request, messages.WARNING, 'You do not have that permission.', extra_tags='alert-warning')
	return HttpResponseRedirect(reverse('myTools'))

#tool_edit_view
#Allows a user to change their tools shed location
#Planned: R2
def tool_edit_view(request, tool_id):
	return (HttpResponse('Tool edit ' + tool_id))
