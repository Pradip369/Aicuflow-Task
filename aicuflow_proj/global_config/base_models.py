from django.db import models

class TimeStampedModel(models.Model):
    """
    Abstract model that adds created and updated timestamp fields to a model.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

