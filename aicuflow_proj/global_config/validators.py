from django.core.validators import RegexValidator
from aicuflow_proj.global_config.error_messages import PHONE_NUMBER_VALIDATION

phone_validator = RegexValidator(
    regex=r'^\+?\d{10,15}$',
    message=PHONE_NUMBER_VALIDATION
)
