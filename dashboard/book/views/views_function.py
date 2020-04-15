"""기본 뷰."""
import datetime
import json
import logging
import math
import traceback
import typing

import requests
from book import models, utils
from book.nav import get_render_dict
from book.views import views_api
from book.xml_helper import XmlDictConfig, get_xml_request
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)


# investment
@user_passes_test(lambda u: u.is_superuser)
def currency_change(request):
    """
    환전 내용.

    :param request:
    :return:
    """
    render_dict = get_render_dict("currency_change")
    currency_list = models.Currency.objects.all().order_by("-date")

    total_from = 0.0
    total_to = 0.0

    for currency in currency_list:
        total_from += currency.from_amount
        total_to += currency.to_amount
    if total_to != 0.0:
        total = {"from": total_from, "to": total_to, "rate": total_from / total_to}
    else:
        total = {"from": total_from, "to": total_to, "rate": 0.0}

    render_dict["currency_list"] = currency_list
    render_dict["total"] = total

    return render(request, "book/investment/currency_change.html", render_dict)


def export_lotto(request):
    """
    로또 정보 Export.

    :param request:
    :return:
    """
    max_object = models.Lotto.objects.order_by("-draw_number")[0]

    max_draw = max_object.draw_number

    for draw_number in range(1, max_draw + 10):
        result, _ = utils.new_lotto(draw_number)

        if result["returnValue"] == "fail":
            break

    all_objects = models.Lotto.objects.order_by("draw_number")
    result_list = []
    for obj in all_objects:
        result_list.append(
            ",".join(
                map(
                    str,
                    [
                        obj.draw_number,
                        obj.numbers["totSellamnt"],
                        obj.numbers["firstWinamnt"],
                        obj.numbers["firstPrzwnerCo"],
                        obj.numbers["drwtNo1"],
                        obj.numbers["drwtNo2"],
                        obj.numbers["drwtNo3"],
                        obj.numbers["drwtNo4"],
                        obj.numbers["drwtNo5"],
                        obj.numbers["drwtNo6"],
                    ],
                )
            )
        )

    return HttpResponse("\n".join(result_list))


def lotto(request):
    """
    Lotto 정보 제공.

    :param request:
    :return:
    """
    render_dict = get_render_dict("lotto")

    result = ""
    if request.POST:
        draw_number = request.POST["draw_number"]
        render_dict["draw_number"] = draw_number

        result, _ = utils.new_lotto(draw_number)
    all_objects = models.Lotto.objects.order_by("-draw_number")[:30]
    render_dict["result"] = result
    render_dict["all_objects"] = all_objects

    return render(request, "book/investment/lotto.html", render_dict)


# law_search
law_query_url = "http://www.law.go.kr/DRF/lawSearch.do?OC=test&target=law&type=XML&mobileYn=Y&query={}"


def law_search(request):
    """법률 검색."""
    render_dict = get_render_dict("law_search")

    if request.POST:
        query = request.POST["query"]
        render_dict["query"] = query

        result, tree = get_xml_request(law_query_url.format(query))

        law_list = [XmlDictConfig(node) for node in tree.findall("law")]
        render_dict["result"] = result
        render_dict["law_list"] = law_list

    return render(request, "book/law_search.html", render_dict)


def query_chatbot(request):
    """챗봇."""
    if request.POST:
        message = request.POST["message"]
        data = {
            "sender": "Rasa",
            "message": message,
        }

        result = {}
        try:
            text = json.loads(
                requests.post("http://rasa:5005/webhooks/rest/webhook", json=data).text
            )
            result["text"] = text
            result["status"] = "success"
        except Exception as e:
            text = "Server is not responding"
            result["text"] = str(e)
            result["status"] = "failed"
        return HttpResponse(json.dumps(text))
    else:
        return HttpResponse("Empty Message")


def real_estate(request):
    """부동산 유용 정보."""
    render_dict = get_render_dict("real_estate")

    price_link = models.Link.objects.filter(content_type="부동산 시세")
    useful_link = models.Link.objects.filter(content_type="부동산")

    check_list = [
        "햇빛은 잘 들어오는가?",
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
        "집을 내놓았을 때 잘 나갈 수 있겠는가?",
    ]

    render_dict["price_link"] = price_link
    render_dict["useful_link"] = useful_link
    render_dict["check_list"] = check_list
    return render(request, "book/real_estate.html", render_dict)


