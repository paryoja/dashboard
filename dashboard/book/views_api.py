import json

import requests
import urllib3
from celery import shared_task
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse

from . import models


class Domain:
    People = "people"
    Pokemon = "pokemon"


def image(request, method):
    if method == "DELETE":
        image_id = request.POST.get("image_id")
        img = models.PeopleImage.objects.get(id=int(image_id))
        img.delete()
        return HttpResponse("Done")
    if method == "GET":
        image_id = request.POST.get("image_id")
        img = models.PeopleImage.objects.get(id=image_id)
        return JsonResponse(model_to_dict(img))
    else:
        return HttpResponseBadRequest("Unknown Method")


def set_rating(request):
    img_id = int(request.POST.get('image_id'))
    data_type = request.POST.get('data_type')
    if data_type == Domain.Pokemon:
        img = models.PokemonImage.objects.get(id=img_id)
        img.classified = request.POST.get('selected').lower()
    elif data_type == Domain.People:
        img = models.PeopleImage.objects.get(id=img_id)
        img.selected = request.POST.get('selected').lower() == 'yes'
    else:
        return HttpResponseBadRequest("Not Supported data_type {}".format(data_type))

    img.save()
    return HttpResponse(request.POST.get('selected'))


def get_id(request):
    query = request.POST.get('query')
    image = models.PeopleImage.objects.filter(url__endswith=query)[0]
    return HttpResponse(image.id)


@shared_task
def get_classification_result(domain, int_img_id):
    if domain == Domain.People:
        img = models.PeopleImage.objects.get(id=int_img_id)
        existing_rating = models.Rating.objects.filter(image_id=int_img_id,
                                                       deep_model__domain=domain,
                                                       deep_model__latest=True)
    elif domain == Domain.Pokemon:
        img = models.PokemonImage.objects.get(id=int_img_id)
        existing_rating = models.PokemonRating.objects.filter(image_id=int_img_id,
                                                              deep_model__domain=domain,
                                                              deep_model__latest=True)
    else:
        raise KeyError("Domain {} unknown".format(domain))

    # 이미 가져온건지 다시 확인 -> 작업 추가시에 중복되어 있을 수 있음
    need_to_request = True
    if existing_rating.count() != 0:
        return

    data = {
        'requested_url': img.url
    }
    headers = {
        'Content-Type': 'application/json'
    }

    server = models.APIServers.objects.get(title=domain)

    request_url = 'http://{}:{}/{}'.format(server.ip, server.port, server.endpoint)
    try:
        result = requests.post(request_url,
                               json=data, headers=headers)
    except urllib3.exceptions.MaxRetryError:
        print("Max tries failed {}".format(request_url))
        return
    except requests.exceptions.ConnectionError:
        print("Connection Refused".format(request_url))
        return

    if result.status_code != 200:
        print(result.text, result.status_code)
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
        target_deep_model = models.DeepLearningModel(domain=domain, version=json_data["version"])
        target_deep_model.save()

    if json_data["status"] == "success":
        if domain == Domain.People:
            class_names = json_data["class_names"]
            positive = json_data["classification"][class_names["True"]]
            rating = models.Rating(deep_model=target_deep_model, image_id=int_img_id,
                                   data=json_data, positive=positive)
            rating.save()

        elif domain == Domain.Pokemon:
            class_names = json_data["class_names"]
            positive = json_data["classification"][class_names["yes"]]
            rating = models.PokemonRating(deep_model=target_deep_model, image_id=int_img_id,
                                          data=json_data, positive=positive)
            rating.save()
    else:
        if domain == Domain.People:
            rating = models.Rating(deep_model=target_deep_model, image_id=int_img_id,
                                   data=json_data)
            rating.save()

        elif domain == Domain.Pokemon:
            rating = models.PokemonRating(deep_model=target_deep_model, image_id=int_img_id,
                                          data=json_data)
            rating.save()


def get_response(img_id, domain):
    int_img_id = int(img_id.split('_')[1])

    # 이미 존재하는지 체크
    if domain == Domain.People:
        existing_rating = models.Rating.objects.filter(image_id=int_img_id,
                                                       deep_model__domain=domain,
                                                       deep_model__latest=True)
    elif domain == Domain.Pokemon:
        existing_rating = models.PokemonRating.objects.filter(image_id=int_img_id,
                                                              deep_model__domain=domain,
                                                              deep_model__latest=True)
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
        json_data = {
            'status': 'requested',
            'classification': ['?', '?'],
            'label': '?'
        }

    response = {
        'img_id': img_id,
        'classification': json_data
    }

    return response


def people_classification_api(request):
    img_id = request.POST.get('image_id')
    if img_id:
        response = get_response(img_id, domain=Domain.People)

        return JsonResponse(response)
    return HttpResponseBadRequest("No Image Id")


def pokemon_classification_api(request):
    img_id = request.POST.get('image_id')
    if img_id:
        response = get_response(img_id, domain=Domain.Pokemon)
        return JsonResponse(response)
    return HttpResponseBadRequest("No Image Id")
