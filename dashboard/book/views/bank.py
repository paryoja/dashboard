"""Banking에 관련된 View."""

import logging
from typing import Any, Dict

from bank import models as bank_models
from book.nav import get_render_dict
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import ListView

from .view_utils import CurrentPageMixin

logger = logging.getLogger(__name__)


# investment
@user_passes_test(lambda u: u.is_superuser)
def currency_change(request):
    """
    환전 내용.

    :param request:
    :return:
    """
    render_dict = get_render_dict("currency_change")
    currency_list = bank_models.Currency.objects.all().order_by("-date")

    total_from = 0.0
    total_to = 0.0

    chart_data = {}
    chart_amount = {}

    for currency in currency_list:
        total_from += currency.from_amount
        total_to += currency.to_amount

        chart_data[currency.date] = currency.currency_rate
        chart_amount[currency.date] = (
            chart_amount.get(currency.date, 0) + currency.to_amount
        )
    if total_to != 0.0:
        total = {"from": total_from, "to": total_to, "rate": total_from / total_to}
    else:
        total = {"from": total_from, "to": total_to, "rate": 0.0}

    render_dict["currency_list"] = currency_list
    render_dict["total"] = total

    chart_label = sorted([label for label in chart_data])
    render_dict["chart_label"] = [label.strftime("%Y-%m-%d") for label in chart_label]
    render_dict["chart_data"] = [chart_data[label] for label in chart_label]
    render_dict["chart_amount"] = [chart_amount[label] for label in chart_label]

    return render(request, "book/investment/currency_change.html", render_dict)


class SavingsView(ListView, CurrentPageMixin, LoginRequiredMixin, UserPassesTestMixin):
    """예적금 리스트."""

    current_page = "savings"
    template_name = "book/investment/savings.html"
    queryset = bank_models.Saving.objects.order_by("-date").prefetch_related("bank")

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


class AccountView(ListView, CurrentPageMixin, LoginRequiredMixin, UserPassesTestMixin):
    """계좌 내역 리스트."""

    current_page = "account"
    template_name = "book/investment/account.html"
    model = bank_models.Account
