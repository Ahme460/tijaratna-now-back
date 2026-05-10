from rest_framework import serializers
from .models import Product, ProductVariant

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'
        read_only_fields = ('id', 'product')

class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'store', 'category', 'name', 'description', 'image_url', 'is_popular', 'status', 'variants', 'created_at')
        read_only_fields = ('id', 'store', 'created_at')

    def create(self, validated_data):
        variants_data = validated_data.pop('variants')
        product = Product.objects.create(**validated_data)
        for variant_data in variants_data:
            ProductVariant.objects.create(product=product, **variant_data)
        return product

    def update(self, instance, validated_data):
        variants_data = validated_data.pop('variants', None)
        
        # تحديث بيانات المنتج الأساسية
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # تحديث المتغيرات إذا تم توفيرها
        if variants_data is not None:
            # حذف المتغيرات القديمة وإضافة الجديدة
            instance.variants.all().delete()
            for variant_data in variants_data:
                ProductVariant.objects.create(product=instance, **variant_data)
        
        return instance
