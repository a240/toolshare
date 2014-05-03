# models.py  - Contains the views for sharetools
# @author David Samuelson, Phillip Lopez, Matthew Anderson, Mike Albert

import urllib, urllib.parse, hashlib

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password
from django.views.generic import TemplateView

from sharetools.models import Asset, Location, UserProfile, User, ShareContract, Asset_Type, Address, Membership
from sharetools.forms import UserForm, UserEditForm, MakeToolForm, ShedForm, AddressForm, MakeShareForm, AssetSearchForm,  AddMemberForm, EditShedForm
from sharetools.manager import set_user_role, is_member, is_mod, get_user_role


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

class IndexView(TemplateView):
	"""
	The main index page of the site.
	"""

	NUMBER_OF_RECENT_ITEMS = 5
	template_name = "base_index.html"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return render(request, 'landing.html', {})

		assets = Asset.objects.exclude(owner=request.user)[:self.NUMBER_OF_RECENT_ITEMS]
		locations = Location.objects.exclude(owner=request.user)[:self.NUMBER_OF_RECENT_ITEMS]
		context = RequestContext(request, {
			'assets': assets,
			'locations': locations,
		})
		return render(request, self.template_name, context_instance=context)



#########################################################
#          Category: USER PROFILE Manipulation          #
######################################################### 

class LoginView(TemplateView):
	"""
	The view where a user can login.
	"""

	template_name = 'base_login.html'

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			redirect('sharetools:index')

		return render(request, self.template_name)

	def post(self, request, *args, **kwargs):
		form = AuthenticationForm(data=request.POST)
		if not form.is_valid():
			context = RequestContext(request, {
			'login_error': "The username and password you gave us did not match up"
			})
			return render(request, self.template_name, context_instance=context)
		else:
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None and user.is_active:
				login(request, user)
				return redirect('sharetools:index')
			else:
				context = RequestContext(request, {
				'login_error': "The username and password combination you gave us did not work"
				})
				return render(request, self.template_name, context_instance=context)



def logout_view(request):
	logout(request)
	return redirect('sharetools:index')

class RegisterView(TemplateView):
	"""
	The view where users register a new profile.
	"""
	template_name = 'base_register.html'

	def get(self, request):
		if request.user.is_authenticated():
			redirect('sharetools:index')

		context = RequestContext(request, {
			'form': UserForm()
		})
		return render(request, self.template_name, context_instance=context)

	def post(self, request, *args, **kwargs):
		form = UserForm(request.POST)
		if not form.is_valid():
			messages.add_message(request, messages.WARNING, 'Form Submission Error.', extra_tags='alert-warning')
			return redirect('sharetools:register')
		else:
			user = form.save()
			profile = UserProfile()
			profile.user = user
			privateShed = Location.objects.create(
				owner = user,
				name = "Private Shed",
				description = "Your private shed.  Seems like a nice spot to put tools you may not want to share right now.",
				isPrivate = True,
				isCommunity = False,
			)
			profile.privateLocation = privateShed
			profile.save()
			set_user_role(
				user=user,
				location=privateShed,
				role=Membership.ADMIN
			)

			return redirect('sharetools:login')

# my_profile_view
# displays the requesting users profile
def my_profile_view(request):
	return ProfileView.as_view()(request, request.user)

def generateGravatarUrl(user):
	url = 'http://www.gravatar.com/avatar/' + hashlib.md5(
		user.email.lower().encode('utf-8')).hexdigest() + '?'
	url += urllib.parse.urlencode({
		'd': 'identicon',
		's': 350,
	})
	return url

class ProfileView(TemplateView):
	"""
	View of a particular user's profile.
	"""
	template_name = 'base_profile.html'


	def get(self, request, user_id, *args, **kwargs):
		user = get_object_or_404(User, username=user_id)
		rated_shares = ShareContract.objects.filter(borrower=user, rated__gt=0)
		context = RequestContext(request, {
			'userProfile': user.userprofile,
			'avatarURL': generateGravatarUrl(user),
			'ratings': rated_shares,
		})
		return render(request, self.template_name, context_instance=context)
		
