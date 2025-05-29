from django.db import models
from django.utils.translation import gettext_lazy as _

class HealthRecordChoices(models.TextChoices):
    """Defines possible status values for health records."""
    OPEN = 'OPEN', _('Open')
    CLOSED = 'CLOSED', _('Closed')
