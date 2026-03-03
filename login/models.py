from django.db import models
from django.core.validators import validate_email

import uuid
# Create your models here.
class Person(models.Model):
  link = models.CharField(max_length = 50, null =True)
  first_name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)
  name = models.CharField(max_length = 300, null = True)
  user_name = models.CharField(max_length=50, null =True)
  email = models.EmailField(max_length=50, null = True)
  password = models.CharField(max_length=200)
  
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  
  def create_name(self, first_name, last_name):
    self.name = self.last_name + " " + self.first_name
    
  def save(self, *args, **kwargs):
    self.create_name(self.first_name, self.last_name)
    if not self.link:
      self.link = str(uuid.uuid4())
    super().save(*args, **kwargs)
    
class Email_Link(models.Model):
  token = models.CharField(max_length = 50)
  email = models.EmailField(null=True)
  
  used = models.BooleanField(default=False)
  is_expired = models.BooleanField(default=False)
  expiry_date = models.DateTimeField(null =True)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  
  
  def save(self, *args, **kwargs):
    if not self.token:
      self.token = str(uuid.uuid4())
    super().save(*args, **kwargs)