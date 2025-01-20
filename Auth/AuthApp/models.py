from django.db import models
from django.contrib.auth.models import User as user
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(user , on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)