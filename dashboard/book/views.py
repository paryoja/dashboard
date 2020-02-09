import datetime
import json
import math
import re
import traceback

import requests
from bs4 import BeautifulSoup
from celery import shared_task
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core import exceptions
from django.http import HttpResponse
from django.shortcuts import render

from . import models
from . import utils
from .nav import get_render_dict
from .xml_helper import XmlDictConfig, get_xml_request


def index(request):
    render_dict = get_render_dict('index')
    return render(request, 'book/index.html', render_dict)


def link(request):
    render_dict = get_render_dict('link')
    render_dict['table_content'] = models.Link.objects.all()
    return render(request, 'book/link.html', render_dict)


def algorithm(request):
    render_dict = get_render_dict('algorithm')
    return render(request, 'book/algorithm.html', render_dict)


# investment
@user_passes_test(lambda u: u.is_superuser)
def live_currency(request):
    render_dict = get_render_dict('live_currency')
    currency_list = models.Currency.objects.all().order_by('-date')

    total_from = 0
    total_to = 0

    for currency in currency_list:
        total_from += currency.from_amount
        total_to += currency.to_amount
    total = {'from': total_from, 'to': total_to, 'rate': total_from / total_to}

    render_dict['currency_list'] = currency_list
    render_dict['total'] = total

    return render(request, 'book/investment/live_currency.html', render_dict)


def leading_stocks(request):
    render_dict = get_render_dict('leading_stocks')
    return render(request, 'book/investment/leading_stocks.html', render_dict)


krx_price_query_url = "http://asp1.krx.co.kr/servlet/krx.asp.XMLSise?code={}"
krx_statement_query_url = "http://asp1.krx.co.kr/servlet/krx.asp.XMLJemu?code={}"
balance_order = ['hangMok', 'year1Money', 'year1GuSungRate', 'year1JungGamRate', 'year2Money', 'year2GuSungRate',
                 'year2JungGamRate', 'year3Money', 'year3GuSungRate', 'year3JungGamRate']
cash_order = ['hangMok', 'year1Money', 'year1JungGamRate', 'year2Money', 'year2JungGamRate', 'year3Money',
              'year3JungGamRate']
a_pattern = re.compile('<a href="(.+?)">(.+?)</a>')


def krx_price_query(request):
    render_dict = get_render_dict('krx_price_query')
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
                    models.Stock.objects.get(code=query)
                except exceptions.ObjectDoesNotExist:
                    stock = models.Stock(code=query, name=info_json['JongName'])
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

    stocks = models.Stock.objects.all().order_by('code')
    render_dict['stocks'] = stocks
    return render(request, 'book/investment/krx_price_query.html', render_dict)


def export_lotto(request):
    max_object = models.Lotto.objects.order_by('-draw_number')[0]

    max_draw = max_object.draw_number

    for draw_number in range(1, max_draw + 10):
        result, _ = utils.new_lotto(draw_number)

        if result['returnValue'] == 'fail':
            break

    all_objects = models.Lotto.objects.order_by('draw_number')
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
    render_dict = get_render_dict('lotto')

    result = ""
    if request.POST:
        draw_number = request.POST['draw_number']
        render_dict["draw_number"] = draw_number

        result, _ = utils.new_lotto(draw_number)
    all_objects = models.Lotto.objects.order_by('-draw_number')[:30]
    render_dict["result"] = result
    render_dict["all_objects"] = all_objects

    return render(request, 'book/investment/lotto.html', render_dict)


def wine(request):
    render_dict = get_render_dict('wine')

    wine_list = models.Wine.objects.all()
    render_dict['wine_list'] = wine_list
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


def todo(request):
    render_dict = get_render_dict('todo')
    return render(request, 'book/todo.html', render_dict)


# study
def slide(request):
    render_dict = get_render_dict('slide')
    return render(request, 'book/study/slide.html', render_dict)


def paper(request):
    render_dict = get_render_dict('paper')
    paper_list = models.Paper.objects.all()

    render_dict['paper_list'] = paper_list
    return render(request, 'book/study/paper.html', render_dict)


