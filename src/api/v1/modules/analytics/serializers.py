from rest_framework import serializers
from .models import CampaignDataModel


class CampaignDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignDataModel
        fields = "__all__"
