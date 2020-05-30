from typing import Any, Dict

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
