from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(slug_field = 'username', read_only=True) # può essere fatto con user id?

    class Meta:
        model = Notification
        fields = ['id', 'sender', 'notification_type', 'message', 'created_at', 'is_read']