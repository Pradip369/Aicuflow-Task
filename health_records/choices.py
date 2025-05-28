from django.db import models
from django.utils.translation import gettext_lazy as _

class HealthRecordChoices(models.TextChoices):
    OPEN = 'OPEN', _('Open')
    CLOSED = 'CLOSED', _('Closed')

