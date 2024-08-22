import uuid
from django.db import models


class CampaignDataModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_id = models.CharField(max_length=255)
    revenue = models.DecimalField(max_digits=15, decimal_places=2)
    conversions = models.IntegerField()
    status = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    date = models.DateField()
    impressions = models.IntegerField()
    clicks = models.IntegerField()

    def __str__(self):
        return f"{self.customer_id} - {self.date}"
