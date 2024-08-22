from django.urls import path
from .views import CSVUploadView

urlpatterns = [
    path("analytics/upload-csv/", CSVUploadView.as_view(), name="upload-csv"),
]
