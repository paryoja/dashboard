"""Bank 모듈의 Admin View."""

# Register your models here.
from book import utils
from django.contrib import admin
from django.contrib.humanize.templatetags.humanize import intcomma
from django.template.defaultfilters import floatformat

from . import models


@admin.register(models.Bank)
class BankAdmin(utils.ExportCsvMixin):
    """은행 정보."""

    change_list_template = "admin/bank_changelist.html"
    list_display = ("name",)
    actions = ["export_as_csv"]


@admin.register(models.Saving)
class SavingAdmin(utils.ExportCsvMixin):
    """적금 정보."""

    change_list_template = "admin/bank_changelist.html"
    list_display = (
        "date",
        "bank",
        "account_number",
        "principal",
        "interest",
        "interest_rate",
        "tax",
        "payment",
        "interest_minus_tax",
        "interest_rate_per_year",
    )
    actions = ["export_as_csv"]
    field_names = [
        "id",
        "date",
        "bank_id",
        "account_number",
        "principal",
        "interest",
        "is_tax_exemption",
        "is_deposit",
        "range",
    ]

    def interest_rate(self, obj):
        """이자율 포맷."""
        return "%.2f%%" % (obj.interest_rate * 100)

    def interest_rate_minus_tax(self, obj):
        """실이자율 포맷."""
        return "%.2f%%" % (obj.interest_rate_minus_tax * 100)

    def interest_rate_per_year(self, obj):
        """연환산 이자율 포맷."""
        return "%.2f%%" % (obj.interest_rate_per_year * 100)


@admin.register(models.Currency)
class CurrencyAdmin(utils.ExportCsvMixin):
    """환전 정보."""

    change_list_template = "admin/bank_changelist.html"
    fieldsets = [
        ("Date information", {"fields": ["date"]}),
        ("From", {"fields": ["from_currency", "from_amount"]}),
        ("To", {"fields": ["to_currency", "to_amount"]}),
        ("Rate", {"fields": ["currency_rate"]}),
    ]
    list_display = ("date", "from_amount", "to_amount", "currency_rate", "rate")
    actions = ["export_as_csv"]

    def from_amount(self, obj):
        """Format from_amount."""
        return intcomma(floatformat(obj.from_amount))

    def rate(self, obj):
        """환율을 변환된 값으로 부터 계산한 값."""
        return "%.2f" % (float(obj.from_amount) / float(obj.to_amount))


@admin.register(models.Account)
class AccountAdmin(utils.ExportCsvMixin):
    """계좌 정보."""

    search_fields = ("account_number", "account_name", "closed")
    list_display = (
        "bank",
        "account_number",
        "account_name",
        "account_type",
        "last_updated",
    )


@admin.register(models.AccountSnapshot)
class AccountSnapshotAdmin(utils.ExportCsvMixin):
    """계좌 내역 정보."""
