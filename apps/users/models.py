import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    """Custom user manager where phone is the unique identifier"""
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError(_('Phone number must be provided'))
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(phone, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = (
        ('trader', _('Trader')),
        ('admin', _('Admin')),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    phone = models.CharField(_('Phone Number'), max_length=15, unique=True)
    name = models.CharField(_('Full Name'), max_length=255)
    email = models.EmailField(_('Email Address'), blank=True, null=True)
    role = models.CharField(_('Role'), max_length=10, choices=ROLE_CHOICES, default='trader')
    address = models.TextField(_('Address'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f"{self.name} ({self.phone})"

class NotificationSettings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_settings')
    push_enabled = models.BooleanField(default=True)
    email_enabled = models.BooleanField(default=False)
    order_updates_enabled = models.BooleanField(default=True)
    offers_enabled = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notification settings for {self.user.name}"
