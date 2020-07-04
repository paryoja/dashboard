"""Views for user login and logout."""
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm

from .views import views_function


class CustomAuthenticationForm(AuthenticationForm):
    """Authentication Form."""

    def __init__(self, *args, **kwargs):
        """Submit 버튼 추가."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"

        self.helper.add_input(Submit("submit", "Submit"))


class BookLoginView(auth_views.LoginView):
    """Login view."""

    form_class = CustomAuthenticationForm

    def __init__(self):
        super(BookLoginView, self).__init__()

    def get_context_data(self, **kwargs):
        """Set current page."""
        context = super().get_context_data(**kwargs)
        context.update({**views_function.get_render_dict("login")})
        return context


class BookLogoutView(auth_views.LogoutView):
    """Logout view."""

    template_name = "book/index.html"

    def get_context_data(self, **kwargs):
        """Set current page."""
        context = super().get_context_data(**kwargs)

        context.update({"logged_out": True, **views_function.get_render_dict("logout")})
        return context
