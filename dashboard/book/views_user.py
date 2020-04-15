"""Views for user login and logout."""
from django.contrib.auth import views as auth_views

from .views import views_function


class BookLoginView(auth_views.LoginView):
    """Login view."""

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