def food(request):
    """맛집 정보."""
    render_dict = get_render_dict("food")

    restaurant_list = [
        {
            "name": "고기리막국수",
            "famous_for": "막국수",
            "cuisine_type": "한식",
            "address": "고기리",
            "visited": False,
        },
        {
            "name": "명동교자",
            "famous_for": "칼국수",
            "cuisine_type": "한식",
            "history": "칼국수, 만두",
            "visited": True,
        },
        {
            "name": "라모라",
            "famous_for": "파스타",
            "cuisine_type": "양식",
            "history": "트러플 파스타",
            "visited": True,
        },
        {
            "name": "필동면옥",
            "famous_for": "평양냉면",
            "cuisine_type": "한식",
            "history": "평양냉면",
            "visited": True,
        },
        {
            "name": "임병주산동손칼국수",
            "famous_for": "칼국수",
            "cuisine_type": "한식",
            "history": "칼국수, 콩국수, 만두",
            "visited": True,
        },
    ]

    render_dict["restaurant_list"] = restaurant_list

    return render(request, "book/food.html", render_dict)


@login_required
def image(request, data_type="pokemon"):
    """이미지 등록."""
    render_dict = get_render_dict(data_type)
    if data_type != "pokemon" and data_type != "people":
        raise KeyError("{} is not valid data_type".format(data_type))

    if request.POST:
        try:
            url = request.POST["url"]
            category_id = request.POST["category"]

            if data_type == "pokemon":
                result = requests.get(url)
                render_dict["result"] = result.text

                bs = BeautifulSoup(result.text, "html.parser")
                # directory list
                all_a = bs.findAll("a", text=True)

                for a in all_a:
                    views_api.add_image_client.delay(
                        "{}".format(a), url, category_id, data_type
                    )
                render_dict["parsed"] = all_a

            elif data_type == "people":
                result = requests.get(url)
                render_dict["result"] = result.text

                bs = BeautifulSoup(result.text, "html.parser")
                all_a = bs.findAll("a", text=True)
                render_dict["parsed"] = all_a

                for a in all_a:
                    views_api.add_image_client.delay(
                        "{}".format(a), url, category_id, data_type
                    )

        except KeyError:
            if "parsed" in render_dict:
                render_dict["parsed"] += traceback.format_exc()
            else:
                render_dict["parsed"] = traceback.format_exc()

    category_list = models.Category.objects.all()
    render_dict["data_type"] = data_type
    render_dict["category_list"] = category_list
    return render(request, "book/add_image.html", render_dict)


@login_required
def pokemon(request, page=1):
    """포켓몬 분류 페이지."""
    render_dict = get_render_dict("pokemon_classification")

    query = request.GET.get("query", "")

    distinct = (
        models.PokemonImage.objects.filter(classified="yes")
        .order_by()
        .values("original_label")
        .distinct()
        .annotate(Count("id"))
        .order_by("id__count")
    )
    distinct = utils.to_table(distinct, 5)
    render_dict["distinct"] = distinct

    if query:
        image_list = (
            models.PokemonImage.objects.filter(original_label__icontains=query)
            .filter(classified=None)
            .order_by("?")[:400]
        )
    else:
        image_list = models.PokemonImage.objects.filter(classified=None).order_by("?")

    p, page_info = utils.get_page_info(image_list, page, 20)
    render_dict["image_list"] = p
    render_dict["page_info"] = page_info
    render_dict["query"] = query

    return render(request, "book/pokemon/pokemon.html", render_dict)


@login_required
def pokemon_sorted(request):
    """Yes 순 정렬 페이지."""
    render_dict = get_render_dict("pokemon_sorted")

    query = request.GET.get("query", "")

    image_list = models.PokemonRating.objects.filter(deep_model__latest=True).filter(
        image__classified=None
    )
    if query:
        image_list = image_list.filter(image__original_label__icontains=query)

    image_list = image_list.order_by("-positive")[:50]

    render_dict["image_list"] = [rating.image for rating in image_list]
    render_dict["query"] = query

    return render(request, "book/pokemon/pokemon.html", render_dict)


