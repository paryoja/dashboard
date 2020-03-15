from rest_framework import serializers

from book.models import PokemonImage


class PokemonImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonImage
        fields = ("url", "title", "original_label", "classified")
