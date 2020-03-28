import json
import logging
import re
import typing

import requests
import urllib3
from book import models
from bs4 import BeautifulSoup
from celery import shared_task
from django.db import models as dj_models
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse

logger = logging.getLogger(__name__)

a_pattern = re.compile('<a href="(.+?)">(.+?)</a>')


class Domain:
    People = "people"
    Pokemon = "pokemon"


def image(request, method, image_type="People") -> HttpResponse:
    image_id = request.POST.get("image_id")
    if image_id is None:
        return HttpResponseBadRequest("Empty Image Id")
    if image_type == "People":
        img = models.PeopleImage.objects.get(id=int(image_id))
    elif image_type == "Pokemon":
        img = models.PokemonImage.objects.get(id=int(image_id))
    else:
        raise ValueError("Unknown image type {}".format(image_type))

    if method == "DELETE":
        img.delete()
        return HttpResponse("Done")
    if method == "GET":
        return JsonResponse(model_to_dict(img))
    else:
        return HttpResponseBadRequest("Unknown Method")


def set_rating(request) -> HttpResponse:
    img_id = int(request.POST.get("image_id"))
    data_type = request.POST.get("data_type")
    if data_type == Domain.Pokemon:
        img = models.PokemonImage.objects.get(id=img_id)
        img.classified = request.POST.get("selected").lower()
    elif data_type == Domain.People:
        img = models.PeopleImage.objects.get(id=img_id)
        selected = request.POST.get("selected").lower()
        img.selected = selected == "true" or selected == "yes"
    else:
        return HttpResponseBadRequest("Not Supported data_type {}".format(data_type))

    img.save()
    return HttpResponse(request.POST.get("selected"))


def get_id(request) -> HttpResponse:
    query = request.POST.get("query")
    image_obj = models.PeopleImage.objects.filter(url__endswith=query)[0]
    return HttpResponse(image_obj.id)


def get_img_rating(
    domain, int_img_id
) -> typing.Tuple[
    typing.Union[models.PokemonImage, models.PokemonImage], dj_models.query.QuerySet
]:
    if domain == Domain.People:
        img = models.PeopleImage.objects.get(id=int_img_id)
        existing_rating = models.Rating.objects.filter(
            image_id=int_img_id, deep_model__domain=domain, deep_model__latest=True
        )
    elif domain == Domain.Pokemon:
        img = models.PokemonImage.objects.get(id=int_img_id)
        existing_rating = models.PokemonRating.objects.filter(
            image_id=int_img_id, deep_model__domain=domain, deep_model__latest=True
        )
    else:
        message = "Domain {} unknown".format(domain)
        logger.warning(message)
        raise KeyError(message)
    return img, existing_rating


def save_success(
    domain: str,
    json_data: dict,
    target_deep_model: models.DeepLearningModel,
    int_img_id: int,
) -> None:
    if domain == Domain.People:
        class_names = json_data["class_names"]
        positive = json_data["classification"][class_names["True"]]
        rating = models.Rating(
            deep_model=target_deep_model,
            image_id=int_img_id,
            data=json_data,
            positive=positive,
        )
        rating.save()

    elif domain == Domain.Pokemon:
        class_names = json_data["class_names"]
        positive = json_data["classification"][class_names["yes"]]
        rating = models.PokemonRating(
            deep_model=target_deep_model,
            image_id=int_img_id,
            data=json_data,
            positive=positive,
        )
        rating.save()


def save_failure(
    domain: str,
    json_data: dict,
    target_deep_model: models.DeepLearningModel,
    int_img_id: int,
) -> None:
    if domain == Domain.People:
        rating = models.Rating(
            deep_model=target_deep_model, image_id=int_img_id, data=json_data
        )
        rating.save()

    elif domain == Domain.Pokemon:
        rating = models.PokemonRating(
            deep_model=target_deep_model, image_id=int_img_id, data=json_data
        )
        rating.save()


def call_api_server(img, domain: str) -> typing.Optional[requests.Response]:
    data = {"requested_url": img.url}
    headers = {"Content-Type": "application/json"}

    server = models.APIServers.objects.get(title=domain)

    request_url = "http://{}:{}/{}".format(server.ip, server.port, server.endpoint)
    try:
        result = requests.post(request_url, json=data, headers=headers)
    except urllib3.exceptions.MaxRetryError as e:
        logger.warning("Max tries failed {}".format(request_url))
        raise e
    except requests.exceptions.ConnectionError as e:
        logger.warning("Connection Refused {}".format(request_url))
        raise e

    if result.status_code != 200:
        logger.warning(result.text, result.status_code)
        return None
    return result


