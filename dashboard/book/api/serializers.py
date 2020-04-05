"""DRF Serializer."""

from book.models import PeopleImage, PokemonImage
from rest_framework import serializers


class PokemonImageSerializer(serializers.ModelSerializer):
    """Pokemon 이미지 Serializer."""

    class Meta:
        """Fields 설정."""

        model = PokemonImage
        fields = ("url", "title", "original_label", "classified")


class InstagramTextSerializer(serializers.ModelSerializer):
    """인스타그램 Text Serializer."""

    class Meta:
        """Fields 설정."""

        model = PeopleImage
        fields = ("title",)


class InstagramImageSerializer(serializers.ModelSerializer):
    """인스타그램 이미지 Serializer."""

    class Meta:
        """Fields 설정."""

        model = PeopleImage
        fields = ("url", "selected")
