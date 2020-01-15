from django.contrib.auth import views as auth_views

from . import views


class BookLoginView(auth_views.LoginView):
    def __init__(self):
        super(BookLoginView, self).__init__()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            **views.get_render_dict("")
        })
        return context


class BookLogoutView(auth_views.LogoutView):
    template_name = 'book/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'logged_out': True,
            **views.get_render_dict("")
        })
        return context
