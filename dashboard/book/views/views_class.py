"""Class View 를 이용한 view 구현."""
from typing import Any, Dict

from book import models
from django.views.generic import ListView, TemplateView


class CurrentPageListView(ListView):
    # noinspection PyUnresolvedReferences
    """
    Navbar 에서 current_page 를 세팅하는 ListView.

    :param current_page: 현재 page
    :type current_page: str
    """

    current_page: str = None

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        current_page 를 context 에 추가.

        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        context["current_page"] = self.current_page
        return context


class CurrentPageTemplateView(TemplateView):
    # noinspection PyUnresolvedReferences
    """
    Navbar 에서 current_page 를 세팅하는 ListView.

    :param current_page: 현재 page
    :type current_page: str
    """

    current_page = None

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        current_page 를 context 에 추가.

        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        context["current_page"] = self.current_page
        return context


class WebStackListView(CurrentPageListView):
    """WebStack."""

    current_page = "web_stack"
    template_name = "book/link/web_stack.html"
    queryset = models.Link.objects.filter(content_type="Web")


class BookmarkListView(CurrentPageListView):
    """북마크 뷰."""

    current_page = "link"
    template_name = "book/link/link.html"
    queryset = models.Link.objects.exclude(content_type="Web")


class WineListView(CurrentPageListView):
    """와인 뷰."""

    current_page = "wine"
    template_name = "book/wine.html"
    model = models.Wine


class RecommendBookListView(CurrentPageListView):
    """책 정보 뷰."""

    current_page = "recommend_book"
    template_name = "book/investment/recommend_book.html"
    model = models.Book


class PaperListViwew(CurrentPageListView):
    """논문 리스트 뷰."""

    current_page = "paper"
    template_name = "book/study/paper.html"
    model = models.Paper


# Template Views
class IndexTemplateView(CurrentPageTemplateView):
    """첫 페이지."""

    current_page = "index"
    template_name = "book/index.html"


class AlgorithmTemplateView(CurrentPageTemplateView):
    """알고리즘 정보."""

    current_page = "algorithm"
    template_name = "book/algorithm.html"


class LeadingStockTemplateView(CurrentPageTemplateView):
    """주식 정보."""

    current_page = "leading_stocks"
    template_name = "book/investment/leading_stocks.html"


class TodoTemplateView(CurrentPageTemplateView):
    """할일 정보."""

    current_page = "todo"
    template_name = "book/todo.html"


class SlideTemplateView(CurrentPageTemplateView):
    """슬라이드 정보."""

    current_page = "slide"
    template_name = "book/study/slide.html"


class ColabTemplateView(CurrentPageTemplateView):
    """Colab."""

    current_page = "colab"
    template_name = "book/study/colab.html"


class IdeaTemplateView(CurrentPageTemplateView):
    """아이디어 정보."""

    current_page = "idea"
    template_name = "book/idea.html"


class ChatbotTemplateView(CurrentPageTemplateView):
    """Chatbot 관련 뷰."""

    current_page = "chatbot"
    template_name = "book/chatbot/chatbot.html"
