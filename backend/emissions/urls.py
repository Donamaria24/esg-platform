from django.urls import path

from .views import (
    emission_summary,
    review_record,
    export_pdf_report
)

urlpatterns = [

    path(
        'summary/',
        emission_summary
    ),

    path(
        'review/<int:record_id>/',
        review_record
    ),

    path(
        'export/pdf/',
        export_pdf_report
    ),
]