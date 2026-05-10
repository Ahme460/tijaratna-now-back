from rest_framework import serializers
from .models import SupportTicket

class SupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = '__all__'
        read_only_fields = ('id', 'user', 'status', 'created_at')

    def create(self, validated_data):
        return SupportTicket.objects.create(
            user=self.context['request'].user,
            **validated_data
        )
