from django import forms
from django.contrib.auth.models import User
from sharetools.models import UserProfile

class UserForm(forms.ModelForm):
	class Meta:
		model = User
	# first_name = forms.CharField(max_length=20)
	# last_name = forms.CharField(max_length=20)
	# username = forms.CharField(max_length=30)
	# email = forms.CharField()
	# password = forms.CharField()
	# t_and_c = forms.BooleanField()

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		exclude = ['user']

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField()