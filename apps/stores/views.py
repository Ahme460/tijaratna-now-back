from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Sum, Q
from django.utils import timezone
from datetime import timedelta
from .models import Category, Store
from .serializers import CategorySerializer, StoreSerializer, StoreStatisticsSerializer
from apps.orders.models import Order

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None

class StoreListCreateView(generics.ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'is_featured']
    search_fields = ['name', 'description']

    def get_queryset(self):
        return super().get_queryset().exclude(owner=self.request.user)
    

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class StoreDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

class MyStoreView(generics.RetrieveUpdateAPIView):
    serializer_class = StoreSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        # الحصول على المتجر الخاص بالمستخدم الحالي
        store = Store.objects.filter(owner=self.request.user).first()
        if not store:

            from django.http import Http404
            raise Http404("لا يوجد متجر مرتبط بهذا الحساب.")
        return store

class StoreStatisticsView(generics.RetrieveAPIView):
    serializer_class = StoreStatisticsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        store = Store.objects.filter(owner=user).first()
        if not store:
            from django.http import Http404
            raise Http404("لا يوجد متجر مرتبط بهذا الحساب.")
        
        # 1. متوسط سعر الأوردر اللي أنا بعمله (المشتريات)
        avg_placed = Order.objects.filter(buyer=user).aggregate(Avg('total_amount'))['total_amount__avg'] or 0
        
        # 2. متوسط سعر الأوردر اللي بيطلب مني (المبيعات)
        avg_received = Order.objects.filter(store=store).aggregate(Avg('total_amount'))['total_amount__avg'] or 0
        
        # 3. إجمالي المبيعات (الطلبات المكتملة فقط كمثال)
        total_sales = Order.objects.filter(store=store, status='completed').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        
        # 4. عدد الطلبات الجديدة (آخر يومين)
        two_days_ago = timezone.now() - timedelta(days=2)
        new_orders_count = Order.objects.filter(
            store=store, 
            created_at__gte=two_days_ago,

        ).count()

        # إضافة البيانات للكائن بشكل مؤقت للسيرياليزر
        store.avg_order_value_placed = avg_placed
        store.avg_order_value_received = avg_received
        store.total_sales = total_sales
        store.new_orders_count = new_orders_count
        
        return store
