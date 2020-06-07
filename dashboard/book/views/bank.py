"""Banking에 관련된 View."""

import logging
from typing import Any, Dict

from bank import models as bank_models
from book.nav import get_render_dict
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView

from .view_utils import CurrentPageMixin, SuperuserMixin

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


class SavingsView(ListView, LoginRequiredMixin, SuperuserMixin, CurrentPageMixin):
    """예적금 리스트."""

    current_page = "savings"
    template_name = "book/investment/savings.html"
    queryset = bank_models.Saving.objects.order_by("-date").prefetch_related("bank")

    def test_func(self):
        """Check whether user is superuser or not."""
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Chart 내용을 context 에 추가."""
        context = super().get_context_data(**kwargs)

        chart_map = {}

        for obj in self.queryset:
            chart_map[obj.date] = chart_map.get(obj.date, 0) + obj.interest_minus_tax

        chart_label = sorted([label for label in chart_map])
        chart_amount = [chart_map[label] for label in chart_label]

        context["chart_label"] = [label.strftime("%Y-%m-%d") for label in chart_label]
        context["chart_amount"] = chart_amount

        return context


class BankDetailView(DetailView, LoginRequiredMixin, SuperuserMixin, CurrentPageMixin):
    """은행 상세 정보."""

    model = bank_models.Bank
    current_page = "account"
    template_name = "book/investment/bank.html"


class AccountListView(
    TemplateView, LoginRequiredMixin, SuperuserMixin, CurrentPageMixin
):
    """계좌 내역 리스트."""

    current_page = "account"
    template_name = "book/investment/account.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Get latest snapshots."""
        context = super().get_context_data(**kwargs)
        object_list = bank_models.Account.objects.all().prefetch_related(
            "accountsnapshot_set", "bank"
        )
        latest = object_list.order_by("bank", "account_number")

        object_list = []
        for obj in latest:
            snapshot = obj.accountsnapshot_set.all().order_by("-added_time")
            if snapshot:
                object_list.append((obj, snapshot[0]))
            else:
                object_list.append((obj, None))

        summary = {}
        total = {}
        for obj, snapshot in object_list:
            if snapshot:
                value = summary.get(obj.bank, {})
                currency = value.get(snapshot.currency, 0.0)

                value[snapshot.currency] = currency + snapshot.amount
                summary[obj.bank] = value

                aggregation = total.get(snapshot.currency, 0.0)
                total[snapshot.currency] = aggregation + snapshot.amount

        context["object_list"] = object_list
        context["summary"] = summary
        context["total"] = total
        return context


class AccountDetailView(
    DetailView, LoginRequiredMixin, SuperuserMixin, CurrentPageMixin
):
    """계좌 상세 정보."""

    pass
