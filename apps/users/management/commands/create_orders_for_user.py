import random
from django.core.management.base import BaseCommand
from apps.users.models import User
from apps.stores.models import Store
from apps.products.models import Product
from apps.orders.models import Order, OrderItem


class Command(BaseCommand):
    help = 'Create 100 orders for a specific user'

    def add_arguments(self, parser):
        parser.add_argument(
            'phone',
            type=str,
            help='User phone number (e.g., +201000000008 or 01000000008)'
        )

    def handle(self, *args, **options):
        phone = options['phone']
        
        # البحث عن المستخدم
        try:
            user = User.objects.get(phone=phone)
            self.stdout.write(self.style.SUCCESS(f'✓ وجدت المستخدم: {user.name}'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'✗ لم أجد مستخدم برقم: {phone}'))
            return

        # الحصول على المتاجر (ما عدا متجر المستخدم)
        user_store = Store.objects.filter(owner=user).first()
        all_stores = Store.objects.exclude(owner=user)
        
        if not all_stores.exists():
            self.stdout.write(self.style.ERROR('✗ لا توجد متاجر أخرى للشراء منها'))
            return

        self.stdout.write(f'جاري إنشاء 100 أوردر للمستخدم {user.name}...')
        
        total_orders = 0
        total_items = 0
        
        for i in range(100):
            # اختيار متجر عشوائي
            store = random.choice(all_stores)
            store_products = Product.objects.filter(store=store)
            
            if not store_products.exists():
                continue
            
            # إنشاء الأوردر
            order = Order.objects.create(
                buyer=user,
                store=store,
                status=random.choice(['pending', 'accepted', 'processing', 'shipped', 'delivered', 'completed']),
                total_amount=0
            )
            
            total = 0
            # إضافة 1-5 items لكل أوردر
            num_items = random.randint(1, 5)
            for _ in range(num_items):
                prod = random.choice(store_products)
                variant = random.choice(prod.variants.all())
                qty = random.randint(1, 10)
                price = variant.price
                
                OrderItem.objects.create(
                    order=order,
                    product=prod,
                    variant=variant,
                    quantity=qty,
                    price_at_order=price
                )
                total += price * qty
                total_items += 1
            
            order.total_amount = total
            order.save()
            total_orders += 1
            
            if (i + 1) % 20 == 0:
                self.stdout.write(f'  → {i + 1}/100 أوردر تم إنشاؤها...')
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('تم بنجاح!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(f'✓ المستخدم: {user.name}')
        self.stdout.write(f'✓ إجمالي الأوردرات: {total_orders}')
        self.stdout.write(f'✓ إجمالي الـ Items: {total_items}')
        self.stdout.write(self.style.SUCCESS('='*50 + '\n'))
