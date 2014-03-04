from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Shed(models.Model):
	owner = models.ForeignKey(User)
	zipcode = models.IntegerField(default=0)
	name = models.CharField(max_length=80, unique=True)
	isCommunity = models.BooleanField(editable=False)
	isActive = models.BooleanField(default=True)
	isPrivate = models.BooleanField(default=False)
	dateCreated = models.DateTimeField(auto_now_add=True)


class UserToolShareProfile(models.Model):
	user = models.OneToOneField(User, unique=True)
	shed = models.OneToOneField(Shed)
	zipcode = models.IntegerField()


def makeUserProfile(user, shed, zipcode):
	profile = UserToolShareProfile()
	profile.user = user
	profile.shed = shed
	profile.zipcode = zipcode
	return profile
	

def makeShed(owner, zipcode, name):
	shed = Shed()
	shed.owner = owner
	shed.zipcode = zipcode
	shed.name = name
	return shed