from rest_framework import serializers
from .models import Category, Store

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'icon', 'parent', 'subcategories')

    def get_subcategories(self, obj):
        if obj.subcategories.exists():
            return CategorySerializer(obj.subcategories.all(), many=True).data
        return []

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'
        read_only_fields = ('id', 'owner', 'rating', 'created_at')

class StoreStatisticsSerializer(serializers.ModelSerializer):
    avg_order_value_placed = serializers.FloatField()
    avg_order_value_received = serializers.FloatField()
    new_orders_count = serializers.IntegerField()
    total_sales = serializers.FloatField()

    class Meta:
        model = Store
        fields = ('id', 'name', 'logo_url', 'avg_order_value_placed', 'avg_order_value_received', 'new_orders_count', 'total_sales')
