import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class MediaFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(_('File'), upload_to='uploads/%Y/%m/%d/')
    url = models.URLField(_('Direct URL'), blank=True)
    file_type = models.CharField(_('File Type'), max_length=100)
    size = models.IntegerField(_('File Size (Bytes)'))
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='uploaded_files')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Media File')
        verbose_name_plural = _('Media Files')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.url and self.file:
            self.url = self.file.url
            super().save(update_fields=['url'])

    def __str__(self):
        return f"File #{self.id}"
