from django.core.validators import RegexValidator
from aicuflow_proj.global_config.error_messages import PHONE_NUMBER_VALIDATION

# Validator to ensure phone numbers have 10-15 digits, optionally starting with a plus (+).
# -----------------------------------------------
phone_validator = RegexValidator(
    regex=r'^\+?\d{10,15}$',
    message=PHONE_NUMBER_VALIDATION
)
