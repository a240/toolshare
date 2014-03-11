# models.py 
# Contains the models for the sharetools app
# @authors Phillip Lopez, David Samuelson, Mike Albert

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	zipcode = models.CharField(max_length=5)

	def __str__(self):
		return self.user.username

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
	owner = models.ForeignKey(User, related_name = 'user')
	name = models.CharField(max_length=80)
	description = models.CharField(max_length=300, blank=True)
	type = models.ForeignKey(Asset_Type, related_name = 'type')
	location = models.ForeignKey(Location, related_name = 'location')

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.owner.username + '\'s ' + self.type.name

	def get_absolute_url(self):
		return reverse('sharetools.views.tool_view', args=[str(self.id)])

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

	def __str__(self):
		return self.lender.__str__() + ' lent ' + self.borrower.__str__() + ' a ' + self.asset.__str__() +  ' on ' + self.loanDate.__str__()

class Message(models.Model):
	subject = models.CharField(max_length=100)
	msg_to = models.ForeignKey(User, related_name='to')
	msg_from = models.ForeignKey(User, related_name='from')
	body = models.TextField()
	read = models.BooleanField(default=False)

	def __str__(self):
		return 'From ' + self.msg_from.__str__() + '  To: '+ self.msg_to.__str__() + self.body