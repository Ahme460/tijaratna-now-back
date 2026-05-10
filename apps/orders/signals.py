from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, OrderRating
from apps.notifications.models import Notification
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Order)
def order_notification_signal(sender, instance, created, **kwargs):
    """
    إشعارات الطلبات:
    1. عند إنشاء طلب جديد (إشعار للتاجر/صاحب المتجر)
    2. عند تغيير حالة الطلب (إشعار للمشتري)
    """
    try:
        if created:
            # حالة إنشاء طلب جديد - نرسل إشعار لصاحب المتجر
            Notification.objects.create(
                user=instance.store.owner,
                title="طلب جديد استلمته!",
                message=f"لقد استلمت طلباً جديداً برقم #{instance.order_number} بقيمة {instance.total_amount} ج.م"
            )
        else:
            # حالة تحديث طلب موجود - نرسل إشعار للمشتري بتغيير الحالة
            # ملاحظة: يمكن تحسين هذا للتحقق من أن الحالة قد تغيرت فعلياً
            status_map = {
                'accepted': 'تم قبول طلبك',
                'processing': 'طلبك قيد التجهيز الآن',
                'shipped': 'تم شحن طلبك، ترقبه قريباً',
                'delivered': 'تم توصيل طلبك بنجاح',
                'completed': 'اكتمل الطلب، يسعدنا تقييمك',
                'rejected': 'نعتذر، تم رفض طلبك'
            }
            
            if instance.status in status_map:
                Notification.objects.create(
                    user=instance.buyer,
                    title="تحديث في حالة طلبك",
                    message=f"{status_map[instance.status]} (طلب رقم #{instance.order_number})"
                )
    except Exception as e:
        # نستخدم الـ logger لتسجيل الخطأ دون تعطيل عملية الـ save الأساسية
        logger.error(f"Error in order_notification_signal: {str(e)}")

@receiver(post_save, sender=OrderRating)
def rating_notification_signal(sender, instance, created, **kwargs):
    """
    إشعار عند قيام مشتري بتقييم طلب (إشعار للتاجر)
    """
    try:
        if created:
            Notification.objects.create(
                user=instance.store.owner,
                title="تقييم جديد لمتجرك!",
                message=f"قام أحد العملاء بتقييم الطلب #{instance.order.order_number} بـ {instance.rating} نجوم."
            )
    except Exception as e:
        logger.error(f"Error in rating_notification_signal: {str(e)}")
