from django.urls import path
from .views import CSVUploadView, ConversionRateView

urlpatterns = [
    path("analytics/upload-csv/", CSVUploadView.as_view(), name="upload-csv"),
    path("conversion-rate/", ConversionRateView.as_view(), name="conversion-rate"),
]
