from book.models import PeopleImage, PokemonImage
from rest_framework import serializers


class PokemonImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonImage
        fields = ("url", "title", "original_label", "classified")


class InstagramTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeopleImage
        fields = ("title",)


class InstagramImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeopleImage
        fields = ("url", "selected")
