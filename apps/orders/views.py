from django.db import models
from django.db.models import Sum, Count, Q, Avg
from rest_framework import generics, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order, OrderItem, OrderRating
from .serializers import (
    OrderSerializer, 
    OrderDetailSerializer, 
    OrderStatusUpdateSerializer,
    OrderRatingSerializer
)

from django.db.models import F, Sum, DecimalField, ExpressionWrapper



class OrderCreateListView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status','store__name']
    search_fields = ['id'] # سنستخدم هذا للبحث بـ order_number برمجياً

    def get_queryset(self):
        user = self.request.user
        order_type = self.request.query_params.get('type', 'placed')
        order_number = self.request.query_params.get('order_number')
        
        if order_type == 'received':
            queryset = Order.objects.filter(store__owner=user)
        else:
            queryset = Order.objects.filter(buyer=user)

        # البحث بـ order_number بكفاءة عالية (عن طريق الـ UUID)
        if order_number:
            try:
                # تحويل الرقم إلى hex (4 خانات)
                # بما أن الـ order_number هو int(id[:4], 16)
                order_hex = hex(int(order_number))[2:].zfill(4)
                queryset = queryset.filter(id__startswith=order_hex)
            except (ValueError, TypeError):
                pass

        return queryset.select_related('store', 'buyer')

class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(
            Q(buyer=user) | Q(store__owner=user)
        ).select_related('store', 'buyer').prefetch_related(
            'items__product', 
            'items__variant'
        )

class OrderStatusUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(Q(buyer=user) | Q(store__owner=user))

    def get_object(self):
        return super().get_object()

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        return Response({
            'id': str(order.id),
            'status': order.status,
            'created_at': order.created_at,
            'updated_at': order.updated_at
        })

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class OrderRatingCreateView(generics.CreateAPIView):
    """
    إضافة تقييم لطلب مكتمل
    """
    serializer_class = OrderRatingSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        order = serializer.validated_data['order']
        serializer.save(
            buyer=self.request.user,
            store=order.store
        )
        
        # تحديث متوسط تقييم المتجر
        store = order.store
        avg_rating = OrderRating.objects.filter(store=store).aggregate(Avg('rating'))['rating__avg']
        if avg_rating:
            store.rating = round(avg_rating, 2)
            store.save()

class AnalyticsDashboardView(APIView):
    permission_classes = (permissions.IsAuthenticated,)


    def revenue(self, user):
        revenue = (
            OrderItem.objects
            .filter(order__store__owner=user)
            .aggregate(
                total=Sum(
                    ExpressionWrapper(
                        (F('variant__price') - F('variant__cost')) * F('quantity'),
                        output_field=DecimalField()
                    )
                )
            )['total'] or 0
        )

        return revenue
  
    def get(self, request):
        user = request.user
        
        # Supplier/Owner analytics
        orders = Order.objects.filter(store__owner=user)
        total_sales = orders.filter(status='completed').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        total_orders = orders.count()

        
        # Best sellers
        from apps.products.models import Product
        best_sellers = OrderItem.objects.filter(order__store__owner=user)\
            .values('product__name')\
            .annotate(total_quantity=Sum('quantity'))\
            .order_by('-total_quantity')[:5]

        return Response({
            "total_sales": total_sales,
            "total_orders": total_orders,
            "revenue": self.revenue(user),
            "best_sellers": best_sellers
        })