def colab(request):
    render_dict = get_render_dict('colab')
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


@user_passes_test(lambda u: u.is_superuser)
def people(request):
    render_dict = get_render_dict('people')

    query = request.GET.get('query', '')

    unclassified = models.PeopleImage.objects.filter(selected=None)
    unclassified_count = unclassified.count()
    query_count = unclassified.filter(title__contains=query).count()
    image_list = unclassified.filter(title__contains=query).order_by('?')[:100]

    render_dict['unclassified_count'] = unclassified_count
    render_dict['query_count'] = query_count

    if query:
        id_select = unclassified.filter(url__contains=query)
        render_dict['query_count'] += id_select.count()
        render_dict['image_list'] = id_select[:50].values() | image_list.values()
    else:
        render_dict['image_list'] = image_list.values()
    render_dict['query'] = query

    return render(request, 'book/people.html', render_dict)


@user_passes_test(lambda u: u.is_superuser)
def people_result(request, page=1):
    render_dict = get_render_dict('people_result')

    query = request.GET.get('query', '')
    selected_list = models.PeopleImage.objects.filter(selected=True)
    if query:
        queried_list = selected_list.filter(url__contains=query)
        selected_list = queried_list | selected_list.filter(title__contains=query)
    else:
        selected_list = models.PeopleImage.objects.filter(selected=True).order_by('url')

    p, page_info = utils.get_page_info(selected_list, page, 120)

    row_count = 3
    people_table = []
    count = 0
    people_row = []
    for img in p:
        if count % row_count == 0:
            people_row = []
            people_table.append(people_row)
        people_row.append(img)
        count += 1

    render_dict['people_table'] = people_table
    render_dict['page_info'] = page_info
    render_dict['query'] = query

    return render(request, 'book/people_result.html', render_dict)


@user_passes_test(lambda u: u.is_superuser)
def people_high_expectation(request):
    render_dict = get_render_dict('people_high_expectation')

    query = request.GET.get('query', '')
    order = request.GET.get('order', 'decreasing')

    selected_list = models.Rating.objects.filter(image__selected=None, deep_model__latest=True)
    render_dict['unclassified_count'] = selected_list.count()

    if query:
        queried_list = selected_list.filter(image__url__contains=query)[:100]
        selected_list = queried_list | selected_list.filter(image__title__contains=query)[:100]

    render_dict['query_count'] = selected_list.count()

    if order == "decreasing":
        selected_list = selected_list.order_by("-positive")[:100]
    elif order == "increasing":
        selected_list = selected_list.order_by("positive")[:100]
    else:
        selected_list = selected_list.order_by("?")[:100]

    unclassified = [rating.image for rating in selected_list]

    render_dict['rating'] = selected_list

    render_dict['image_list'] = unclassified
    render_dict['query'] = query

    return render(request, 'book/people.html', render_dict)


@user_passes_test(lambda u: u.is_superuser)
def people_result_download(request, selected, page):
    image_list = models.PeopleImage.objects.filter(selected=selected).only("url", "selected", "page")

    count = 1000
    return utils.get_compressed_result(image_list, count, page)


