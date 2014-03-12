from django import forms
from django.contrib.auth.models import User
from messaging.models import Message

class MessageForm(forms.ModelForm):
	to = forms.CharField()

	class Meta:
		model = Message
		fields = ('subject','body')