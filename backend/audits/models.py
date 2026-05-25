from django.db import models
from emissions.models import NormalizedEmissionRecord


class AuditLog(models.Model):

    record = models.ForeignKey(
        NormalizedEmissionRecord,
        on_delete=models.CASCADE
    )

    action = models.CharField(max_length=100)

    previous_value = models.JSONField(
        null=True,
        blank=True
    )

    new_value = models.JSONField(
        null=True,
        blank=True
    )

    changed_by = models.CharField(max_length=255)

    timestamp = models.DateTimeField(
        auto_now_add=True
    )