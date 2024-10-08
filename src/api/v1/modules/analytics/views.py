import csv
import io
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import CampaignDataModel
from .serializers import CampaignDataSerializer
from django.db.models import Count, Sum
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime


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


class ConversionRateView(APIView):
    def get(self, request):
        data = CampaignDataModel.objects.all()

        conversion_rates = [
            {
                "customer_id": item.customer_id,
                "conversion_rate": (
                    (item.conversions / item.impressions) * 100
                    if item.impressions > 0
                    else 0
                ),
            }
            for item in data
        ]

        if not conversion_rates:
            return Response({"error": "No data available"}, status=404)

        highest_conversion_rate = max(
            conversion_rates, key=lambda x: x["conversion_rate"]
        )
        lowest_conversion_rate = min(
            conversion_rates, key=lambda x: x["conversion_rate"]
        )

        return Response(
            {
                "conversion_rates": conversion_rates,
                "highest_conversion_rate": highest_conversion_rate,
                "lowest_conversion_rate": lowest_conversion_rate,
            },
            status=status.HTTP_200_OK,
        )


class StatusDistributionView(APIView):
    def get(self, request):
        try:
            status_distribution = CampaignDataModel.objects.values("status").annotate(
                count=Count("status")
            )

            if not status_distribution:
                return Response(
                    {"error": "No data found for status distribution."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            return Response(status_distribution)

        except ObjectDoesNotExist:
            return Response(
                {
                    "error": "Database query failed. Check if the table exists and is populated."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CategoryTypePerformanceView(APIView):
    def get(self, request):
        try:
            performance_data = (
                CampaignDataModel.objects.values("category", "type")
                .annotate(
                    total_revenue=Sum("revenue"),
                    total_conversions=Sum("conversions"),
                    total_impressions=Sum("impressions"),
                    total_clicks=Sum("clicks"),
                    count=Count("id"),
                )
                .order_by("category", "type")
            )

            if not performance_data:
                return Response(
                    {"error": "No data found for category-type performance."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            return Response(performance_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FilteredAggregationView(APIView):
    def get(self, request):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        category = request.query_params.get("category")

        if not start_date or not end_date:
            return Response(
                {"error": "Start date and end date are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        valid_categories = CampaignDataModel.objects.values_list(
            "category", flat=True
        ).distinct()

        if not category:
            return Response(
                {
                    "error": "Category is required.",
                    "valid_categories": valid_categories,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        category = category.upper()

        if category not in valid_categories:
            return Response(
                {
                    "error": f"Invalid category '{category}'.",
                    "valid_categories": valid_categories,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        filtered_data = CampaignDataModel.objects.filter(
            date__range=[start_date, end_date], category=category
        )

        aggregated_data = filtered_data.aggregate(
            total_revenue=Sum("revenue"),
            total_conversions=Sum("conversions"),
            total_impressions=Sum("impressions"),
            total_clicks=Sum("clicks"),
        )

        return Response(aggregated_data, status=status.HTTP_200_OK)
