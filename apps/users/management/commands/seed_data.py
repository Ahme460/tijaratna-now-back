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

        # 1. Create Users
        users = []
        for i in range(1, 11):
            phone = f'0100000000{i}' if i < 10 else f'010000000{i}'
            user, created = User.objects.get_or_create(
                phone=phone,
                defaults={
                    'name': f'Trader {i}',
                    'email': f'trader{i}@example.com',
                    'role': 'trader',
                    'address': f'Address {i}, City, Country'
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                NotificationSettings.objects.get_or_create(user=user)
            users.append(user)

        # 2. Create Categories
        categories_data = [
            {'name': 'Electronics', 'icon': 'devices'},
            {'name': 'Groceries', 'icon': 'shopping_basket'},
            {'name': 'Clothing', 'icon': 'checkroom'},
            {'name': 'Home & Garden', 'icon': 'home'},
        ]
        categories = []
        for cat_data in categories_data:
            cat, _ = Category.objects.get_or_create(name=cat_data['name'], defaults={'icon': cat_data['icon']})
            categories.append(cat)

        # 3. Create Stores
        stores = []
        for i in range(5):
            store, _ = Store.objects.get_or_create(
                name=f'Store {i+1}',
                defaults={
                    'owner': users[i],
                    'description': f'This is a description for Store {i+1}',
                    'category': categories[i % len(categories)].name,
                    'rating': random.uniform(3.5, 5.0),
                    'is_featured': random.choice([True, False]),
                    'location_lat': 30.0 + random.uniform(-0.1, 0.1),
                    'location_lng': 31.0 + random.uniform(-0.1, 0.1),
                }
            )
            stores.append(store)

        # 4. Create Products & Variants
        products = []
        for store in stores:
            for i in range(1, 6):
                product, _ = Product.objects.get_or_create(
                    name=f'Product {i} from {store.name}',
                    defaults={
                        'store': store,
                        'category': categories[random.randint(0, len(categories)-1)],
                        'description': f'Detailed description for Product {i}',
                        'is_popular': random.choice([True, False]),
                        'status': 'in_stock'
                    }
                )
                products.append(product)
                
                # Variants
                sizes = ['Small', 'Medium', 'Large', 'XL']
                for size in sizes:
                    price = random.randint(50, 500)
                    ProductVariant.objects.get_or_create(
                        product=product,
                        size=size,
                        defaults={
                            'price': price,
                            'cost': price * 0.7,
                            'stock_quantity': random.randint(10, 100),
                            'sku': f'SKU-{product.id}-{size}'
                        }
                    )

        # 5. Create Orders
        for i in range(20):
            buyer = random.choice(users)
            store = random.choice(stores)
            
            # Ensure buyer is not the store owner
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
            for _ in range(random.randint(1, 3)):
                prod = random.choice(store_products)
                variant = random.choice(prod.variants.all())
                qty = random.randint(1, 5)
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
