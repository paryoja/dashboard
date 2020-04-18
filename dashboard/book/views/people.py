"""인스타그램 내용 파싱."""
import requests
from book import models, utils
from book.nav import get_render_dict
from book.templatetags import book_extras
from celery import shared_task
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.shortcuts import render


@user_passes_test(lambda u: u.is_superuser)
def people(request):
    """
    이미지 제공.

    :param request:
    :return:
    """
    render_dict = get_render_dict("people")

    query = request.GET.get("query", "")

    unclassified = models.PeopleImage.objects.filter(selected=None, rating=None)
    unclassified_count = unclassified.count()

    distinct = (
        unclassified.order_by()
        .values("user_id")
        .distinct()
        .annotate(Count("id"))
        .order_by("id__count")
    )
    distinct = utils.to_table(distinct, 5)

    render_dict["distinct"] = distinct

    query_count = unclassified.filter(title__contains=query).count()
    image_list = unclassified.filter(title__contains=query).order_by("?")[:100]

    render_dict["unclassified_count"] = unclassified_count
    render_dict["query_count"] = query_count
    render_dict["distinct"] = distinct

    if query:
        id_select = unclassified.filter(url__contains=query)
        render_dict["query_count"] += id_select.count()
        render_dict["image_list"] = id_select[:50].values() | image_list.values()
    else:
        render_dict["image_list"] = image_list.values()
    render_dict["query"] = query

    return render(request, "book/people/people.html", render_dict)


@user_passes_test(lambda u: u.is_superuser)
def people_result(request, page=1):
    """분류 결과 선택."""
    selected = request.GET.get("arg", "True")
    render_dict = get_render_dict("people_result_{}".format(selected))
    render_dict["arg"] = selected

    selected = selected == "True"
    query = request.GET.get("query", "")
    selected_list = models.PeopleImage.objects.filter(selected=selected)

    distinct = (
        selected_list.order_by()
        .values("user_id")
        .distinct()
        .annotate(Count("id"))
        .order_by("-id__count")
    )
    distinct = utils.to_table(distinct, 5)
    render_dict["distinct"] = distinct

    if query:
        queried_list = selected_list.filter(url__contains=query)
        selected_list = queried_list | selected_list.filter(title__contains=query)
    else:
        selected_list = models.PeopleImage.objects.filter(selected=selected)
    selected_list = selected_list.order_by("-id")
    p, page_info = utils.get_page_info(selected_list, page, 120)

    row_count = 6
    people_table = utils.to_table(p, row_count)

    render_dict["people_table"] = people_table
    render_dict["page_info"] = page_info
    render_dict["query"] = query

    return render(request, "book/people/people_result.html", render_dict)


@user_passes_test(lambda u: u.is_superuser)
def people_high_expectation(request):
    """우선순위 순으로 보여줌."""
    render_dict = get_render_dict("people_high_expectation")

    query = request.GET.get("query", "")
    order = request.GET.get("order", "decreasing")

    selected_list = models.Rating.objects.filter(
        image__selected=None, deep_model__latest=True
    ).select_related("image")
    render_dict["unclassified_count"] = selected_list.count()

    if query:
        queried_list = selected_list.filter(image__url__contains=query)[:100]
        selected_list = (
            queried_list | selected_list.filter(image__title__contains=query)[:100]
        )

    render_dict["query_count"] = selected_list.count()

    if order == "decreasing":
        selected_list = selected_list.order_by("-positive")[:100]
    elif order == "increasing":
        selected_list = selected_list.order_by("positive")[:100]
    else:
        selected_list = selected_list.order_by("?")[:100]

    unclassified = [rating.image for rating in selected_list]

    render_dict["rating"] = selected_list

    render_dict["image_list"] = unclassified
    render_dict["query"] = query

    return render(request, "book/people/people.html", render_dict)


@shared_task
def get_new_people_links():
    """
    인스타그램 text 속에 있는 user link 추출 후 링크 제공.

    :return:
    """
    selected_list = models.PeopleImage.objects.filter(title__contains="@").filter(
        content_parsed=None
    )[:100]

    new_id = 0
    user_names = set()

    for selected_image in selected_list:
        names = book_extras.user_pattern.findall(selected_image.title)
        for name in names:
            if not models.User.objects.filter(username=name).exists():
                user_names.add(name)
                new_id += 1
        selected_image.content_parsed = True
        selected_image.save()

    while user_names:
        user = user_names.pop()
        r = requests.get("https://www.instagram.com/" + user)
        if r.status_code == 200:
            models.User(username=user, checked=None).save()
        else:
            models.User(username=user, checked=False).save()


@user_passes_test(lambda u: u.is_superuser)
def people_links(request):
    """링크 제공."""
    render_dict = get_render_dict("people_result")

    get_new_people_links.delay()
    verified = models.User.objects.filter(checked=None)

    render_dict["user_names"] = verified
    return render(request, "book/people/people_links.html", render_dict)


@user_passes_test(lambda u: u.is_superuser)
def people_result_download(_, selected, page):
    """이미지 통합 다운로드."""
    image_list = models.PeopleImage.objects.filter(selected=selected).only(
        "url", "selected", "page"
    )

    count = 1000
    return utils.get_compressed_result(image_list, count, page)
