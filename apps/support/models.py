import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class SupportTicket(models.Model):
    STATUS_CHOICES = (
        ('open', _('Open')),
        ('in_progress', _('In Progress')),
        ('resolved', _('Resolved')),
        ('closed', _('Closed')),
    )

    PRIORITY_CHOICES = (
        ('low', _('Low')),
        ('medium', _('Medium')),
        ('high', _('High')),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
    subject = models.CharField(_('Subject'), max_length=255)
    message = models.TextField(_('Message'))
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(_('Priority'), max_length=10, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Support Ticket')
        verbose_name_plural = _('Support Tickets')

    def __str__(self):
        return f"{self.subject} ({self.status})"
