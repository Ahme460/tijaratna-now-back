import random
from decimal import Decimal

from django.core.management.base import BaseCommand

from apps.products.models import Product, ProductVariant
from apps.stores.models import Category, Store
from apps.users.models import NotificationSettings, User


def clean_url(raw_url):
    return raw_url.replace("`", "").strip()


class Command(BaseCommand):
    help = "Seeds users, stores, and products using existing categories"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding users, stores, and products...")

        category_mapping = {
            "Fruits": "خضروات وفواكه",
            "Vegetables": "خضروات وفواكه",
            "Bakery": "مخبوزات وحلويات",
            "Dairy": "ألبان وأجبان",
            "Drinks": "مشروبات وعصائر",
            "Snacks": "وجبات خفيفة",
        }

        stores = [
            {
                "name": "Fresh Market",
                "location": "Cairo",
                "rating": 4.5,
                "image": " `https://images.unsplash.com/photo-1514933651103-005eec06c04b` ",
            },
            {
                "name": "Green Grocery",
                "location": "Alexandria",
                "rating": 4.2,
                "image": " `https://images.unsplash.com/photo-1556740749-887f6717d7e4` ",
            },
            {
                "name": "Daily Mart",
                "location": "Giza",
                "rating": 4.0,
                "image": " `https://images.unsplash.com/photo-1528698827591-e19ccd7bc23d` ",
            },
            {
                "name": "Mega Store",
                "location": "Mansoura",
                "rating": 4.7,
                "image": " `https://images.unsplash.com/photo-1441986300917-64674bd600d8` ",
            },
            {
                "name": "Family Supermarket",
                "location": "Tanta",
                "rating": 4.3,
                "image": " `https://images.unsplash.com/photo-1481437156560-3205f6a55735` ",
            },
            {
                "name": "City Shop",
                "location": "Aswan",
                "rating": 4.1,
                "image": " `https://images.unsplash.com/photo-1521334884684-d80222895322` ",
            },
            {
                "name": "Food Hub",
                "location": "Luxor",
                "rating": 4.6,
                "image": " `https://images.unsplash.com/photo-1441984904996-e0b6ba687e04` ",
            },
            {
                "name": "Smart Buy",
                "location": "Port Said",
                "rating": 4.4,
                "image": " `https://images.unsplash.com/photo-1520607162513-77705c0f0d4a` ",
            },
            {
                "name": "Royal Market",
                "location": "Ismailia",
                "rating": 4.8,
                "image": " `https://images.unsplash.com/photo-1472851294608-062f824d29cc` ",
            },
            {
                "name": "Budget Store",
                "location": "Hurghada",
                "rating": 3.9,
                "image": " `https://images.unsplash.com/photo-1507914372368-b2b085b925a1` ",
            },
        ]

        products = [
            {
                "name": "Fresh Apples",
                "category": "Fruits",
                "price": 3.99,
                "image": " `https://images.unsplash.com/photo-1567306226416-28f0efdc88ce` ",
            },
            {
                "name": "Organic Bananas",
                "category": "Fruits",
                "price": 2.49,
                "image": " `https://images.unsplash.com/photo-1574226516831-e1dff420e37f` ",
            },
            {
                "name": "Tomatoes",
                "category": "Vegetables",
                "price": 1.99,
                "image": " `https://images.unsplash.com/photo-1546094096-0df4bcaaa337` ",
            },
            {
                "name": "Fresh Bread",
                "category": "Bakery",
                "price": 4.25,
                "image": " `https://images.unsplash.com/photo-1509440159596-0249088772ff` ",
            },
            {
                "name": "Cheddar Cheese",
                "category": "Dairy",
                "price": 5.50,
                "image": " `https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d` ",
            },
            {
                "name": "Orange Juice",
                "category": "Drinks",
                "price": 3.75,
                "image": " `https://images.unsplash.com/photo-1600271886742-f049cd5bba3f` ",
            },
            {
                "name": "Chocolate Cookies",
                "category": "Snacks",
                "price": 2.99,
                "image": " `https://images.unsplash.com/photo-1499636136210-6f4ee915583e` ",
            },
            {
                "name": "Potato Chips",
                "category": "Snacks",
                "price": 1.50,
                "image": " `https://images.unsplash.com/photo-1566478989037-eec170784d0b` ",
            },
            {
                "name": "Fresh Milk",
                "category": "Dairy",
                "price": 2.20,
                "image": " `https://images.unsplash.com/photo-1550583724-b2692b85b150` ",
            },
            {
                "name": "Coffee Beans",
                "category": "Drinks",
                "price": 8.99,
                "image": " `https://images.unsplash.com/photo-1495474472287-4d71bcdd2085` ",
            },
        ]

        created_users = []
        for idx, store_data in enumerate(stores, start=1):
            phone = f"+20{1000000000 + idx:010d}"
            user, created = User.objects.get_or_create(
                phone=phone,
                defaults={
                    "name": f"تاجر {idx}",
                    "email": f"trader{idx}@tijaratna.com",
                    "role": "trader",
                    "address": f"{store_data['location']}، مصر",
                },
            )
            user.set_password("password123")
            user.save(update_fields=["password"])
            if created:
                NotificationSettings.objects.get_or_create(user=user)
            created_users.append(user)

        for idx, store_data in enumerate(stores):
            owner = created_users[idx]
            store, _ = Store.objects.get_or_create(
                owner=owner,
                defaults={
                    "name": store_data["name"],
                    "logo_url": clean_url(store_data["image"]),
                    "description": f"متجر {store_data['name']} في {store_data['location']}",
                    "category": "متجر غذائي",
                    "phone_number": owner.phone,
                    "whatsapp_number": owner.phone,
                    "rating": store_data["rating"],
                    "is_featured": store_data["rating"] >= 4.5,
                    "location_lat": 30.0 + random.uniform(-0.4, 0.4),
                    "location_lng": 31.0 + random.uniform(-0.4, 0.4),
                },
            )

            for product_idx, product_data in enumerate(products, start=1):
                category_name = category_mapping.get(product_data["category"], "وجبات خفيفة")
                category = Category.objects.filter(name=category_name).first()
                if category is None:
                    category = Category.objects.create(name=category_name, icon="inventory_2")

                product_name = f"{product_data['name']} - {store.name}"
                product, _ = Product.objects.get_or_create(
                    name=product_name,
                    store=store,
                    defaults={
                        "category": category,
                        "description": f"{product_data['name']} متوفر في {store.name}",
                        "image_url": clean_url(product_data["image"]),
                        "is_popular": random.choice([True, False]),
                        "status": "in_stock",
                    },
                )

                price = Decimal(str(product_data["price"]))
                ProductVariant.objects.get_or_create(
                    product=product,
                    size="قطعة",
                    defaults={
                        "price": price,
                        "cost": (price * Decimal("0.75")).quantize(Decimal("0.01")),
                        "stock_quantity": random.randint(20, 200),
                        "sku": f"SKU-{idx + 1:02d}-{product_idx:02d}",
                    },
                )

        self.stdout.write(self.style.SUCCESS("Successfully seeded users, stores, and products!"))
