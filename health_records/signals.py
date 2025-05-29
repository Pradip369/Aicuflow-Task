from django.db.models.signals import post_save
from django.dispatch import receiver
from aicuflow_proj.global_config.base_functions import send_notification_email
from health_records.models import HealthRecord, DoctorAnnotation
from notifications.models import Notification
from notifications.choices import NotificationTitleChoices

@receiver(post_save, sender=HealthRecord)
def notify_doctor_on_new_record(sender, instance, created, **kwargs):
    """Send notification and email to doctor when a new health record is created."""
    if created:
        Notification.objects.create(
            sender=instance.patient.user,
            receiver=instance.doctor.user,
            title=NotificationTitleChoices.NEW_PATIENT_ASSIGNED,
            message=f"A new health record has been created for patient {instance.patient.user.get_full_name()}."
        )

        if instance.doctor.user.email:
            send_notification_email(
                to_email=instance.doctor.user.email,
                subject=NotificationTitleChoices.NEW_PATIENT_ASSIGNED,
                message=f"A new health record has been created for patient {instance.patient.user.get_full_name()}."
            )


@receiver(post_save, sender=DoctorAnnotation)
def notify_patient_on_doctor_annotation(sender, instance, created, **kwargs):
    """Send notification and email to patient when doctor adds a new annotation."""
    if created:
        Notification.objects.create(
            sender=instance.doctor.user,
            receiver=instance.record.patient.user,
            title=NotificationTitleChoices.DOCTOR_ADDED_NEW_ANNOTATION,
            message=instance.comment
        )

    if instance.doctor.user.email:
        send_notification_email(
            to_email=instance.record.patient.user.email,
            subject=NotificationTitleChoices.DOCTOR_ADDED_NEW_ANNOTATION,
            message=f"A new annotation has been created from {instance.record.patient.user.get_full_name()}."
        )
