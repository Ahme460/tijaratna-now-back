from rest_framework import generics, permissions
from .models import SupportTicket
from .serializers import SupportTicketSerializer

class TicketCreateListView(generics.ListCreateAPIView):
    serializer_class = SupportTicketSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return SupportTicket.objects.filter(user=self.request.user)
