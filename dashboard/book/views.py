import json

import requests
from django.core import exceptions
from django.http import HttpResponse
from django.shortcuts import render

from .models import Link, Lotto, Paper, Stock
from .utils import new_lotto
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
            info_json = XmlDictConfig(realtime_result[1].find('TBL_StockInfo'))
            render_dict['market_close'] = realtime_json['myJangGubun'] == "장마감" or realtime_json[
                'myJangGubun'] == '장개시전'
            render_dict['realtime_result'] = (realtime_json, realtime_result[0], info_json)

            if 'JongName' in info_json and info_json['JongName']:
                try:
                    Stock.objects.get(code=query)
                except exceptions.ObjectDoesNotExist:
                    stock = Stock(code=query, name=info_json['JongName'])
                    stock.save()

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

    stocks = Stock.objects.all().order_by('code')
    render_dict['stocks'] = stocks
    return render(request, 'book/investment/krx_price_query.html', render_dict)


def export_lotto(request):
    max_object = Lotto.objects.order_by('-draw_number')[0]

    max_draw = max_object.draw_number

    for draw_number in range(1, max_draw + 10):
        result, _ = new_lotto(draw_number)

        if result['returnValue'] == 'fail':
            break

    all_objects = Lotto.objects.order_by('draw_number')
    result_list = []
    for obj in all_objects:
        result_list.append(','.join(map(str, [obj.draw_number,
                                              obj.numbers['totSellamnt'],
                                              obj.numbers['firstWinamnt'],
                                              obj.numbers['firstPrzwnerCo'],
                                              obj.numbers['drwtNo1'],
                                              obj.numbers['drwtNo2'],
                                              obj.numbers['drwtNo3'],
                                              obj.numbers['drwtNo4'],
                                              obj.numbers['drwtNo5'],
                                              obj.numbers['drwtNo6']])))

    return HttpResponse('\n'.join(result_list))


def lotto(request):
    render_dict = get_render_dict('invest', 'lotto')

    result = ""
    if request.POST:
        draw_number = request.POST['draw_number']
        render_dict["draw_number"] = draw_number

        result, _ = new_lotto(draw_number)
    all_objects = Lotto.objects.order_by('-draw_number')[:30]
    render_dict["result"] = result
    render_dict["all_objects"] = all_objects

    return render(request, 'book/investment/lotto.html', render_dict)


def wine(request):
    render_dict = get_render_dict('others', 'wine')
    return render(request, 'book/wine.html', render_dict)


# law_search
law_query_url = "http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=law&type=XML&mobileYn=Y&query={}"


def law_search(request):
    render_dict = get_render_dict('others', 'law_search')

    if request.POST:
        query = request.POST['query']
        render_dict['query'] = query

        result, tree = get_xml_request(law_query_url.format(query))

        law_list = [XmlDictConfig(node) for node in tree.findall('law')]
        render_dict['result'] = result
        render_dict['law_list'] = law_list

    return render(request, 'book/law_search.html', render_dict)


def todo(request):
    render_dict = get_render_dict('others', 'todo')
    return render(request, 'book/todo.html', render_dict)


# study
def slide(request):
    render_dict = get_render_dict('study', 'slide')
    return render(request, 'book/study/slide.html', render_dict)


def paper(request):
    render_dict = get_render_dict('study', 'paper')
    paper_list = Paper.objects.all()

    render_dict['paper_list'] = paper_list
    return render(request, 'book/study/paper.html', render_dict)


def colab(request):
    render_dict = get_render_dict('study', 'colab')
    return render(request, 'book/study/colab.html', render_dict)


def idea(request):
    render_dict = get_render_dict('idea')
    return render(request, 'book/idea.html', render_dict)


def chatbot(request):
    render_dict = get_render_dict('chatbot')
    return render(request, 'book/chatbot/chatbot.html', render_dict)


def query_chatbot(request):
    if request.POST:
        message = request.POST['message']
        data = {
            "sender": "Rasa",
            "message": message,
        }

        result = {}
        try:
            text = json.loads(requests.post('http://rasa:5005/webhooks/rest/webhook', json=data).text)
            result['text'] = text
            result['status'] = 'success'
        except Exception as e:
            text = "Server is not responding"
            result['text'] = str(e)
            result['status'] = 'failed'
        # print(text)
        return HttpResponse(json.dumps(text))
    else:
        return HttpResponse("Empty Message")
