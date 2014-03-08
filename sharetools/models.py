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

class Address(models.Model):
	street = models.CharField(max_length=80)
	city = models.CharField(max_length=80)
	country = models.CharField(max_length=80)
	zipcode = models.CharField(max_length=5)

	def __str__(self):
		return self.street + ', ' + self.city + ', ' + self.country

class Location(models.Model):
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=80, unique=True)
	description = models.CharField(max_length=1000)
	address = models.ForeignKey(Address)
	isActive = models.BooleanField(default=True)
	isPrivate = models.BooleanField(default=False)
	dateCreated = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class Asset_Type(models.Model):
	name = models.CharField(max_length=80, unique=True)
	description = models.CharField(max_length=300)

	def __str__(self):
		return self.name
	
class Asset(models.Model):
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=80)
	description = models.CharField(max_length=300, blank=True)
	type = models.ForeignKey(Asset_Type)
	location = models.ForeignKey(Location)

	def __str__(self):
		return self.owner.username + '\'s ' + self.type.name

class ShareContract(models.Model):
	returnDate = models.DateTimeField()
	loanDate = models.DateTimeField()
	lender = models.ForeignKey(User, related_name='lender')
	borrower = models.ForeignKey(User, related_name='borrower')
	asset = models.ForeignKey(Asset, related_name='asset')

	def __str__(self):
		return self.lender + ' lent ' + self.borrower + ' on ' + loanDate