class EditProfileView(LoginRequiredMixin, TemplateView):
	"""
	Allows users to modify their profile.
	"""
	template_name = 'base_editProfile.html'

	def get(self, request):
		form = UserEditForm(initial={
			'first_name': request.user.first_name,
			'last_name': request.user.last_name,
			'zipcode': request.user.userprofile.zipcode,
			'email': request.user.email
		})
		context = RequestContext(request, {
			'user_name': request.user.username,
			'form': form
		})
		return render(request, self.template_name, context_instance=context)


	def post(self, request):
		form = UserEditForm(request.POST, instance=request.user)
		if not form.is_valid():
			messages.add_message(request, messages.WARNING, 'Error processing form', extra_tags='alert-warning')
			return redirect('sharetools:editProfile')
		else:
			request.user.userprofile.zipcode = form.cleaned_data['zipcode']
			request.user.password = make_password(form.cleaned_data['password'], 'pbkdf2_sha256')
			request.user.userprofile.save()
			form.save()
			return redirect('sharetools:myProfile')

#########################################################
#             Category: SHED Manipulation               #
######################################################### 

class ShedView(LoginRequiredMixin, TemplateView):
	"""
	The view for a particular shed.
	"""
	template_name = 'base_shed.html'

	def post(self, request, shed_id):
		shedLocation = get_object_or_404(Location, pk=shed_id)
		if request.POST['requestMembership'] == '1':
			if is_member(user=request.user, location=shedLocation):
				messages.add_message(request, messages.WARNING, 'You already are a member of this shed', extra_tags='alert-success')
				return redirect('sharetools:shed', shed_id)
			else:
				messages.add_message(request, messages.SUCCESS, 'Your request has been sent', extra_tags='alert-success')
				set_user_role(user=request.user, role=Membership.REQUEST, location=shedLocation)
				return redirect('sharetools:shed', shed_id)
		else:	
			return redirect('sharetools:shed', shed_id)


	def get(self, request, shed_id):	
		shedLocation = get_object_or_404(Location, pk=shed_id)
		role = get_user_role(location=shedLocation, user=request.user)
		assets = Asset.objects.filter(location=shedLocation).order_by('type')
		try:
			membership = Membership.objects.get(location=shedLocation, user=request.user)
		except Membership.DoesNotExist:
			membership = None
		context = RequestContext(request, {
			'assets': assets,
			'location': shedLocation,
			'isMember': is_member(user=request.user, location=shedLocation),
			'isMod': is_mod(user=request.user, location=shedLocation),
			'membership': membership
		})
		
		return render(request, self.template_name, context_instance=context)
			
class ShedModView(LoginRequiredMixin, TemplateView):
	"""
	The view for moderating a shed.
	"""
	template_name = 'base_shed_mod.html'

	def get(self, request, shed_id):	
		shedLocation = get_object_or_404(Location, pk=shed_id)
		members = Membership.objects.filter(location=shedLocation).order_by('role')
		members.exclude(role=Membership.REQUEST)
		requests = Membership.objects.filter(role=Membership.REQUEST)
		isAdmin = True
		try:
			member = Membership.objects.get(location=shedLocation, user=request.user)
			if member.role == Membership.MEMBER:
				isAdmin=False
		except:
			isAdmin = False
		if not isAdmin:
			return HttpResponseRedirect(reverse('sharetools:index'))

		memberForm = AddMemberForm(location=shedLocation)
		editForm = EditShedForm(instance=shedLocation)
			
		context = RequestContext(request, {
			'location': shedLocation,
			'members': members, 
			'requests':requests,
			'memberForm': memberForm,
			'editForm': editForm,
		})
		return render(request, self.template_name, context_instance=context)
		
	def post(self, request, shed_id):
		shedLocation = get_object_or_404(Location, pk=shed_id)
		memberForm = AddMemberForm(request.POST, location=shedLocation)
		editForm = EditShedForm(request.POST, instance=shedLocation)
		if memberForm.is_valid():
			member = Membership.objects.get(location=shedLocation, user=memberForm.cleaned_data['user'])
			member.delete()
			memberForm.save()
			return redirect('sharetools:shedAdmin',shed_id)
		
		elif editForm.is_valid():
			editForm.save()
			return redirect('sharetools:shedAdmin',shed_id)	
			
		else:
			return redirect('sharetools:shedAdmin',shed_id)
			
class MyShedsView(LoginRequiredMixin, TemplateView):
	"""
	A view for the shed's a user is a member of
	"""

	template_name = "base_mySheds.html"

	def get(self, request):
		memberships = Membership.objects.filter(user=request.user)
		template = loader.get_template('base_mySheds.html')
		context = RequestContext(request, {
			'memberships': memberships,
		})
		return HttpResponse(template.render(context))


