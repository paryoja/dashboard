"""Class View 를 이용한 view 구현."""
from typing import Any, Dict

from book import forms, models
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, TemplateView
from django.views.generic.base import ContextMixin


class CurrentPageMixin(ContextMixin):
    """Current Page 를 추가해주는 mixin."""

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


class WebStackListView(ListView, CurrentPageMixin):
    """WebStack."""

    current_page = "web_stack"
    template_name = "book/link/web_stack.html"
    queryset = models.Link.objects.filter(content_type="Web")


class BookmarkListView(ListView, CurrentPageMixin):
    """북마크 뷰."""

    current_page = "link"
    template_name = "book/link/link.html"
    queryset = models.Link.objects.exclude(content_type="Web")


class WineListView(ListView, CurrentPageMixin):
    """와인 뷰."""

    current_page = "wine"
    template_name = "book/wine.html"
    model = models.Wine


class SavingsView(ListView, CurrentPageMixin, LoginRequiredMixin, UserPassesTestMixin):
    """예적금 리스트."""

    current_page = "savings"
    template_name = "book/investment/savings.html"
    queryset = models.Saving.objects.order_by("-date")

    def test_func(self):
        """Check whether user is superuser or not."""
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Form 을 context 에 추가."""
        context = super().get_context_data(**kwargs)

        chart_map = {}

        for obj in self.queryset:
            chart_map[obj.date] = chart_map.get(obj.date, 0) + obj.interest_minus_tax

        chart_label = sorted([label for label in chart_map])
        chart_amount = [chart_map[label] for label in chart_label]

        context["chart_label"] = [label.strftime("%Y-%m-%d") for label in chart_label]
        context["chart_amount"] = chart_amount

        return context


class MomentumView(ListView, CurrentPageMixin, LoginRequiredMixin, UserPassesTestMixin):
    """모멘텀 투자 정보 리스트."""

    current_page = "momentum"
    template_name = "book/investment/momentum.html"
    queryset = models.MomentumSummary.objects.order_by("-date")

    def test_func(self):
        """Check whether user is superuser or not."""
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Form 을 context 에 추가."""
        context = super().get_context_data(**kwargs)

        return context


class RecommendBookListView(ListView, CurrentPageMixin):
    """책 정보 뷰."""

    current_page = "recommend_book"
    template_name = "book/investment/recommend_book.html"
    model = models.Book


class PaperListViwew(ListView, CurrentPageMixin):
    """논문 리스트 뷰."""

    current_page = "paper"
    template_name = "book/study/paper.html"
    model = models.Paper


# Template Views
class IndexTemplateView(TemplateView, CurrentPageMixin):
    """첫 페이지."""

    current_page = "index"
    template_name = "book/index.html"


class AlgorithmTemplateView(TemplateView, CurrentPageMixin):
    """알고리즘 정보."""

    current_page = "algorithm"
    template_name = "book/algorithm.html"


class LeadingStockTemplateView(TemplateView, CurrentPageMixin):
    """주식 정보."""

    current_page = "leading_stocks"
    template_name = "book/investment/leading_stocks.html"


class TodoTemplateView(ListView, CurrentPageMixin):
    """할일 정보."""

    model = models.TodoItem
    current_page = "todo"
    template_name = "book/todo.html"


class SlideTemplateView(TemplateView, CurrentPageMixin):
    """슬라이드 정보."""

    current_page = "slide"
    template_name = "book/study/slide.html"


class ColabTemplateView(TemplateView, CurrentPageMixin):
    """Colab."""

    current_page = "colab"
    template_name = "book/study/colab.html"


class IdeaTemplateView(TemplateView, CurrentPageMixin):
    """아이디어 정보."""

    current_page = "idea"
    template_name = "book/idea.html"


class ChatbotTemplateView(TemplateView, CurrentPageMixin):
    """Chatbot 관련 뷰."""

    current_page = "chatbot"
    template_name = "book/chatbot/chatbot.html"


class QueryView(TemplateView, CurrentPageMixin):
    """Query View."""

    current_page = "query"
    template_name = "book/chatbot/query.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Form 을 context 에 추가."""
        context = super().get_context_data(**kwargs)

        context["form"] = forms.QueryForm()
        return context


class RLView(ListView, CurrentPageMixin):
    """Reinforcement Learning View."""

    queryset = models.Lecture.objects.filter(
        class_name=models.Lecture.LectureClassChoices.RL
    ).order_by("-number")
    current_page = "reinforcement"
    template_name = "book/study/reinforcement.html"


class NLPView(ListView, CurrentPageMixin):
    """Natural Language Processing View."""

    queryset = models.Lecture.objects.filter(
        class_name=models.Lecture.LectureClassChoices.NLP
    ).order_by("-number")
    current_page = "nlp"
    template_name = "book/study/nlp.html"
