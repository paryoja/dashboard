"""Class View 를 이용한 view 구현."""
from typing import Any, Dict

from book import forms, models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from people import models as people_models

from .view_utils import CurrentPageMixin, SuperuserMixin


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


class MomentumView(ListView, CurrentPageMixin, LoginRequiredMixin, SuperuserMixin):
    """모멘텀 투자 정보 리스트."""

    current_page = "momentum"
    template_name = "book/investment/momentum.html"
    queryset = models.MomentumSummary.objects.order_by("-date")

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


class ReactTemplateView(TemplateView, CurrentPageMixin):
    """React."""

    current_page = "react"
    template_name = "book/study/react.html"


class VueTemplateView(TemplateView, CurrentPageMixin):
    """Vue."""

    current_page = "vue"
    template_name = "book/study/vue.html"


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


class FriendListView(LoginRequiredMixin, ListView, CurrentPageMixin):
    """친구 리스트."""

    queryset = people_models.Person.objects.all()
    current_page = "friend_list"
    template_name = "people/person.html"
