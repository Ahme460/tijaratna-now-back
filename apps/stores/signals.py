from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Store

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_store(sender, instance, created, **kwargs):
    if created:
        Store.objects.create(
            owner=instance,
            name=f"متجر {instance.name}"
        )