@shared_task
def get_classification_result(domain: str, int_img_id: int) -> None:
    img, existing_rating = get_img_rating(domain, int_img_id)

    # 이미 가져온건지 다시 확인 -> 작업 추가시에 중복되어 있을 수 있음
    if existing_rating.count() != 0:
        return

    result = call_api_server(img, domain)
    if not result:
        return
    json_data = json.loads(result.text)

    # 신규 모델인지 확인
    deep_model_filter = models.DeepLearningModel.objects.filter(domain=domain)

    new_model = True
    target_deep_model = None
    for deep_model in deep_model_filter:
        if deep_model.version == json_data["version"]:
            new_model = False
            target_deep_model = deep_model
            break

    # 신규 모델 생성
    if new_model:
        for deep_model in deep_model_filter:
            deep_model.latest = False
            deep_model.save()
        target_deep_model = models.DeepLearningModel(
            domain=domain, version=json_data["version"]
        )
        target_deep_model.save()

    if json_data["status"] == "success":
        save_success(domain, json_data, target_deep_model, int_img_id)
    else:
        save_failure(domain, json_data, target_deep_model, int_img_id)


def get_response(img_id: str, domain: str) -> dict:
    int_img_id = int(img_id.split("_")[1])

    # 이미 존재하는지 체크
    if domain == Domain.People:
        existing_rating = models.Rating.objects.filter(
            image_id=int_img_id, deep_model__domain=domain, deep_model__latest=True
        )
    elif domain == Domain.Pokemon:
        existing_rating = models.PokemonRating.objects.filter(
            image_id=int_img_id, deep_model__domain=domain, deep_model__latest=True
        )
    else:
        raise KeyError("Unknown domain {}".format(domain))

    need_to_request = True

    json_data = None
    if existing_rating.count() != 0:
        # 존재함 -> 최신 모델인지 확인
        for rating in existing_rating:
            if rating.deep_model.latest:
                need_to_request = False
                json_data = rating.data
                break

    if need_to_request:
        # 미존재 혹은 최신 평가치 없음 -> 평가 요청
        get_classification_result.delay(domain, int_img_id)
        json_data = {"status": "requested", "classification": ["?", "?"], "label": "?"}

    response = {"img_id": img_id, "classification": json_data}

    return response


def people_classification_api(request) -> HttpResponse:
    img_id = request.POST.get("image_id")
    if img_id:
        response = get_response(img_id, domain=Domain.People)

        return JsonResponse(response)
    return HttpResponseBadRequest("No Image Id")


def pokemon_classification_api(request) -> HttpResponse:
    img_id = request.POST.get("image_id")
    if img_id:
        response = get_response(img_id, domain=Domain.Pokemon)
        return JsonResponse(response)
    return HttpResponseBadRequest("No Image Id")


def get_image_directory_list(data_type, url, a_parsed) -> list:
    if data_type == "people":
        json_url = url + a_parsed[0][0] + "/image.json"
        image_list_text = requests.get(json_url).text
        try:
            result = json.loads(image_list_text)["image_list"]
        except json.JSONDecodeError as e:
            raise e

    elif data_type == "pokemon":
        directory_url = url + a_parsed[0][0]
        image_result = requests.get(directory_url)
        bs = BeautifulSoup(image_result.text, "html.parser")

        all_a = bs.findAll("a", text=True)
        result = []
        for a in all_a:
            image_a_parsed = a_pattern.findall("{}".format(a))
            logger.info(image_a_parsed)
            if not image_a_parsed[0][0].startswith("../"):
                result.append(directory_url + image_a_parsed[0][0])

    else:
        raise ValueError("Unsupported data_type {}".format(data_type))

    return result


@shared_task
def add_image_client(a_text, url, category_id, data_type) -> None:
    a_parsed = a_pattern.findall(a_text)

    if not a_parsed[0][0].startswith("../"):
        result = get_image_directory_list(data_type, url, a_parsed)
        for img in result:
            try:
                if data_type == "people":
                    image_obj = models.PeopleImage(
                        url=url + a_parsed[0][0] + img["local"],
                        title=img["alt"][:500],
                        category_id=category_id,
                        page=img["a"],
                    )
                elif data_type == "pokemon":
                    path = img.split("/")
                    image_obj = models.PokemonImage(
                        url=img,
                        title=path[-1],
                        category_id=category_id,
                        original_label=path[-2],
                    )
                else:
                    raise ValueError("Unsupported data_type {}".format(data_type))
                image_obj.save()
            except Exception:
                continue


@shared_task
def cron_image_add() -> None:
    try:
        category_id = "people"
        data_type = "people"
        url = models.APIServers.objects.filter(title="people_image")[0]
        url_text = "http://{}:{}/{}".format(url.ip, url.port, url.endpoint)
        result = requests.get(url_text)
        bs = BeautifulSoup(result.text, "html.parser")
        all_a = bs.findAll("a", text=True)

        for a in all_a:
            add_image_client.delay("{}".format(a), url_text, category_id, data_type)

    except Exception as e:
        raise Exception("Error {}".format(e))
