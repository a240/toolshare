from django import template
from sharetools.models import UserProfile
import urllib, urllib.parse, hashlib

register = template.Library()

def gravatar_url(user):
	url = 'http://www.gravatar.com/avatar/' + hashlib.md5(
		user.email.lower().encode('utf-8')).hexdigest() + '?'
	url += urllib.parse.urlencode({
		'd': 'identicon',
		's': 350,
	})
	return url

register.simple_tag(gravatar_url)