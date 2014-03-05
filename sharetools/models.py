# models.py 
# Contains the models for the sharetools app
# @authors Phillip Lopez, David Samuelson

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	zipcode = models.CharField(max_length=5)

	def __str__(self):
		return self.user.username


class Shed(models.Model):
	owner = models.OneToOneField(User)
	zipcode = models.CharField(max_length=5)
	name = models.CharField(max_length=80, unique=True)
	isCommunity = models.BooleanField(default=False)
	isActive = models.BooleanField(default=True)
	isPrivate = models.BooleanField(default=False)
	dateCreated = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.name
	
class Tool(models.Model):
	TOOL_CHOICES = (
			('Drills', (
					('Hammer Drill', 'Hammer Drill'),
					('Press Drill', 'Press Drill'),
					('Air Drill', 'Air Drill'),
					('Percussion Drill', 'Percussion Drill'),
					('Power Drill', 'Power Drill'),
				)
			),
			('Screwdriver', (
					('Slotted Screwdriver', 'Slotted Screwdriver'),
					('Flared Screwdriver', 'Flared Screwdriver'),
				)
			),
			('Wrenches', (
					('Torque Wrench', 'Torque Wrench'),
					('Pipe Wrench', 'Pipe Wrench'),
					('Strap Wrench', 'Strap Wrench'),
				)
			),
			('Hammer', (
					('Claw Hammer', 'Claw Hammer'),
					('Power Hammer', 'Power Hammer'),
				)
			)
		)

	owner = models.OneToOneField(User)
	type = models.CharField(max_length=80, choices=TOOL_CHOICES)
	description = models.CharField(max_length=300, blank=True)
	currentShed = models.OneToOneField(Shed)
	available =  models.BooleanField()

	def __str__(self):
		return self.owner.username + '\'s ' + self.type

class ShareContract(models.Model):
	returnDate = models.DateTimeField()
	loanDate = models.DateTimeField()
	lender = models.OneToOneField(User, related_name='lender')
	borrower = models.OneToOneField(User, related_name='borrower')
	tool = models.OneToOneField(Tool, related_name='tool')

	def __str__(self):
		return self.lender + ' lent ' + self.borrower + ' on ' + loanDate


def makeTool(owner, name, description, type):
	tool = Tool()
	tool.tool_owner = owner
	tool.name = name
	tool.description = description
	tool.type = type
	tool.currShed = tool.owner.shed
	return tool


def makeUserProfile(user, shed, zipcode):
	profile = UserProfile()
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