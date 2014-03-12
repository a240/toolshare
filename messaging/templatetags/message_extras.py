from django import template
from messaging.models import Message

register = template.Library()

def unread_message_count(user):
	"""Returns the number of unread messages the current user has"""
	count = Message.objects.filter(msg_to=user, read=False).count()
	return count

register.simple_tag(unread_message_count)