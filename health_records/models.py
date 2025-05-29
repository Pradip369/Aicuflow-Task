from django.db import models
from health_records.choices import HealthRecordChoices
from accounts.models import PatientProfile, DoctorProfile
from aicuflow_proj.global_config.base_models import TimeStampedModel

class HealthRecord(TimeStampedModel):
    """Model representing a patient's health record, including vitals, diagnosis, and related details."""
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='patient_health_records')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, related_name='doctor_health_records')
    visit_reason = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    blood_pressure = models.CharField(max_length=20, blank=True, null=True)
    heart_rate = models.PositiveIntegerField(null=True, blank=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    respiratory_rate = models.PositiveIntegerField(null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    diagnosis = models.TextField(blank=True)
    prescriptions = models.TextField(blank=True)
    recommended_tests = models.TextField(blank=True)
    attachment = models.FileField(upload_to='health_records/', null=True, blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=HealthRecordChoices.choices, default='open')

    def __str__(self):
        return f"{self.patient} | {self.doctor}"


class DoctorAnnotation(TimeStampedModel):
    """Model for doctors' annotations on health records, including attachments."""
    record = models.ForeignKey(HealthRecord, on_delete=models.CASCADE, related_name='annotations')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    comment = models.TextField()
    attachment = models.FileField(upload_to='health_records/', null=True, blank=True)

    def __str__(self):
        return f"{self.record}"
