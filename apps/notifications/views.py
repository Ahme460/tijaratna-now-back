from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notification
from .serializers import NotificationSerializer

class UserNotificationListView(generics.ListAPIView):
    """
    عرض الإشعارات الخاصة بالمستخدم الحالي
    """
    serializer_class = NotificationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class MarkNotificationReadView(APIView):
    """
    تحويل إشعار معين أو جميع الإشعارات إلى مقروءة
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk=None):
        if pk:
            # تحويل إشعار واحد فقط لمقروء
            try:
                notification = Notification.objects.get(pk=pk, user=request.user)
                notification.is_read = True
                notification.save()
                return Response({"detail": "تم تحديث الإشعار كـ مقروء."}, status=status.HTTP_200_OK)
            except Notification.DoesNotExist:
                return Response({"detail": "الإشعار غير موجود."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # تحويل جميع الإشعارات غير المقروءة لمقروءة
            Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
            return Response({"detail": "تم تحديث جميع الإشعارات كـ مقروءة."}, status=status.HTTP_200_OK)
