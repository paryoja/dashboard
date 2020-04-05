from typing import Any, Dict

from book import models
from django.views.generic import ListView, TemplateView


class CurrentPageListView(ListView):
    """
    Navbar 에서 current_page 를 세팅하는 view

    :param current_page
    """

    current_page = None

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["current_page"] = self.current_page
        return context


class CurrentPageTemplateView(TemplateView):
    current_page = None

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["current_page"] = self.current_page
        return context


class WebStackListView(CurrentPageListView):
    current_page = "web_stack"
    template_name = "book/link/web_stack.html"
    queryset = models.Link.objects.filter(content_type="Web")


class BookmarkListView(CurrentPageListView):
    current_page = "link"
    template_name = "book/link/link.html"
    queryset = models.Link.objects.exclude(content_type="Web")


class WineListView(CurrentPageListView):
    current_page = "wine"
    template_name = "book/wine.html"
    model = models.Wine


class RecommendBookListView(CurrentPageListView):
    current_page = "recommend_book"
    template_name = "book/investment/recommend_book.html"
    model = models.Book


class IndexTemplateView(CurrentPageTemplateView):
    current_page = "index"
    template_name = "book/index.html"


class AlgorithmTemplateView(CurrentPageTemplateView):
    current_page = "algorithm"
    template_name = "book/algorithm.html"


class LeadingStockTemplateView(CurrentPageTemplateView):
    current_page = "leading_stocks"
    template_name = "book/investment/leading_stocks.html"
