from django.shortcuts import render


def get_render_dict(current_page):
    return {current_page: 'active'}


def index(request):
    render_dict = get_render_dict('index')
    return render(request, 'book/index.html', render_dict)


def link(request):
    render_dict = get_render_dict('link')
    return render(request, 'book/link.html', render_dict)


def algorithm(request):
    render_dict = get_render_dict('algorithm')
    return render(request, 'book/algorithm.html', render_dict)


def invest(request):
    render_dict = get_render_dict('invest')
    return render(request, 'book/invest.html', render_dict)