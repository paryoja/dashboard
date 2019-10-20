from xml.etree import cElementTree as ElementTree

import requests
from django.shortcuts import render

from .xml_helper import XmlDictConfig


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
