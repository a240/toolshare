from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
	subject = models.CharField(max_length=100)
	msg_to = models.ForeignKey(User, related_name='to')
	msg_from = models.ForeignKey(User, related_name='from')
	body = models.TextField()
	read = models.BooleanField(default=False)

	def __str__(self):
		return 'From ' + self.msg_from.__str__() + '  To: '+ self.msg_to.__str__() + self.body