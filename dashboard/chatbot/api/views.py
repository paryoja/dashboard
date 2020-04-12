"""Chatbot 에 사용할 API View Set."""

from chatbot import models
from chatbot.api.serializers import WikiSerializer
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """100개 단위로 Pagination 수행."""

    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


class WikiViewSet(viewsets.ModelViewSet):
    """위키 API View Set."""

    queryset = models.Wiki.objects.all()

    serializer_class = WikiSerializer
    pagination_class = StandardResultsSetPagination
