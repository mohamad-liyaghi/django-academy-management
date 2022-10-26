from django.dispatch import receiver
from django.db.models.signals import post_save 
from django.conf import settings
from accounts.models import Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, **kwargs):
    if kwargs["created"]:
        Profile.objects.create(user=kwargs["instance"])