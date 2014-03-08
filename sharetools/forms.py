from django import forms
from django.contrib.auth.models import User
from sharetools.models import UserProfile

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'username', 'email', 'password')
		widgets = {
			'email': forms.EmailInput(),
			'password': forms.PasswordInput(),
		}

	def save(self, commit=True):
		user = super(UserForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password'])
		if commit:
			user.save()
		return user

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			User.objects.get(username=username)
		except ObjectDoesNotExist:
			return username
		else:
			raise forms.ValidationError('Username is already taken')

	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			User.objects.get(email=email)
		except ObjectDoesNotExist:
			return email
		else:
			raise forms.ValidationError('Email is already in use')

class UserEditForm(forms.ModelForm):
	zipcode = forms.CharField(max_length = 5)
	
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'zipcode', 'email', 'password')
		widgets = {
			'email': forms.EmailInput(),
			'password': forms.PasswordInput(),
		}
		
		
class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField()