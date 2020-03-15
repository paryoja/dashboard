from rest_framework import viewsets

from book.api.serializers import PokemonImageSerializer
from .. import models


class PokemonImageViewSet(viewsets.ModelViewSet):
    queryset = models.PokemonImage.objects.all()[:10]
    serializer_class = PokemonImageSerializer
