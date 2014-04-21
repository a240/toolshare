#forms.py - Holds the forms for receiving and handling user input
#@author David Samuelson, Phillip Lopez, Matthew Anderson, Mike Albert

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from sharetools.models import UserProfile, Asset, Location, Address, ShareContract, Membership
import datetime


class UserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'username', 'email')

class ShedForm(forms.ModelForm):
	class Meta:
		model = Location
		fields = ('name', 'description')

	def clean_name(self):
		locname = self.cleaned_data['name']
		try:
			Location.objects.get(name=locname)
		except ObjectDoesNotExist:
			return locname
		else:
			raise forms.ValidationError('Location name is already taken')

	def save(self, commit=True):
		loc = super(ShedForm, self).save(commit=False)
		if commit:
			loc.save()
		return loc

class AddressForm(forms.ModelForm):
	class Meta:
		model = Address
		fields = ('street', 'city', 'state', 'country', 'zipcode')

	def save(self, commit=True):
		add = super(AddressForm, self).save(commit=False)
		if commit:
			add.save()
		return add
		
class AddMemberForm(forms.ModelForm):

	role = forms.ChoiceField(membership.ROLE_CHOICES)
	
	class Meta:
		model = membership
		fields = ('role','user')
		
	def __init__(self, *args, **kwargs):
		self._location=kwargs.pop('location')
		super(AddMemberForm,self).__init__(*args,**kwargs)
		users = set()
		for member in membership.objects.filter(shed=self._location,role=membership.REQUEST):
			users.add(member.user.id)
		self.fields['user'].queryset = User.objects.filter(id__in = users)
			
	def save(self,commit=True):
		inst = super(AddMemberForm,self).save(commit=False)
		inst.shed = self._location
		if commit:
			inst.save()
			self.save_m2m()
		return inst
		
class EditShedForm(forms.ModelForm):
	
	class Meta:
		model = Location
		fields = (
			'name',
			'description',
			'address',
			'isActive',
			'membershipRequired',
			'inviteOnly',
			'toolModeration',
		)
			

class UserEditForm(forms.ModelForm):
	zipcode = forms.CharField(max_length = 5)
	
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'zipcode', 'email', 'password')
		widgets = {
			'email': forms.EmailInput(),
			'password': forms.PasswordInput(),
		}

class MakeToolForm(forms.ModelForm):

	class Meta:
		model = Asset
		fields = ('name','description','type','location')
		
	def __init__(self, *args, **kwargs):
		self._user=kwargs.pop('user')
		super(MakeToolForm,self).__init__(*args,**kwargs)
		self.fields['location'].queryset = Location.objects.filter(owner=self._user)
		userprofile = UserProfile.objects.get(user=self._user)
		self.fields['location'].initial = userprofile.privateLocation
		
	def save(self,commit=True):
		inst = super(MakeToolForm,self).save(commit=False)
		inst.owner = self._user
		if commit:
			inst.save()
			self.save_m2m()
		return inst
		
class MakeShareForm(forms.ModelForm):
	loanDate = forms.DateTimeField(initial=datetime.datetime.today())
	returnDate = forms.DateTimeField(initial=datetime.datetime.today())
	
	class Meta:
		model = ShareContract
		fields = ('loanDate','returnDate')
		
	def __init__(self, *args, **kwargs):
		self._borrower=kwargs.pop('user')
		self._asset=kwargs.pop('asset')
		super(MakeShareForm,self).__init__(*args,**kwargs)

		
	def save(self, commit=True):
		shareContractinst = super(MakeShareForm,self).save(commit=False)
		shareContractinst.lender = self._asset.owner
		shareContractinst.borrower = self._borrower
		shareContractinst.asset = self._asset
		
		if commit:
			shareContractinst.save()
			self.save_m2m()
		return shareContractinst

class AssetSearchForm(forms.ModelForm):
	type = forms.CharField()
	name = forms.CharField(required=False)
	available_only = forms.BooleanField(required=False)

	class Meta:
		model = Asset
		fields = ('name',)