def my_sheds_view(request):
	shedLocations = Location.objects.filter(owner=request.user)
	template = loader.get_template('base_mySheds.html')
	context = RequestContext(request, {
	'shedLocations': shedLocations,
	})
	return HttpResponse(template.render(context))

class ShedCrateView(LoginRequiredMixin, TemplateView):
	"""
	A view creating a new shed.
	"""

	template_name = "base_shed_create.html"

	def get(self, request):
		context = RequestContext(request, {
			'shed_form': ShedForm(),
			'address_form': AddressForm()
		})
		template = loader.get_template('base_shed_create.html')
		return render(request, self. template_name, context)

	def post(self, request):
		add_form = AddressForm(request.POST)
		sform = ShedForm(request.POST)
		if add_form.is_valid() and sform.is_valid():
			address = add_form.save()
			shed = sform.save(commit=False)
			shed.address = address
			shed.owner = request.user
			shed.save()
			Membership.objects.create( 
				location = shed, 
				role = Membership.ADMIN, 
				user = request.user 
 			) 
			messages.add_message(request, messages.SUCCESS, 'Shed Created Successfully.', extra_tags='alert-success')
			return redirect('sharetools:mySheds')
		else:
			messages.add_message(request, messages.WARNING, 'Shed Creation Error.', extra_tags='alert-warning')
			return redirect('sharetools:makeShed')


def shed_create_view(request):
	if request.method == 'POST':
		add_form = AddressForm(request.POST)
		sform = ShedForm(request.POST)
		if add_form.is_valid() and sform.is_valid():
			address = add_form.save()
			shed = sform.save(commit=False)
			shed.address = address
			shed.owner = request.user
			shed.save()
			Membership.objects.create( 
				location = shed, 
				role = Membership.ADMIN, 
				user = request.user 
 			) 
			messages.add_message(request, messages.SUCCESS, 'Shed Created Successfully.', extra_tags='alert-success')
			return redirect('sharetools:mySheds')
		else:
			messages.add_message(request, messages.WARNING, 'Shed Creation Error.', extra_tags='alert-warning')
			return redirect('sharetools:makeShed')
	context = RequestContext(request, {
	'shed_form': ShedForm(),
	'address_form': AddressForm()
	})
	template = loader.get_template('base_shed_create.html')
	return HttpResponse(template.render(context))


def shed_delete_view(request, shed_id):
	shed = get_object_or_404(Location, pk=shed_id)
	if not request.user.is_authenticated():
		return redirect('sharetools:landing')
	elif (shed.owner == request.user) and not shed.isOriginal:
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


class MakeShareView(LoginRequiredMixin, TemplateView):
	"""
	A view for creating a new share contract for an asset.
	"""

	template_name = 'base_makeShare.html'

	def get(self, request, tool_id):
		curr_asset = get_object_or_404(Asset, pk=tool_id)		
		form = MakeShareForm(user=request.user, asset=curr_asset)

		context = RequestContext(request, {
			'isMember': is_member(user=request.user, location=curr_asset.location),
			'form': form,
			'tool_id': tool_id
		})

		return render(request, self.template_name, context)

	def post(self, request, tool_id):
		# Get the tool or 404
		curr_asset = get_object_or_404(Asset, pk=tool_id)
		# Test if user has required permissions
		# Only members of the shed of the tool may borrow it
		if not is_member(user=request.user, location=curr_asset.location):
			messages.add_message(request, messages.WARNING, 'You do not have permission to borrow this tool.',
				extra_tags='alert-warning')
			return redirect('sharetools:shares')

		form = MakeShareForm(request.POST, user=request.user, asset=curr_asset)
		if form.is_valid():
			messages.add_message(request, messages.SUCCESS, 'Share Contract Created Successfully.',
				extra_tags='alert-success')
			form.save()
			return redirect('sharetools:shares')
		messages.add_message(request, messages.SUCCESS, 'Please enter a valid date.',
			extra_tags='alert-warning')	
		return redirect('sharetools:makeShareContract', tool_id)


