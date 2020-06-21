"""은행 관련 입력을 받기 위한 폼."""
from bank.models import Account
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms


class AddSnapshotForm(forms.Form):
    """현재 계좌 상황을 입력 받기 위한 폼."""

    helper = FormHelper()
    helper.add_input(Submit("submit", "Submit"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for account in Account.objects.all().order_by("bank", "account_name"):
            self.fields["account_{}".format(account.id)] = forms.IntegerField(
                label="{} {} {}".format(
                    account.bank, account.account_name, account.account_number
                )
            )
