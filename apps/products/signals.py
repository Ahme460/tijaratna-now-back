from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Product, ProductVariant
from apps.notifications.models import Notification

User = get_user_model()

def send_bulk_notification(title, message):
    """
    إرسال تنبيه لكل المستخدمين بشكل bulk لتحسين الأداء
    """
    users = User.objects.all()
    notifications = [
        Notification(
            user=user,
            title=title,
            message=message
        )
        for user in users
    ]
    Notification.objects.bulk_create(notifications)

@receiver(pre_save, sender=Product)
def product_pre_save(sender, instance, **kwargs):
    # نتحقق من الحالة القديمة قبل الحفظ
    if instance.pk:
        try:
            old_instance = Product.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
        except Product.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None

@receiver(post_save, sender=Product)
def product_post_save(sender, instance, created, **kwargs):
    # نرسل تنبيه فقط إذا كان المتجر مميزاً
    if not instance.store.is_featured:
        return

    if created:
        title = "منتج جديد!"
        description_text = f"\nالوصف: {instance.description}" if instance.description else ""
        message = f"التاجر {instance.store.name} أضاف منتج جديد: {instance.name}{description_text}"
        send_bulk_notification(title, message)
    elif hasattr(instance, '_old_status') and instance._old_status == 'out_of_stock' and instance.status == 'in_stock':
        # إذا تحول المنتج من غير متوفر إلى متوفر
        title = "المنتج متوفر الآن!"
        message = f"خبر سار! المنتج '{instance.name}' من التاجر {instance.store.name} أصبح متوفراً الآن."
        send_bulk_notification(title, message)

@receiver(pre_save, sender=ProductVariant)
def product_variant_pre_save(sender, instance, **kwargs):
    # نتحقق من السعر القديم قبل الحفظ لمعرفة إذا كان قد تغير
    if instance.pk:
        try:
            old_instance = ProductVariant.objects.get(pk=instance.pk)
            instance._old_price = old_instance.price
        except ProductVariant.DoesNotExist:
            instance._old_price = None
    else:
        instance._old_price = None

@receiver(post_save, sender=ProductVariant)
def product_variant_post_save(sender, instance, created, **kwargs):
    store = instance.product.store
    if not store.is_featured:
        return

    if created:
        # إضافة حجم جديد
        title = "حجم جديد متوفر"
        message = f"التاجر {store.name} أضاف حجماً جديداً ({instance.size}) للمنتج {instance.product.name}"
        send_bulk_notification(title, message)
    elif hasattr(instance, '_old_price') and instance._old_price is not None and instance._old_price != instance.price:
        # تعديل السعر
        title = "تحديث في الأسعار"
        message = f"التاجر {store.name} قام بتعديل سعر {instance.product.name} ({instance.size}) ليصبح {instance.price}"
        send_bulk_notification(title, message)
