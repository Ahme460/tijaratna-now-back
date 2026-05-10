import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('Category Name'), max_length=100, unique=True)
    icon = models.CharField(_('Category Icon'), max_length=50, help_text="Material Design Icon name")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']

    def __str__(self):
        return self.name

class Store(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stores')
    name = models.CharField(_('Store Name'), max_length=255)
    logo_url = models.URLField(_('Logo URL'), blank=True, null=True)
    description = models.TextField(_('Store Description'), blank=True, null=True)
    category = models.CharField(_('Store Category'), max_length=100, blank=True, null=True)
    phone_number = models.CharField(_('Phone Number'), max_length=20, blank=True, null=True)
    whatsapp_number = models.CharField(_('WhatsApp Number'), max_length=20, blank=True, null=True)
    rating = models.FloatField(_('Rating'), default=0.0)
    is_featured = models.BooleanField(_('Is Featured'), default=False)
    location_lat = models.FloatField(_('Latitude'), null=True, blank=True)
    location_lng = models.FloatField(_('Longitude'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Store')
        verbose_name_plural = _('Stores')
        ordering = ['-created_at']

    def __str__(self):
        return self.name
