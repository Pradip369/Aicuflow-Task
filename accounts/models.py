from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from accounts.choices import GenderChoices, UserRoleChoices
from aicuflow_proj.global_config.base_models import TimeStampedModel
from aicuflow_proj.global_config.validators import phone_validator

class User(AbstractUser):
    """Custom user model extending Django's AbstractUser with a role and unique email."""
    role = models.CharField(max_length=7, choices=UserRoleChoices.choices)
    email = models.EmailField(_('email address'), unique=True)


class PatientProfile(TimeStampedModel):
    """Profile model to store patient-specific information linked to a User."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    phone_number = models.CharField(max_length=15, validators=[phone_validator], blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GenderChoices.choices, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    insurance_details = models.JSONField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='patient_profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}"


class DoctorProfile(TimeStampedModel):
    """Profile model to store doctor-specific information linked to a User."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    phone_number = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=1, choices=GenderChoices.choices, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    license_number = models.CharField(max_length=100, blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='doctor_profiles/', blank=True, null=True)
    available_times = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Dr. {self.user.username}"
