import random
from django.core.management.base import BaseCommand
from apps.users.models import User
from apps.stores.models import Category, Store
from apps.products.models import Product, ProductVariant
from apps.orders.models import Order, OrderItem

class Command(BaseCommand):
    help = 'Seeds the database with only categories'

    def handle(self, *args, **kwargs):
        # self.stdout.write('Clearing old data...')
        
        # # Clear existing data in correct order
        # OrderItem.objects.all().delete()
        # Order.objects.all().delete()
        # ProductVariant.objects.all().delete()
        # Product.objects.all().delete()
        # Store.objects.all().delete()
        # Category.objects.all().delete()
        # # Note: We keep users as they might be needed for admin access
        
        # self.stdout.write(self.style.SUCCESS('Data cleared!'))
        # self.stdout.write('Seeding categories...')

        # Food related categories
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
        
        for cat_data in food_categories:
            Category.objects.get_or_create(
                name=cat_data['name'], 
                defaults={'icon': cat_data['icon']}
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded categories!'))
