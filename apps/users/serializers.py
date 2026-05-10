from rest_framework import serializers
from .models import User, NotificationSettings
from apps.stores.serializers import StoreSerializer
from apps.notifications.models import Notification

class NotificationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSettings
        fields = ('push_enabled', 'email_enabled', 'order_updates_enabled', 'offers_enabled')

class UserSerializer(serializers.ModelSerializer):
    notification_settings = NotificationSettingsSerializer(read_only=True)
    store = serializers.SerializerMethodField()
    count_notifications_not_read = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'phone', 'name', 'email', 'role', 'address', 'notification_settings', 'store', 'count_notifications_not_read', 'created_at')
        read_only_fields = ('id', 'created_at')

    def get_store(self, obj):
        # جلب أول متجر مرتبط بالمستخدم (باعتبار أن لكل مستخدم متجر واحد في العادة)
        store = obj.stores.first()
        if store:
            return StoreSerializer(store).data
        return None
    
    def get_count_notifications_not_read(self, obj):
        return Notification.objects.filter(user=obj, is_read=False).count()

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("كلمة المرور القديمة غير صحيحة.")
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "كلمتا المرور الجديدتان غير متطابقتين."})
        return data

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('phone', 'name', 'password', 'role', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            phone=validated_data['phone'],
            name=validated_data['name'],
            password=validated_data['password'],
            role=validated_data.get('role', 'trader'),
            email=validated_data.get('email')
        )
        # Create default notification settings
        NotificationSettings.objects.create(user=user)
        return user
