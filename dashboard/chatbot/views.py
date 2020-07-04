"""Create your views here."""
from typing import Any, Dict

from chatbot import epl, forms
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import FormView, TemplateView


class AboutView(FormView):
    """About View."""

    template_name = "about.html"
    form_class = forms.ChatForm


class ChattingView(FormView):
    """Chatting Room."""

    template_name = "chatbot/chatting.html"
    form_class = forms.ChattingForm


class EPLView(TemplateView):
    """EPL Formation."""

    template_name = "epl/formation2.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """라인업 정보와 HTML 을 받아온다."""
        context = super().get_context_data(**kwargs)
        lineup, lineup_html = epl.get_lineup(0)
        context["lineup_html"] = lineup_html
        context["lineup"] = lineup
        return context

    @xframe_options_exempt
    def get(self, request, *args, **kwargs):
        """X-Frame 예외 설정."""
        return super().get(request, *args, **kwargs)
