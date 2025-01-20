from django.db.models.signals import post_save 
from .models import UserProfile
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.core.cache import cache
User = get_user_model()

#create profile
@receiver(post_save , sender = User)
def create_profile(sender , instance , created, **kwargs):
    if created:
        name = instance.first_name + ' ' + instance.last_name
        profile = UserProfile.objects.create(user = instance)
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
     if hasattr(instance, 'profile'):
        instance.profile.save()