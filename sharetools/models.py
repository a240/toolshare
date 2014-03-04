# models.py 
# Contains the models for the sharetools app
# @authors Phillip Lopez, 


from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Shed(models.Model):
	owner = models.ForeignKey(User)
	zipcode = models.IntegerField(default=0)
	name = models.CharField(max_length=80, unique=True)
	isCommunity = models.BooleanField(default=False)
	isActive = models.BooleanField(default=True)
	isPrivate = models.BooleanField(default=False)
	dateCreated = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.name


class UserToolShareProfile(models.Model):
	user = models.OneToOneField(User, unique=True)
	shed = models.OneToOneField(Shed)
	zipcode = models.IntegerField()
	
	def __str__(self):
		return self.user.username
	
class Tool(models.Model):

	name = models.CharField(max_length=80, unique=True)
	description = models.CharField(max_length=300)
	owner = models.OneToOneField(UserToolShareProfile, unique=True)	
	type = models.CharField(max_length=80)
	available =  models.BooleanField()
	status = models.CharField(max_length=300)
	borrower = models.OneToOneField(UserToolShareProfile, related_name="borrowing_user",blank=True, null=True)
	currShed = models.OneToOneField(Shed)
	expectedAvailabilityDate = models.DateTimeField(blank=True, null=True)
	dateLoaned = models.DateTimeField(blank=True,null=True)
	
	def __str__(self):
		return self.type + " : " + self.name

def makeTool(owner, name, description, type):

	tool = Tool()
	tool.tool_owner = owner
	tool.name = name
	tool.description = description
	tool.type = type
	tool.currShed = tool.owner.shed
	
	return tool


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