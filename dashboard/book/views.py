from django.views.generic import ListView, TemplateView

from .models import Boards


# Create your views here.
class BoardsListClassView(ListView):
    model = Boards


class BoardsTemplateClassView(TemplateView):
    template_name = "template.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = Boards.objects.all()
        return context
