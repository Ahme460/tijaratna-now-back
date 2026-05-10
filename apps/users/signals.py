from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from apps.notifications.models import Notification
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def user_welcome_notification(sender, instance, created, **kwargs):
    """
    إرسال إشعار ترحيبي عند إنشاء مستخدم جديد
    """
    try:
        if created:
            Notification.objects.create(
                user=instance,
                title="أهلاً بك في B2B Marketplace!",
                message=f"مرحباً {instance.name or instance.phone}، نحن سعداء بانضمامك إلينا. ابدأ الآن باستكشاف أفضل العروض."
            )
    except Exception as e:
        logger.error(f"Error in user_welcome_notification signal: {str(e)}")
