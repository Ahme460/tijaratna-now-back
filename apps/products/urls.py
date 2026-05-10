from django.urls import path
from .views import (
    StoreProductListView, 
    ProductListCreateView, 
    ProductDetailUpdateDeleteView,
    ProductSuggestionsView
)

urlpatterns = [
    path('suggestions/', ProductSuggestionsView.as_view(), name='product_suggestions'),
    path('store/<uuid:store_id>/', StoreProductListView.as_view(), name='store_product_list'),
    path('', ProductListCreateView.as_view(), name='product_list_create'),
    path('<uuid:pk>/', ProductDetailUpdateDeleteView.as_view(), name='product_detail_update_delete'),
]
