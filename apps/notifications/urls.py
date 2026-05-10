from django.urls import path
from .views import UserNotificationListView, MarkNotificationReadView

urlpatterns = [
    path('', UserNotificationListView.as_view(), name='user_notifications'),
    path('read/', MarkNotificationReadView.as_view(), name='mark_all_read'),
    path('read/<uuid:pk>/', MarkNotificationReadView.as_view(), name='mark_single_read'),
]
