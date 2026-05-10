from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.notifications.models import Notification
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'إضافة 100 إشعار تجريبي للمستخدم صاحب الرقم +201000000008'

    def handle(self, *args, **options):
        phone_number = '+201000000008'
        try:
            user = User.objects.get(phone=phone_number)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'المستخدم صاحب الرقم {phone_number} غير موجود'))
            return

        titles = [
            "تم استلام طلب جديد",
            "تحديث حالة الطلب",
            "عرض جديد متوفر",
            "تنبيه أمان",
            "رسالة من الإدارة",
            "تم دفع الفاتورة",
            "منتج جديد في متجرك"
        ]
        
        messages = [
            "لقد تلقيت طلباً جديداً برقم #{} من أحد العملاء.",
            "تم تغيير حالة طلبك رقم #{} إلى تم الشحن.",
            "احصل على خصم 20% على جميع المنتجات لفترة محدودة.",
            "تم تسجيل الدخول إلى حسابك من جهاز جديد.",
            "شكراً لاستخدامك منصتنا، نحن نقدر وجودك معنا.",
            "تم تأكيد عملية الدفع بنجاح لمشترياتك الأخيرة.",
            "تمت إضافة منتجك الجديد بنجاح وهو الآن معروض للبيع."
        ]

        notifications_to_create = []
        for i in range(100):
            notifications_to_create.append(
                Notification(
                    user=user,
                    title=random.choice(titles),
                    message=random.choice(messages).format(random.randint(1000, 9999)),
                    is_read=random.choice([True, False])
                )
            )

        Notification.objects.bulk_create(notifications_to_create)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully added 100 notifications for user {user.phone}'))
