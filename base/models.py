from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
  name = models.CharField(max_length=255, null=True)
  email = models.EmailField(unique=True, null=True)
  bio = models.TextField(null=True)
  
  avatar = models.ImageField(null=True, default='avatar.svg')
  
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []
  



class Topic(models.Model):
  name = models.CharField(max_length=255)
  def __str__(self):
    return self.name



class Room(models.Model):
  topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
  host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  name = models.CharField(max_length=255)
  description = models.TextField(null=True, blank=True)
  participants = models.ManyToManyField(User, related_name='participants', blank=True)
  last_updated = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)
  def __str__(self):
      return self.name
    
  class Meta: 
    ordering = ['-last_updated', '-created_at']
  
  
class Message(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  room = models.ForeignKey(Room, on_delete=models.CASCADE)
  body = models.TextField()
  last_updated = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)
  
  class Meta: 
    ordering = ['-last_updated', '-created_at']
  
  def __str__(self):
      return self.body[:50]
  
