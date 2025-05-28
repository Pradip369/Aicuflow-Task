from django.urls import path
from notifications.views import NotificationListView, NotificationDeleteView

app_name = 'notification'

urlpatterns = [
    path('notification_list/', NotificationListView.as_view(), name='notification_list'),
    path('notification_delete/<int:pk>/', NotificationDeleteView.as_view(), name='notification_delete')
]