@login_required
def pokemon_result(request, page=1):
    """포켓몬 분류 결과."""
    classified = request.GET.get("arg", "yes")
    render_dict = get_render_dict("pokemon_result_{}".format(classified))

    query = request.GET.get("query", "")
    image_list = models.PokemonImage.objects.filter(classified=classified)

    distinct = (
        image_list.order_by()
        .values("original_label")
        .distinct()
        .annotate(Count("id"))
        .order_by("id__count")
    )
    distinct = utils.to_table(distinct, 5)

    if query:
        image_list = image_list.filter(original_label=query)
    p, page_info = utils.get_page_info(image_list, page, 100)

    render_dict["distinct"] = distinct
    render_dict["image_list"] = p
    render_dict["page_info"] = page_info
    render_dict["arg"] = classified

    verified_count = image_list.count()
    row_count = 10
    verified_table = utils.to_table(p, row_count)
    render_dict["query"] = query
    render_dict["verified_table"] = verified_table
    render_dict["verified_count"] = verified_count

    return render(request, "book/pokemon/pokemon_result.html", render_dict)


@login_required
def pokemon_export(request, classified="yes", page=1):
    """포켓몬 분류 결과 출력."""
    count = 1000
    image_list = models.PokemonImage.objects.filter(classified=classified)

    return utils.get_compressed_result(image_list, count, page)


@login_required
def pokemon_relabel(request):
    """포켓몬 분류 결과 수정."""
    render_dict = get_render_dict("pokemon_relabel")
    query = request.GET.get("query", "")

    if query:
        objects = models.PokemonImage.objects.filter(url__endswith=query)

        rating_list = []
        for obj in objects:
            rating_list.append(models.PokemonRating.objects.filter(image=obj))
        render_dict["objects"] = zip(objects, rating_list)

    render_dict["query"] = query

    return render(request, "book/pokemon/pokemon_relabel.html", render_dict)


def compute_expectation(x, coeff):
    """코로나 예상치 계산."""
    value = coeff["a"] / (1 + math.exp(-(x - coeff["x0"]) / coeff["b"]))
    return value


corona_constant = {
    "Korea": {
        "confirmed": {"a": 6591.4785, "b": 2.7211623, "x0": 36.688503},
        "death": {"a": 17.149622, "b": 1.7989516, "x0": 31.290888},
    },
    "China": {
        "confirmed": {"a": 80307.234, "b": 4.234807, "x0": 18.250608},
        "death": {"a": 3089.586, "b": 6.176563, "x0": 24.240225},
    },
}


def range_date(start: datetime.date, end: datetime.date) -> typing.List[datetime.date]:
    """시작부터 끝까지 Date Range."""
    diff = (end - start).days

    for i in range(diff):
        yield start + datetime.timedelta(days=i)


def corona(request):
    """코로나 그래프."""
    render_dict = get_render_dict("corona")

    corona_list = models.Corona.objects.order_by("date")
    if not corona_list:
        return render(request, "book/corona.html", render_dict)

    start_date = corona_list[0].date
    end_date = datetime.date.today() + datetime.timedelta(days=10)

    labels = []

    for date in range_date(start_date, end_date):
        labels.append(date)

    render_dict["labels"] = labels

    country_list = []
    for country in ["China", "Korea"]:
        counts = models.Corona.objects.filter(country=country).order_by("date")

        actual_start_date = counts[0].date

        count_list = []
        for count_type in ["confirmed", "death"]:
            actual = []
            for _ in range_date(start_date, actual_start_date):
                actual.append("NaN")

            for count in counts:
                actual.append(getattr(count, count_type))

            expected = []
            param = corona_constant[country][count_type]

            # for _ in range_date(start_date, actual_end_date):
            #     expected.append("NaN")

            for date in range_date(start_date, end_date):
                off = (date - start_date).days + 1
                if country == "Korea":
                    off = off - 3
                value = compute_expectation(off, param)
                expected.append(value)

            count_list.append((count_type, actual, expected))
        country_list.append((country, count_list))

    render_dict["country_list"] = country_list
    return render(request, "book/corona.html", render_dict)


@user_passes_test(lambda u: u.is_superuser)
def add_user(request):
    """신규 인스타 유저 등록."""
    user = request.GET["username"]
    checked = request.GET["checked"]

    obj = models.User.objects.get(username=user)
    obj.checked = checked
    obj.save()

    return HttpResponse("1")


@user_passes_test(lambda u: u.is_superuser)
def relabel(request):
    """레이블 수정."""
    render_dict = get_render_dict("people_relabel")
    query = request.GET.get("query", "")

    if query:
        objects = models.PeopleImage.objects.filter(url__endswith=query)
        render_dict["objects"] = objects
    render_dict["query"] = query

    return render(request, "book/people/people_relabel.html", render_dict)


def server_error_page(request):
    """Error page for 500 error."""
    response = render(request, "book/error/500.html")
    response.status_code = 500
    return response
