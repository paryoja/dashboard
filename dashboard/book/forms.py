"""Forms for book package."""

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    """사용자 정보 폼."""

    class Meta:
        """유저 명과 패스워드 fields 만 제공."""

        model = User
        fields = ["username", "password"]


class QueryForm(forms.Form):
    """Sentence Query Form."""

    query = forms.CharField(label="Query")
    helper = FormHelper()
    helper.add_input(Submit("submit", "Submit"))

    helper.form_method = "POST"
