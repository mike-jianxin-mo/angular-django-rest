from django.db import models
from django.contrib.auth.models import User

class SubSite(models.Model):
	name = models.CharField(max_length=50)
	email= models.CharField(max_length=100)
	phone= models.CharField(max_length=50)
	contact_person = models.CharField(max_length=50)
	address= models.CharField(max_length=100)
	state = models.IntegerField()
	lon = models.FloatField()
	lat = models.FloatField()
	crdate = models.DateTimeField()
	owner = models.ForeignKey(User, related_name='sites')

class Section(models.Model):
	name = models.CharField(max_length=20)
	content = models.TextField()
	type = models.IntegerField()
	state= models.IntegerField()
	site = models.ForeignKey(SubSite, related_name='sections')