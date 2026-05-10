from django.urls import path
from .views import (
    OrderCreateListView, 
    OrderDetailView, 
    OrderStatusUpdateView, 
    AnalyticsDashboardView,
    OrderRatingCreateView
)

urlpatterns = [
    path('', OrderCreateListView.as_view(), name='order_list_create'),
    path('analytics/dashboard/', AnalyticsDashboardView.as_view(), name='analytics_dashboard'),
    path('rate/', OrderRatingCreateView.as_view(), name='order_rating_create'),
    path('<uuid:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('<uuid:pk>/status/', OrderStatusUpdateView.as_view(), name='order_status_update'),
]
