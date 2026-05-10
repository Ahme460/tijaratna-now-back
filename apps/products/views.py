from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch, Count, Q
from .models import Product, ProductVariant
from .serializers import ProductSerializer
from apps.stores.models import Store
from apps.stores.serializers import StoreSerializer
from django.shortcuts import get_object_or_404

from django.core.cache import cache

class ProductSuggestionsView(generics.ListAPIView):
    """
    عرض اقتراحات منتجات بشكل عشوائي أو البحث في كل المنتجات
    """
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description', 'category__name']

    def get_queryset(self):
        # التحقق من وجود بحث أو فلترة بالقسم
        search_query = self.request.query_params.get('search')
        category_id = self.request.query_params.get('category')
        
 
        if search_query or category_id:
            return Product.objects.select_related(
                'store', 'category'
            ).prefetch_related(
                'variants'
            ).distinct()
 
        cache_key = 'product_suggestions_ids'
        product_ids = cache.get(cache_key)

        if product_ids is None:
            queryset = Product.objects.annotate(
                sales_count=Count('order_items')
            ).filter(
                Q(sales_count__gt=10) | 
                Q(store__rating__gt=4.0)
            ).order_by('?')
 
            if not queryset.exists():
                queryset = Product.objects.order_by('?')[:20]
            
            product_ids = list(queryset.values_list('id', flat=True))
            cache.set(cache_key, product_ids, 120)   

        return Product.objects.filter(id__in=product_ids).select_related(
            'store', 'category'
        ).prefetch_related(
            'variants',
            'order_items'
        )

class StoreProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'is_popular', 'status']
    search_fields = ['name', 'description']

    def get_queryset(self):
        """
        الحصول على منتجات المتجر مع join للأحجام والعلاقات
        """
        queryset = Product.objects.filter(
            store_id=self.kwargs['store_id']
        ).select_related(
            'store',       
            'category'    
        ).prefetch_related(
            'variants'    
        )

        category_name = self.request.query_params.get('category_name')
        if category_name:
            queryset = queryset.filter(category__name=category_name)
        
        return queryset

    def list(self, request, *args, **kwargs):
        store = get_object_or_404(Store, id=self.kwargs['store_id'])
        store_data = StoreSerializer(store).data
        
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data['store'] = store_data
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'store': store_data,
            'results': serializer.data
        })

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        # البحث عن متجر المستخدم أو إنشاؤه إذا لم يكن موجوداً
        store, created = Store.objects.get_or_create(
            owner=self.request.user,
            defaults={'name': f"متجر {self.request.user.name or self.request.user.phone}"}
        )
        serializer.save(store=store)

class ProductDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
