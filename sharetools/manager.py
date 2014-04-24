from sharetools.models import Membership

def get_user_role(location, user):
	try:
		obj = Membership.objects.get(location=location, user=user)
		return obj.role
	except Membership.DoesNotExist:
		return None

def set_user_role(location, user, role):
	try:
		obj = Membership.objects.get(location=location, user=user)
	except Membership.DoesNotExist:
		obj = Membership(location=location, user=user, role=role)
		obj.save()
	else:
		obj.role = role
		obj.save()

def is_member(user, location):
	"""
	Returns true if the user is a member of the given location.
	"""
	try:
		obj = Membership.objects.get(location=location, user=user)
	except Membership.DoesNotExist:
		return False
	else:
		return obj.role == Membership.MEMBER or obj.role == Membership.MODERATOR or obj.role == Membership.ADMIN

def is_mod(user, location):
	"""
	Returns true is the user has moderator privilages in the given location
	"""
	try:
		obj = Membership.objects.get(location=location, user=user)
	except Membership.DoesNotExist:
		return False
	else:
		return obj.role == Membership.MODERATOR or obj.role == Membership.ADMIN