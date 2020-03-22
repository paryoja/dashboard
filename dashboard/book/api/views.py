from book.api.serializers import PokemonImageSerializer
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .. import models


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


class PokemonImageViewSet(viewsets.ModelViewSet):
    queryset = models.PokemonImage.objects.filter(classified="little")
    serializer_class = PokemonImageSerializer
    pagination_class = StandardResultsSetPagination

    filter_fields = ("title", "url")
