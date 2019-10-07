from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from .models import Boards


def get_render_dict(current_page):
    return {'current_page': current_page}


def index(request):
    render_dict = get_render_dict('index')
    return render(request, 'book/index.html', render_dict)


# Create your views here.
class BoardsListClassView(ListView):
    model = Boards
    template_file = "book/boards_list_cbv.html"


def BoardsListFunctionView(request):
    boardList = Boards.objects.all()

    return render(request, 'book/boards_list_fbv.html', {'boardList': boardList})


class BoardsTemplateClassView(TemplateView):
    template_name = "book/template.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = Boards.objects.all()
        return context
