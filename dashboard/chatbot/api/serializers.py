"""DRF Serializer."""

from chatbot import models
from rest_framework import serializers


class WikiSerializer(serializers.ModelSerializer):
    """Wiki 정보 Serializer."""

    class Meta:
        """Fields 설정."""

        model = models.Wiki
        fields = ("link", "title", "source")
