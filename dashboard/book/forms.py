"""Forms for book package."""

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    """사용자 정보 폼."""

    class Meta:
        """유저 명과 패스워드 fields 만 제공."""

        model = User
        fields = ["username", "password"]
