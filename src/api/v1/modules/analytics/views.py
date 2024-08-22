import csv
import io
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import CampaignDataModel
from .serializers import CampaignDataSerializer


class CSVUploadView(APIView):
    def post(self, request):
        file = request.FILES.get("file")
        if not file or not isinstance(file, InMemoryUploadedFile):
            return Response(
                {"error": "No file uploaded or file type is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            file_content = file.read().decode("utf-8")
            csv_reader = csv.DictReader(io.StringIO(file_content))

            for row in csv_reader:
                data, created = CampaignDataModel.objects.get_or_create(
                    revenue=row["revenue"],
                    defaults={
                        "customer_id": row["customer_id"],
                        "conversions": row["conversions"],
                        "status": row["status"],
                        "type": row["type"],
                        "category": row["category"],
                        "date": row["date"],
                        "impressions": row["impressions"],
                        "clicks": row["clicks"],
                    },
                )
                if not created:
                    for field, value in row.items():
                        setattr(data, field, value)
                    data.save()

            return Response(
                {"message": "CSV data successfully uploaded and processed"},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