def real_estate(request):
    render_dict = get_render_dict('real_estate')

    price_link = models.Link.objects.filter(content_type="부동산 시세")
    useful_link = models.Link.objects.filter(content_type="부동산")

    check_list = ["햇빛은 잘 들어오는가?",
                  "물이 샌(누수) 흔적은 없는가?",
                  "천장이나 벽, 장판 아래 곰팡이가 핀 곳은 없는가?",
                  "전기콘센트는 파손된 곳이 없는가?",
                  "수도는 잘 나오는가?",
                  "배수는 잘되는가?",
                  "싱크대, 후드, 수납장 등 파손된 주방시설은 없는가?",
                  "냉장고를 놓을 수 있는 공간이 있는가?",
                  "욕실의 변기나 샤워기, 거울 등 파손된 시설은 없는가?",
                  "세탁기를 놓을 수 있는 공간이 있는가?",
                  "발코니가 있는가?",
                  "빨래를 건조할 수 있는 공간이 있는가?",
                  "방의 높이가 장롱이 들어갈 수 있을 만큼 높은가",
                  "다용도실 같은 별도의 서비스 공간이 있는가?",
                  "방충망이나 방범창이 있는가?",
                  "환기가 잘 되는가?",
                  "외풍이 심하지 않은가?",
                  "전기와 수도 계량기는 별도로 사용하는가?",
                  "주 출입구에 방범시설이 되어 있는가?",
                  "주차장은 있는가?",
                  "집 주변에 고물상, 공장 등 혐오시설은 없는가?",
                  "집 주변에 시장이나 할인마트가 있는가?",
                  "집 주변에 공원이나 놀이터 등이 있는가?",
                  "집에서 학교, 어린이집, 학원 등이 가까운가?",
                  "집에서 병원은 가까운가?",
                  "지하철역과 버스정류장이 도보로 10분 이내에 있는가?",
                  "집이 너무 외진 곳에 있지 않은가?",
                  "저당금액과 총 보증금의 합이 집값의 80%를 넘는가?",
                  "공부서류들의 내용이 서로 일치하는가?",
                  "집을 내놓았을 때 잘 나갈 수 있겠는가?"
                  ]

    render_dict["price_link"] = price_link
    render_dict["useful_link"] = useful_link
    render_dict["check_list"] = check_list
    return render(request, 'book/real_estate.html', render_dict)


def recommend_book(request):
    render_dict = get_render_dict('recommend_book')

    book_list = models.Book.objects.all()
    render_dict['book_list'] = book_list

    return render(request, 'book/investment/recommend_book.html', render_dict)


def food(request):
    render_dict = get_render_dict('food')

    restaurant_list = [
        {'name': '고기리막국수',
         'famous_for': '막국수',
         'cuisine_type': '한식',
         'address': '고기리',
         'visited': False},
        {'name': '명동교자',
         'famous_for': '칼국수',
         'cuisine_type': '한식',
         'history': '칼국수, 만두',
         'visited': True},
        {'name': '라모라',
         'famous_for': '파스타',
         'cuisine_type': '양식',
         'history': '트러플 파스타',
         'visited': True},
        {'name': '필동면옥',
         'famous_for': '평양냉면',
         'cuisine_type': '한식',
         'history': '평양냉면',
         'visited': True},
        {'name': '임병주산동손칼국수',
         'famous_for': '칼국수',
         'cuisine_type': '한식',
         'history': '칼국수, 콩국수, 만두',
         'visited': True}
    ]

    render_dict['restaurant_list'] = restaurant_list

    return render(request, 'book/food.html', render_dict)


@shared_task
def add_image_client(a_text, url, category_id, data_type):
    a_parsed = a_pattern.findall(a_text)

    if not a_parsed[0][0].startswith("../"):

        if data_type == "people":
            json_url = url + a_parsed[0][0] + '/image.json'
            result = json.loads(requests.get(json_url).text)["image_list"]

        elif data_type == "pokemon":
            directory_url = url + a_parsed[0][0]
            image_result = requests.get(directory_url)
            bs = BeautifulSoup(image_result.text, 'html.parser')

            all_a = bs.findAll('a', text=True)
            result = []
            for a in all_a:
                image_a_parsed = a_pattern.findall("{}".format(a))
                print(image_a_parsed)
                if not image_a_parsed[0][0].startswith("../"):
                    result.append(directory_url + image_a_parsed[0][0])

        else:
            raise ValueError("Unsupported data_type {}".format(data_type))

        for img in result:
            try:
                if data_type == "people":
                    image = models.PeopleImage(url=url + a_parsed[0][0] + img['local'],
                                               title=img['alt'][:500],
                                               category_id=category_id,
                                               page=img['a'])
                elif data_type == "pokemon":
                    path = img.split('/')
                    image = models.PokemonImage(url=img,
                                                title=path[-1],
                                                category_id=category_id,
                                                original_label=path[-2])
                else:
                    raise ValueError("Unsupported data_type {}".format(data_type))
                image.save()
            except Exception as e:
                print(e)


