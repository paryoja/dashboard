from xml.etree import cElementTree as ElementTree

import requests
from django.shortcuts import render

from .models import Link
from .xml_helper import XmlDictConfig


def get_render_dict(current_page, side_page=None):
    render_dict = {current_page: 'active'}
    if side_page:
        render_dict[side_page] = 'active'
    return render_dict


def index(request):
    render_dict = get_render_dict('index')
    return render(request, 'book/index.html', render_dict)


def link(request):
    render_dict = get_render_dict('link')
    render_dict['table_content'] = Link.objects.all()
    return render(request, 'book/link.html', render_dict)


def algorithm(request):
    render_dict = get_render_dict('algorithm')
    return render(request, 'book/algorithm.html', render_dict)


def live_currency(request):
    render_dict = get_render_dict('invest', 'live_currency')
    return render(request, 'book/investment/live_currency.html', render_dict)


def leading_stocks(request):
    render_dict = get_render_dict('invest', 'leading_stocks')
    return render(request, 'book/investment/leading_stocks.html', render_dict)


def wine(request):
    render_dict = get_render_dict('wine')
    return render(request, 'book/wine.html', render_dict)


query_url = "http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=law&type=XML&mobileYn=Y&query="


def law_search(request):
    render_dict = get_render_dict('law_search')

    if request.POST:
        query = request.POST['query']
        render_dict['query'] = query

        # query = parse.quote(query)
        url = query_url + query

        result = requests.post(url).text
        render_dict['result'] = result

        tree = ElementTree.ElementTree(ElementTree.fromstring(result))
        law_list = [XmlDictConfig(node) for node in tree.findall('law')]
        render_dict['law_list'] = law_list

    return render(request, 'book/law_search.html', render_dict)


def deep_learning(request):
    render_dict = get_render_dict('deep_learning')
    return render(request, 'book/deep_learning.html', render_dict)


def todo(request):
    render_dict = get_render_dict('todo')
    return render(request, 'book/todo.html', render_dict)
