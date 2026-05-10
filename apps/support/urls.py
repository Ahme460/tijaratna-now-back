from django.urls import path
from .views import TicketCreateListView

urlpatterns = [
    path('tickets/', TicketCreateListView.as_view(), name='ticket_list_create'),
]
