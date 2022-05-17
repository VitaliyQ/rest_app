from django.contrib.auth.models import User
from django.db import models


class Ticket(models.Model):
	title = models.CharField(max_length=255)
	content = models.TextField(blank=True)
	time_create = models.DateTimeField(auto_now_add=True)
	time_update = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	status = models.ForeignKey('Status', on_delete=models.PROTECT, null=True)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ('id',)


class Message(models.Model):
	content = models.TextField(verbose_name='message', max_length=255)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	ticket = models.ForeignKey("Ticket", on_delete=models.CASCADE, related_name="messages")
	date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.content


class Status(models.Model):
	status = models.CharField(max_length=100, db_index=True)

	def __str__(self):
		return self.status