def add_image(request, data_type='pokemon'):
    render_dict = None
    if data_type == 'pokemon':
        render_dict = get_render_dict('pokemon')
    elif data_type == 'people':
        render_dict = get_render_dict('people')

    if request.POST:
        try:
            url = request.POST["url"]
            category_id = request.POST["category"]

            if data_type == 'pokemon':
                result = requests.get(url)
                render_dict['result'] = result.text

                bs = BeautifulSoup(result.text, 'html.parser')
                # directory list
                all_a = bs.findAll('a', text=True)

                for a in all_a:
                    add_image_client.delay("{}".format(a), url, category_id, data_type)
                render_dict['parsed'] = all_a

            elif data_type == 'people':
                result = requests.get(url)
                render_dict['result'] = result.text

                bs = BeautifulSoup(result.text, 'html.parser')
                all_a = bs.findAll('a', text=True)
                render_dict['parsed'] = all_a

                for a in all_a:
                    add_image_client.delay("{}".format(a), url, category_id, data_type)

        except Exception:
            if 'parsed' in render_dict:
                render_dict['parsed'] += traceback.format_exc()
            else:
                render_dict['parsed'] = traceback.format_exc()

    category_list = models.Category.objects.all()
    render_dict['data_type'] = data_type
    render_dict['category_list'] = category_list
    return render(request, 'book/add_image.html', render_dict)


@login_required
def pokemon(request, page=1):
    render_dict = get_render_dict('pokemon_classification')

    query = request.GET.get('query', '')

    if query:
        image_list = models.PokemonImage.objects.filter(original_label__icontains=query).filter(
            classified=None).order_by('?')[:400]
    else:
        image_list = models.PokemonImage.objects.filter(classified=None).order_by('?')
    p, page_info = utils.get_page_info(image_list, page, 20)
    render_dict['image_list'] = p
    render_dict['page_info'] = page_info
    render_dict['query'] = query

    return render(request, 'book/pokemon.html', render_dict)


@login_required
def pokemon_result(request, page=1):
    render_dict = get_render_dict('pokemon_result')

    image_list = models.PokemonImage.objects.filter(classified="yes")

    p, page_info = utils.get_page_info(image_list, page, 100)

    render_dict['image_list'] = p
    render_dict['page_info'] = page_info

    verified_count = image_list.count()
    row_count = 10
    verified_table = []
    count = 0
    verified_row = None

    for img in p:
        if count % row_count == 0:
            verified_row = []
            verified_table.append(verified_row)
        verified_row.append(img)
        count += 1
    render_dict['verified_table'] = verified_table
    render_dict['verified_count'] = verified_count

    return render(request, 'book/pokemon_result.html', render_dict)


@login_required
def pokemon_export(request, classified="yes", page=1):
    count = 1000
    image_list = models.PokemonImage.objects.filter(classified=classified)

    return utils.get_compressed_result(image_list, count, page)


def compute_expectation(x, coeff):
    value = coeff['a'] / (1 + math.exp(-(x - coeff['x0']) / coeff['b']))
    return value


def corona(request):
    render_dict = get_render_dict('corona')

    counts = models.Corona.objects.all().order_by("-date")
    render_dict['counts'] = counts

    confirmed = {
        'a': 49823.777,
        'b': 3.513674,
        'x0': 14.174237
    }
    death = {
        'a': 1374.9548,
        'b': 4.3781347,
        'x0': 16.540905
    }
    offset = counts.count()
    latest_date = counts[0].date
    delta = datetime.timedelta(days=1)

    expected = []

    for off in range(offset + 1, offset + 10):
        latest_date += delta
        expected_confirmed = compute_expectation(off, confirmed)
        expected_death = compute_expectation(off, death)
        expected.append({
            'date': latest_date,
            'confirmed': expected_confirmed,
            'death': expected_death,
        })
    expected = sorted(expected, key=lambda x: x['date'], reverse=True)
    render_dict['expected'] = expected
    return render(request, 'book/corona.html', render_dict)
