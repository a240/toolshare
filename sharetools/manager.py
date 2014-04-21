from sharetools.models import Membership

def set_user_role(location, user, role):
	try:
		obj = Membership.objects.get(location=location, user=user)
	except Membership.DoesNotExist:
		obj = Membership(location=location, user=user, role=role)
		obj.save()
	else:
		obj.role = role
		obj.save()