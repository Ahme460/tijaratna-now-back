from rest_framework import serializers
from .models import Order, OrderItem, OrderRating
from apps.products.models import ProductVariant
from apps.products.serializers import ProductSerializer, ProductVariantSerializer
from apps.stores.serializers import StoreSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'variant', 'quantity', 'price_at_order')
        read_only_fields = ('id', 'price_at_order')

class OrderItemDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    variant = ProductVariantSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'variant', 'quantity', 'price_at_order')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    name_store = serializers.CharField(source='store.name', read_only=True)


    class Meta:
        model = Order
        fields = ('id', 'order_number', 'buyer', 'store', 'status', 'total_amount', "name_store",'items', 'created_at')
        read_only_fields = ('id', 'order_number', 'buyer', 'status', 'total_amount', 'created_at')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        total_amount = 0
        
        # Calculate total amount
        for item_data in items_data:
            variant = item_data['variant']
            total_amount += variant.price * item_data['quantity']

        order = Order.objects.create(
            buyer=self.context['request'].user,
            total_amount=total_amount,
            **validated_data
        )

        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                price_at_order=item_data['variant'].price,
                **item_data
            )
        
        return order

class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemDetailSerializer(many=True, read_only=True)
    store = StoreSerializer(read_only=True)
    is_buyer = serializers.SerializerMethodField()
    is_supplier = serializers.SerializerMethodField()
    has_rated = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', "order_number",'buyer', 'store', 'status', 'total_amount', 'items', 'is_buyer', 'is_supplier', 'has_rated', 'created_at')
        read_only_fields = ('id', "order_number",'buyer', 'status', 'total_amount', 'created_at')

    def get_is_buyer(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.buyer == request.user
        return False

    def get_is_supplier(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.store.owner == request.user
        return False

    def get_has_rated(self, obj):
        return hasattr(obj, 'rating')

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('status',)

class OrderRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRating
        fields = ('id', 'order', 'buyer', 'store', 'rating', 'comment', 'created_at')
        read_only_fields = ('id', 'buyer', 'store', 'created_at')

    def validate_order(self, value):
        # التأكد من أن الطلب مكتمل
        if value.status not in ['completed', 'delivered']:
            raise serializers.ValidationError("يمكنك تقييم الطلبات المكتملة فقط.")
        
        # التأكد من أن المستخدم هو صاحب الطلب
        if value.buyer != self.context['request'].user:
            raise serializers.ValidationError("لا يمكنك تقييم طلب لا يخصك.")
            
        # التأكد من عدم وجود تقييم سابق
        if hasattr(value, 'rating'):
            raise serializers.ValidationError("تم تقييم هذا الطلب مسبقاً.")
            
        return value
