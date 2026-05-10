import random
from django.core.management.base import BaseCommand
from apps.users.models import User, NotificationSettings
from apps.stores.models import Category, Store
from apps.products.models import Product, ProductVariant
from apps.orders.models import Order, OrderItem
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seeds the database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # 1. Create Categories (20 categories - food related)
        food_categories = [
            {'name': 'خضروات وفواكه', 'icon': 'eco'},
            {'name': 'ألبان وأجبان', 'icon': 'water_drop'},
            {'name': 'لحوم ودواجن', 'icon': 'kebab_dining'},
            {'name': 'أسماك ومأكولات بحرية', 'icon': 'set_meal'},
            {'name': 'مخبوزات وحلويات', 'icon': 'bakery_dining'},
            {'name': 'بقوليات وحبوب', 'icon': 'grass'},
            {'name': 'زيوت وسمن', 'icon': 'opacity'},
            {'name': 'توابل وعطارة', 'icon': 'flatware'},
            {'name': 'مشروبات وعصائر', 'icon': 'local_bar'},
            {'name': 'معلبات غذائية', 'icon': 'inventory_2'},
            {'name': 'مجمدات', 'icon': 'ac_unit'},
            {'name': 'أرز ومكرونة', 'icon': 'lunch_dining'},
            {'name': 'شاي وقهوة', 'icon': 'coffee'},
            {'name': 'مكسرات وتسالي', 'icon': 'icecream'},
            {'name': 'منتجات العناية بالمنزل', 'icon': 'cleaning_services'},
            {'name': 'مستلزمات الأطفال', 'icon': 'child_care'},
            {'name': 'منظفات ورقية', 'icon': 'layers'},
            {'name': 'أدوات مائدة', 'icon': 'restaurant'},
            {'name': 'وجبات خفيفة', 'icon': 'fastfood'},
            {'name': 'منتجات عضوية', 'icon': 'nature_people'}
        ]
        
        categories = []
        for cat_data in food_categories:
            cat, _ = Category.objects.get_or_create(
                name=cat_data['name'], 
                defaults={'icon': cat_data['icon']}
            )
            categories.append(cat)

        # 2. Create Users (20 Users)
        user_names = [
            "أحمد محمد", "محمود علي", "إبراهيم حسن", "ياسر إبراهيم", "كريم سيد",
            "هاني جابر", "مصطفى محمود", "خالد وليد", "عمرو دياب", "طارق شوقي",
            "سعيد أنور", "جمال مبارك", "وائل جسار", "رامي صبري", "تامر حسني",
            "مدحت صالح", "علي الحجار", "محمد منير", "هشام عباس", "حمادة هلال"
        ]
        
        users = []
        for i, name in enumerate(user_names):
            phone = f'+2010{1000000 + i}'
            user, created = User.objects.get_or_create(
                phone=phone,
                defaults={
                    'name': name,
                    'email': f'user{i}@tijaratna.com',
                    'role': 'trader',
                    'address': f'شارع {random.randint(1, 100)}, القاهرة, مصر'
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                NotificationSettings.objects.get_or_create(user=user)
            users.append(user)

        # 3. Create Stores (for all users)
        store_names = [
            "سوبر ماركت الأمانة", "بقالة السعادة", "مركز النور للتجارة", "أسواق الخير",
            "الشركة العربية للأغذية", "محل أولاد رجب", "ماركت كازيون", "بيم ماركت",
            "أسواق فتح الله", "سوبر ماركت زاد", "هايبر وان", "سبينيس", "كارفور ماركت",
            "بقالة الهناء", "مركز مكة للتجارة", "أسواق المدينة", "سوبر ماركت المجد",
            "بقالة التوحيد", "مركز الهدى", "سوبر ماركت الصفا"
        ]
        
        stores = []
        for i, store_name in enumerate(store_names):
            store, _ = Store.objects.get_or_create(
                owner=users[i],
                defaults={
                    'name': store_name,
                    'description': f'أفضل المنتجات الغذائية بجودة عالية وأسعار منافسة في {store_name}',
                    'category': categories[i % len(categories)].name,
                    'phone_number': users[i].phone,
                    'whatsapp_number': users[i].phone,
                    'rating': random.uniform(3.5, 5.0),
                    'is_featured': random.choice([True, False]),
                    'location_lat': 30.0 + random.uniform(-0.1, 0.1),
                    'location_lng': 31.0 + random.uniform(-0.1, 0.1),
                }
            )
            stores.append(store)

        # 4. Create Products (10 per store)
        product_names = [
            "أرز مصري فاخر", "زيت عباد شمس", "مكرونة قلم", "صلصة طماطم", "تونة قطعة واحدة",
            "فول مدمس سادة", "عدس أصفر", "سكر أبيض ناعم", "شاي أسود خرز", "قهوة تركي محوجة"
        ]
        
        all_products = []
        for store in stores:
            for i, p_name in enumerate(product_names):
                product, _ = Product.objects.get_or_create(
                    name=f'{p_name} - {store.name}',
                    defaults={
                        'store': store,
                        'category': categories[random.randint(0, len(categories)-1)],
                        'description': f'منتج {p_name} عالي الجودة متوفر الآن في {store.name}',
                        'is_popular': random.choice([True, False]),
                        'status': 'in_stock'
                    }
                )
                all_products.append(product)
                
                # Variants
                sizes = ['كجم', '500 جرام', '2 كجم']
                for size in sizes:
                    price = random.randint(20, 150)
                    ProductVariant.objects.get_or_create(
                        product=product,
                        size=size,
                        defaults={
                            'price': price,
                            'cost': price * 0.8,
                            'stock_quantity': random.randint(50, 500),
                            'sku': f'SKU-{product.id}-{size}'
                        }
                    )

        # 5. Create Orders (30 orders)
        for i in range(30):
            buyer = random.choice(users)
            store = random.choice(stores)
            
            if buyer == store.owner:
                continue
                
            store_products = Product.objects.filter(store=store)
            if not store_products.exists():
                continue
                
            order = Order.objects.create(
                buyer=buyer,
                store=store,
                status=random.choice(['pending', 'accepted', 'processing', 'shipped', 'delivered', 'completed']),
                total_amount=0
            )
            
            total = 0
            # Each order has 1-4 items
            for _ in range(random.randint(1, 4)):
                prod = random.choice(store_products)
                variants = prod.variants.all()
                if not variants.exists():
                    continue
                    
                variant = random.choice(variants)
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
            
            order.total_amount = total
            order.save()

        self.stdout.write(self.style.SUCCESS('Successfully seeded data!'))
