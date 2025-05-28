from django.db import models
from django.contrib.auth import get_user_model
from aicuflow_proj.global_config.base_models import TimeStampedModel
from notifications.choices import NotificationTitleChoices

User = get_user_model()

class Notification(TimeStampedModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_receiver')
    title = models.CharField(max_length=255, choices=NotificationTitleChoices.choices)
    message = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.username} To {self.receiver.username}"
