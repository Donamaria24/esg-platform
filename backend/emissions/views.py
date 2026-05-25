from rest_framework.decorators import (
    api_view,
    permission_classes
)

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from django.http import HttpResponse

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from .models import (
    NormalizedEmissionRecord
)


# PUBLIC DASHBOARD SUMMARY API

@api_view(['GET'])
def emission_summary(request):

    records = (
        NormalizedEmissionRecord.objects.all()
    )

    total_records = records.count()

    suspicious_count = records.filter(
        suspicious_flag=True
    ).count()

    total_emissions = sum(
        r.calculated_emission
        for r in records
    )

    latest_records = []

    for r in records.order_by('-id')[:10]:

        latest_records.append({

            "activity_type":
                r.activity_type,

            "value":
                r.normalized_value,

            "unit":
                r.normalized_unit,

            "emission":
                r.calculated_emission,

            "suspicious":
                r.suspicious_flag
        })

    return Response({

        "total_records":
            total_records,

        "suspicious_records":
            suspicious_count,

        "total_emissions":
            total_emissions,

        "latest_records":
            latest_records
    })


# PROTECTED REVIEW API

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_record(request, record_id):

    record = get_object_or_404(
        NormalizedEmissionRecord,
        id=record_id
    )

    status_value = request.data.get(
        'status'
    )

    comment = request.data.get(
        'comment'
    )

    record.review_status = status_value

    record.review_comment = comment

    record.save()

    return Response({
        "message":
            "Review updated successfully"
    })


# PROTECTED PDF EXPORT API

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_pdf_report(request):

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = (
        'attachment; filename="esg_report.pdf"'
    )

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "ESG Emissions Report",
        styles['Title']
    )

    elements.append(title)

    elements.append(
        Spacer(1, 20)
    )

    records = (
        NormalizedEmissionRecord.objects.all()
    )

    total_emissions = sum(
        r.calculated_emission
        for r in records
    )

    suspicious_count = records.filter(
        suspicious_flag=True
    ).count()

    elements.append(

        Paragraph(
            f"Total Records: "
            f"{records.count()}",
            styles['BodyText']
        )
    )

    elements.append(

        Paragraph(
            f"Suspicious Records: "
            f"{suspicious_count}",
            styles['BodyText']
        )
    )

    elements.append(

        Paragraph(
            f"Total Emissions: "
            f"{total_emissions}",
            styles['BodyText']
        )
    )

    doc.build(elements)

    return response