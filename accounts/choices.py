from django.db import models
from django.utils.translation import gettext_lazy as _

class GenderChoices(models.TextChoices):
    """Defines available gender options for user profiles."""
    MALE = 'M', _('Male')
    FEMALE = 'F', _('Female')
    OTHER = 'O', _('Other')

class UserRoleChoices(models.TextChoices):
    """Defines user roles for access control and permissions."""
    ADMIN = 'ADMIN', _('Admin')
    DOCTOR = 'DOCTOR', _('Doctor'),
    PATIENT = 'PATIENT', _('Patient')
