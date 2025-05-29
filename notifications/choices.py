from django.db import models
from django.utils.translation import gettext_lazy as _

class NotificationTitleChoices(models.TextChoices):
    """
    Predefined titles for notifications to standardize notification messages.
    """
    NEW_PATIENT_ASSIGNED = 'NEW_PATIENT_ASSIGNED', _('You have been assigned a new patient')
    DOCTOR_ADDED_NEW_ANNOTATION = 'DOCTOR_ADDED_NEW_ANNOTATION', _('A new annotation has been created')
