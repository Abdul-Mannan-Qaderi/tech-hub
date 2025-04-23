from django.db import models

# Create your models here.
class Room(models.Model):
  # host
  # toppc
  name = models.CharField(max_length=255)
  description = models.TextField(null=True, blank=True)
  # participants
  last_updated = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)
  
  
  def __str__(self):
      return self.name
  