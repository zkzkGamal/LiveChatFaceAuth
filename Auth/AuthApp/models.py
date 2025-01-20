from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username

    
class UserEmbeddedImage(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE , null=True , blank=True)
    embedded_image = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.user.username if self.user else super().__str__()