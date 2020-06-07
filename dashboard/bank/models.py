"""금융에 관련된 모든 모델."""
import math

from django.db import models
from django.utils.translation import gettext_lazy as _


class CurrencyChoices(models.TextChoices):
    """환전 또는 주식 거래에서 사용할 통화 목록."""

    USD = "USD", _("USD")
    KRW = "KRW", _("KRW")


class AccountTypeChoices(models.TextChoices):
    """계좌 종류."""

    Saving = "Saving", _("입출금")
    Periodic = "Periodic", _("적금")
    Deposit = "Deposit", _("예금")


# Create your models here.
class Bank(models.Model):
    """은행."""

    name = models.CharField(max_length=40)

    def __str__(self):
        return str(self.name)


class Saving(models.Model):
    """적금 계좌."""

    date = models.DateField()
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=100)
    principal = models.IntegerField()
    interest = models.IntegerField()
    is_tax_exemption = models.BooleanField()
    is_deposit = models.BooleanField(default=False)
    range = models.IntegerField(default=12)

    @property
    def interest_rate(self):
        """이자율."""
        return float(self.interest) / float(self.principal)

    @property
    def tax_rate(self):
        """세율."""
        if self.is_tax_exemption:
            return 0.014
        else:
            return 0.154

    @property
    def tax(self):
        """세금."""
        return math.floor(float(self.interest) * self.tax_rate)

    @property
    def interest_minus_tax(self):
        """세금 제외 이자."""
        return self.interest - self.tax

    @property
    def payment(self):
        """실지금액."""
        return self.principal + self.interest_minus_tax

    @property
    def interest_rate_minus_tax(self):
        """실지급 기준 이자율."""
        return self.interest_minus_tax / float(self.principal)

    @property
    def interest_rate_per_year(self):
        """연환산 이자율."""
        return math.pow(1.0 + self.interest_rate_minus_tax, 1.0 / self.range * 12) - 1.0


class Currency(models.Model):
    """환전 내역."""

    class Meta:
        """Meta data for currency."""

        verbose_name_plural = "Currencies"

    date = models.DateField()
    from_currency = models.CharField(
        max_length=10, choices=CurrencyChoices.choices, default=CurrencyChoices.KRW
    )
    to_currency = models.CharField(
        max_length=10, choices=CurrencyChoices.choices, default=CurrencyChoices.USD
    )

    currency_rate = models.FloatField()
    from_amount = models.FloatField()
    to_amount = models.FloatField()

    def get_currency_rate(self):
        """환율 계산."""
        return self.from_amount / self.to_amount


class Account(models.Model):
    """계좌 정보."""

    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=100, null=True, blank=True)
    account_name = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now_add=True)
    account_type = models.TextField(
        max_length=30,
        choices=AccountTypeChoices.choices,
        default=AccountTypeChoices.Saving,
    )

    def __str__(self):
        return "{} {}".format(self.bank, self.account_number)


class AccountSnapshot(models.Model):
    """특정 시점의 계좌내 금액."""

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    added_time = models.DateTimeField(auto_now_add=True)
    currency = models.CharField(
        max_length=10, choices=CurrencyChoices.choices, default=CurrencyChoices.KRW
    )
    amount = models.FloatField()


class Transaction(models.Model):
    """이체 내역."""

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    note = models.CharField(max_length=50)
    amount = models.FloatField()
    is_income = models.BooleanField()
    datetime = models.DateTimeField()
