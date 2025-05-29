from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from notifications.models import Notification
from notifications.serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    """
    Lists notifications for the logged-in user and marks them as read.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.select_related('sender').filter(receiver=self.request.user)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # Mark notifications as read after fetching
        self.get_queryset().filter(is_read=False).update(is_read=True)
        return response


class NotificationDeleteView(generics.DestroyAPIView):
    """
    Allows user to delete their notifications.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user)
