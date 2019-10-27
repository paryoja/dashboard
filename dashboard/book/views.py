import json

import requests
from django.core import exceptions
from django.shortcuts import render

from .models import Link, Lotto
from .xml_helper import XmlDictConfig, get_xml_request


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


# investment
def live_currency(request):
    render_dict = get_render_dict('invest', 'live_currency')
    return render(request, 'book/investment/live_currency.html', render_dict)


def leading_stocks(request):
    render_dict = get_render_dict('invest', 'leading_stocks')
    return render(request, 'book/investment/leading_stocks.html', render_dict)


krx_price_query_url = "http://asp1.krx.co.kr/servlet/krx.asp.XMLSise?code={}"
krx_statement_query_url = "http://asp1.krx.co.kr/servlet/krx.asp.XMLJemu?code={}"
balance_order = ['hangMok', 'year1Money', 'year1GuSungRate', 'year1JungGamRate', 'year2Money', 'year2GuSungRate',
                 'year2JungGamRate', 'year3Money', 'year3GuSungRate', 'year3JungGamRate']
cash_order = ['hangMok', 'year1Money', 'year1JungGamRate', 'year2Money', 'year2JungGamRate', 'year3Money',
              'year3JungGamRate']


def krx_price_query(request):
    render_dict = get_render_dict('invest', 'krx_price_query')
    if request.POST:
        query = request.POST['query']
        render_dict['query'] = query

        realtime_result = get_xml_request(krx_price_query_url.format(query))
        if realtime_result:
            realtime_json = XmlDictConfig(realtime_result[1].find("stockInfo"))
            render_dict['market_close'] = realtime_json['myJangGubun'] == "장마감" or realtime_json[
                'myJangGubun'] == '장개시전'
            render_dict['realtime_result'] = (realtime_json, realtime_result[0])

        statement_result = get_xml_request(krx_statement_query_url.format(query))
        if statement_result:
            balance_sheet = XmlDictConfig(statement_result[1].find("TBL_DaeCha"))
            if "TBL_DaeCha_data" in balance_sheet:
                hangmok_list = []
                for item in balance_sheet["TBL_DaeCha_data"]:
                    # 항목 이름 뒤에 숫자를 붙여 둬서 쓰기 어려우므로 제거
                    item = {k[:-1]: v for k, v in item.items()}
                    hangmok_list.append([item[order] for order in balance_order])
                balance_sheet["TBL_DaeCha_data"] = hangmok_list
                render_dict['balance_sheet'] = balance_sheet

            income_statement = XmlDictConfig(statement_result[1].find("TBL_SonIk"))
            if "TBL_SonIk_data" in income_statement:
                hangmok_list = []
                for item in income_statement["TBL_SonIk_data"]:
                    # 항목 이름 뒤에 숫자를 붙여 둬서 쓰기 어려우므로 제거
                    item = {k[:-1]: v for k, v in item.items()}
                    hangmok_list.append([item[order] for order in balance_order])
                income_statement["TBL_SonIk_data"] = hangmok_list
                render_dict['income_statement'] = income_statement

            cash_flow = XmlDictConfig(statement_result[1].find("TBL_CashFlow"))
            if "TBL_CashFlow_data" in cash_flow:
                hangmok_list = []
                for item in cash_flow["TBL_CashFlow_data"]:
                    # 항목 이름 뒤에 숫자를 붙여 둬서 쓰기 어려우므로 제거
                    item = {k[:-1]: v for k, v in item.items()}
                    hangmok_list.append([item[order] for order in cash_order])
                cash_flow["TBL_CashFlow_data"] = hangmok_list
                render_dict['cash_flow'] = cash_flow
            render_dict['statement_result'] = statement_result
    return render(request, 'book/investment/krx_price_query.html', render_dict)


def lotto(request):
    render_dict = get_render_dict('invest', 'lotto')

    result = ""
    if request.POST:
        draw_number = request.POST['draw_number']
        render_dict["draw_number"] = draw_number

        try:
            obj = Lotto.objects.get(draw_number=draw_number)
            result = obj.numbers
        except exceptions.ObjectDoesNotExist:
            try:
                params = {
                    'method': 'getLottoNumber',
                    'drwNo': draw_number,
                }
                result = requests.get(
                    "https://www.nlotto.co.kr/common.do", params=params)
                result = json.loads(result.text)
                if not result['returnValue'] == 'fail':
                    obj = Lotto(draw_number=draw_number, numbers=result)
                    obj.save()
            except Exception as e:
                result = str(e)

    render_dict["result"] = result

    return render(request, 'book/investment/lotto.html', render_dict)


def wine(request):
    render_dict = get_render_dict('wine')
    return render(request, 'book/wine.html', render_dict)


# law_search
law_query_url = "http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=law&type=XML&mobileYn=Y&query={}"


def law_search(request):
    render_dict = get_render_dict('law_search')

    if request.POST:
        query = request.POST['query']
        render_dict['query'] = query

        result, tree = get_xml_request(law_query_url.format(query))

        law_list = [XmlDictConfig(node) for node in tree.findall('law')]
        render_dict['result'] = result
        render_dict['law_list'] = law_list

    return render(request, 'book/law_search.html', render_dict)


# study
def slide(request):
    render_dict = get_render_dict('study', 'slide')
    return render(request, 'book/study/slide.html', render_dict)


def paper(request):
    render_dict = get_render_dict('study', 'paper')
    return render(request, 'book/study/paper.html', render_dict)


def colab(request):
    render_dict = get_render_dict('study', 'colab')
    return render(request, 'book/study/colab.html', render_dict)


def todo(request):
    render_dict = get_render_dict('todo')
    return render(request, 'book/todo.html', render_dict)


def idea(request):
    render_dict = get_render_dict('idea')
    return render(request, 'book/idea.html', render_dict)