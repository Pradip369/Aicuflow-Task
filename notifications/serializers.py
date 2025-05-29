from rest_framework import serializers
from notifications.models import Notification
from accounts.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model.
    """
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'

