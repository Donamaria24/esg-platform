import pandas as pd

from rest_framework import serializers
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from companies.models import Company
from ingestion.models import DataSource

from emissions.models import (
    RawEmissionRecord,
    NormalizedEmissionRecord
)


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_sap(request):

    if request.method == 'GET':
        return Response({
            "message": "Ready for file upload"
        })

    if 'file' not in request.FILES:
        return Response({
            "error": "No file uploaded"
        }, status=400)

    uploaded_file = request.FILES['file']

    try:

        # RESET FILE POINTER
        uploaded_file.seek(0)

        # READ CSV
        df = pd.read_csv(uploaded_file)

        # RESET AGAIN
        uploaded_file.seek(0)

        # CREATE COMPANY
        company, created = Company.objects.get_or_create(
            name="Demo Company"
        )

        # CREATE DATA SOURCE
        datasource = DataSource.objects.create(
            company=company,
            source_type='sap',
            uploaded_file=uploaded_file
        )

        rows_count = 0

        # PROCESS EACH ROW
        for _, row in df.iterrows():

            # SAVE RAW RECORD
            RawEmissionRecord.objects.create(
                datasource=datasource,
                raw_json=row.to_dict(),
                ingestion_status='success'
            )

            # EXTRACT VALUES
            quantity = float(row.get('quantity', 0))
            unit = str(row.get('unit', '')).lower()
            fuel_type = row.get('fuel_type', 'Unknown')

            # NORMALIZATION
            normalized_value = quantity
            normalized_unit = unit

            # gallons → liters
            if unit == 'gallons':
                normalized_value = quantity * 3.78541
                normalized_unit = 'liters'

            # EMISSION CALCULATION
            emission_factor = 2.5

            calculated_emission = (
                normalized_value * emission_factor
            )

            # SUSPICIOUS DETECTION
            suspicious_flag = False

            if quantity > 10000:
                suspicious_flag = True

            # SAVE NORMALIZED RECORD
            NormalizedEmissionRecord.objects.create(
                company=company,
                datasource=datasource,

                scope_category='Scope 1',
                activity_type=fuel_type,

                original_value=quantity,
                original_unit=unit,

                normalized_value=normalized_value,
                normalized_unit=normalized_unit,

                emission_factor=emission_factor,
                calculated_emission=calculated_emission,

                suspicious_flag=suspicious_flag
            )

            rows_count += 1

        return Response({
            "message": "SAP file uploaded successfully",
            "rows_processed": rows_count
        })

    except Exception as e:
        return Response({
            "error": str(e)
        }, status=500)