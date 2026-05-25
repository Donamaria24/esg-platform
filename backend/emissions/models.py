from django.db import models
from companies.models import Company
from ingestion.models import DataSource


class RawEmissionRecord(models.Model):
    def __str__(self):
        return f"Raw Record {self.id}"

    datasource = models.ForeignKey(
        DataSource,
        on_delete=models.CASCADE
    )

    raw_json = models.JSONField()

    ingestion_status = models.CharField(
        max_length=50,
        default='pending'
    )

    error_message = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class NormalizedEmissionRecord(models.Model):
    def __str__(self):
        return (
            f"{self.activity_type} - "
            f"{self.normalized_value} "
            f"{self.normalized_unit}"
        )
    
    review_status = models.CharField(
        max_length=20,
        default='pending'
    )
    review_comment = models.TextField(
        blank=True,
        null=True
    )

    REVIEW_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )

    datasource = models.ForeignKey(
        DataSource,
        on_delete=models.CASCADE
    )

    scope_category = models.CharField(max_length=20)

    activity_type = models.CharField(max_length=100)

    original_value = models.FloatField()

    original_unit = models.CharField(max_length=50)

    normalized_value = models.FloatField()

    normalized_unit = models.CharField(max_length=50)

    emission_factor = models.FloatField(default=0)

    calculated_emission = models.FloatField(default=0)

    suspicious_flag = models.BooleanField(default=False)

    review_status = models.CharField(
        max_length=20,
        choices=REVIEW_STATUS,
        default='pending'
    )

    locked_for_audit = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True
    )