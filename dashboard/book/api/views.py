from book.api.serializers import (
    InstagramImageSerializer,
    InstagramTextSerializer,
    PokemonImageSerializer,
)
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .. import models


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


class PokemonImageViewSet(viewsets.ModelViewSet):
    queryset = models.PokemonImage.objects.filter(classified="little").order_by("id")
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = PokemonImageSerializer
    pagination_class = StandardResultsSetPagination

    filterset_fields = ("title", "url")


class InstagramTextViewSet(viewsets.ModelViewSet):
    queryset = models.PeopleImage.objects.order_by("id")
    permission_classes = [IsAuthenticated]

    serializer_class = InstagramTextSerializer
    pagination_class = StandardResultsSetPagination


class InstagramImageViewSet(viewsets.ModelViewSet):
    queryset = models.PeopleImage.objects.order_by("id")
    permission_classes = [IsAuthenticated]

    serializer_class = InstagramImageSerializer
    pagination_class = StandardResultsSetPagination

    filterset_fields = ("selected",)
