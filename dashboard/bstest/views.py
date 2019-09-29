from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    render_dict = {
        'content': 'Hello World',
    }
    return render(request, 'bstest/main.html', render_dict)
