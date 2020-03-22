from book.models import PokemonImage
from rest_framework import serializers


class PokemonImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonImage
        fields = ("url", "title", "original_label", "classified")
