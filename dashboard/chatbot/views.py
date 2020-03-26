# Create your views here.
from django.views.generic import FormView

from .forms import ChatForm


class AboutView(FormView):
    template_name = "about.html"
    form_class = ChatForm