def shares_view(request):
	if not request.user.is_authenticated():
		return redirect('sharetools:index')
	if request.method == "POST":
		if request.POST.get("cancel", "-1") != "-1":
			# cancel pending request
			ShareContract.objects.get(id=request.POST.get("cancel", "")).delete()
		elif request.POST.get("approve", "-1") != "-1":
			# approve a share request
			sc = ShareContract.objects.get(id=request.POST.get("approve", ""))
			if not sc.asset.isAvailable:
				messages.add_message(request,  messages.WARNING, 'Tool is currently borrowed and cannot be lent.',
							 extra_tags='alert-warning')
				return redirect('sharetools:shares')
			sc.status = ShareContract.ACCEPTED
			sc.save()
			sc.asset.isAvailable = False
			sc.asset.save()
		elif request.POST.get("deny", "-1") != "-1":
			# disapprove a share request
			sc = ShareContract.objects.get(id=request.POST.get("deny", ""))
			sc.status = ShareContract.DENIED
			sc.save()
		elif request.POST.get("return", "-1") != "-1":
			# mark a tool returned
			sc = ShareContract.objects.get(id=request.POST.get("return", ""))
			sc.status = ShareContract.FULFILLED
			sc.asset.isAvailable = True
			sc.asset.save()
			sc.comments = request.POST.get("comment","")
			userprofile = sc.borrower.userprofile
			if request.POST.get("options","") == "true":
				sc.borrower.userprofile.up_votes += 1
				sc.rated=1
			else:
				sc.borrower.userprofile.down_votes += 1
				sc.rated=2
			try:
				percent = (userprofile.up_votes / (userprofile.getNumVotes())) * 100
			except ZeroDivisionError:
				percent = 0
			sc.borrower.userprofile.votePercent = percent
			sc.borrower.userprofile.save()
			sc.save()
		return redirect('sharetools:shares')
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


#########################################################
#             Category: Tool Manipulation               #
######################################################### 

def my_tools_view(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('sharetools:login'))
	assets = Asset.objects.filter(owner=request.user).order_by('type')
	template = loader.get_template('base_myTools.html')
	context = RequestContext(request, {
	'assets': assets,
	})
	return HttpResponse(template.render(context))


def all_tools_view(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('sharetools:login'))

	args = {}
	assets = Asset.objects.exclude(owner=request.user).order_by('type')
	if request.method == "POST":
		form = AssetSearchForm(data=request.POST)
		if form.is_valid():
			asset_type = form.cleaned_data['type']
			name = form.cleaned_data['name']
			args['query'] = name
			args['type_field'] = asset_type
			avail_only = form.cleaned_data['available_only']
			assets = assets.filter(name__contains=name)
			if asset_type != 'all':
				assets = assets.filter(type__name=asset_type)
			if avail_only:
				args['available_only_field'] = True
	template = loader.get_template('base_allTools.html')
	args['assets'] = assets
	args['asset_types'] = Asset_Type.objects.all()
	context = RequestContext(request, args)
	return HttpResponse(template.render(context))


#Generates a new tool, owner = requesting user
def make_tool_view(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('sharetools:login'))

	if request.method == 'POST':
		form = MakeToolForm(request.POST, user=request.user)
		if form.is_valid():
			messages.add_message(request, messages.SUCCESS, 'Tool Created Successfully.', extra_tags='alert-success')
			form.save()
			return HttpResponseRedirect(reverse('sharetools:myTools'))

	else:
		form = MakeToolForm(user=request.user)

	return render(request, 'base_makeTool.html', {
	'form': form,
	})


class ToolView(LoginRequiredMixin, TemplateView):
	"""
	A single tool view.
	"""

	template_name = "base_tool.html"

	def get(self, request, tool_id):		
		asset = get_object_or_404(Asset, pk=tool_id)
		sharedset = ShareContract.objects.filter(asset=tool_id, status=ShareContract.ACCEPTED)
		shared = None
		if (sharedset):
			shared = sharedset[0]
		context = RequestContext(request, {
			'isMember': is_member(user=request.user, location=asset.location),
			'user': request.user,
			'asset': asset,
			'shared': shared
		})

		return render(request, self.template_name, context)

	def post(self, request, tool_id):
		tool = get_object_or_404(Asset, pk=tool_id)
		shareCheck = ShareContract.objects.filter(asset=tool_id, status=ShareContract.ACCEPTED)
		if (shareCheck):
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
		return redirect('sharetools:myTools')


#tool_edit_view
#Allows a user to change their tools shed location
#Planned: R2
def tool_edit_view(request, tool_id):
	if not request.user.is_authenticated():
		return redirect('sharetools:index')
	return (HttpResponse('Tool edit ' + tool_id))
