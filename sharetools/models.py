# models.py 
# Contains the models for the sharetools app
# @authors Phillip Lopez, David Samuelson, Mike Albert

from django.db import models
from django.contrib.auth.models import User

class Address(models.Model):
	street = models.CharField(max_length=80)
	city = models.CharField(max_length=80)
	state = models.CharField(max_length=80)
	country = models.CharField(max_length=80)
	zipcode = models.CharField(max_length=5)

	def __str__(self):
		return self.street + ', ' + self.city + ', ' + self.country

class Location(models.Model):
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=80)
	description = models.CharField(max_length=1000)
	address = models.ForeignKey(Address, null=True)
	isActive = models.BooleanField(default=True)
	isPrivate = models.BooleanField(default=False)
	dateCreated = models.DateTimeField(auto_now_add=True)
	
	#Settings Fields
	#These fields represent settings that can be 
	#Modified by Admins/Moderators to change
	#How the Location will work
	
	membershipRequired = models.BooleanField(default=False)
	inviteOnly = models.BooleanField(default=False)
	#do tools need to be pre-approved when added to shed
	toolModeration = models.BooleanField(default=True)

	def __str__(self):
		return self.name

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	zipcode = models.CharField(max_length=5)
	karma = models.IntegerField(default=0)
	privateLocation = models.ForeignKey(Location)
	def __str__(self):
		return self.user.username

class Asset_Type(models.Model):
	name = models.CharField(max_length=80, unique=True)
	description = models.CharField(max_length=300)

	def __str__(self):
		return self.name

class Asset(models.Model):
	owner = models.ForeignKey(User, related_name = 'user')
	name = models.CharField(max_length=80)
	description = models.CharField(max_length=300, blank=True)
	type = models.ForeignKey(Asset_Type, related_name = 'type')
	location = models.ForeignKey(Location, related_name = 'location')
	availability = models.BooleanField(default = True)
	def isAvailable(self):
		if self.availability:
			return "Yes"
		return "No"
		
	def __str__(self):
		return self.owner.username + '\'s ' + self.type.name

class ShareContract(models.Model):
	PENDING = 0
	ACCEPTED = 1
	DENIED = 2
	FULFILLED = 3
	STATUS_CHOICES = (
		(PENDING, 'Pending'),
		(ACCEPTED, 'Accepted'),
		(DENIED, 'Denied'),
		(FULFILLED, 'Fulfilled'),
	)
	returnDate = models.DateTimeField()
	loanDate = models.DateTimeField()
	lender = models.ForeignKey(User, related_name='lender')
	borrower = models.ForeignKey(User, related_name='borrower')
	status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
	asset = models.ForeignKey(Asset, related_name='asset')
	rated = models.BooleanField(default=False)
	comments = models.CharField(max_length=300, blank=True)

	def getStatus(self):
		return self.STATUS_CHOICES[self.status][1]

	def __str__(self):
		return self.lender.__str__() + ' lent ' + self.borrower.__str__() + ' a ' + self.asset.__str__() +  ' on ' + self.loanDate.__str__()

class membership(models.Model):
	"""
	A record of a user's membership role within a shed.
	"""
	MEMBER = 0
	MODERATOR = 1
	ADMIN = 2	
	ROLE_CHOICES = (
		(MEMBER, 'Member'),
		(MODERATOR, 'Moderator'),
		(ADMIN, 'Admin'),
	)
	shed = models.ForeignKey(Location)
	role = models.IntegerField(choices=ROLE_CHOICES, default=MEMBER)
	user = models.ForeignKey(User)
	
	def __str__(self):
		return self.user.username + " is a " + str(self.role) + " of " + self.shed.name