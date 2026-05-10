from django.urls import path
from .views import CategoryListView, StoreListCreateView, StoreDetailUpdateDeleteView, MyStoreView, StoreStatisticsView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('my-store/', MyStoreView.as_view(), name='my_store'),
    path('my-store/statistics/', StoreStatisticsView.as_view(), name='store_statistics'),
    path('', StoreListCreateView.as_view(), name='store_list_create'),
    path('<uuid:pk>/', StoreDetailUpdateDeleteView.as_view(), name='store_detail_update_delete'),
]
