import json

import requests
from celery import shared_task
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse

from . import models


def set_rating(request):
    img_id = int(request.POST.get('image_id'))
    data_type = request.POST.get('data_type')
    if data_type == "pokemon":
        img = models.PokemonImage.objects.get(id=img_id)
        img.classified = request.POST.get('selected').lower()
    elif data_type == "people":
        img = models.PeopleImage.objects.get(id=img_id)
        img.selected = request.POST.get('selected').lower() == 'yes'
    else:
        return HttpResponseBadRequest("Not Supported data_type {}".format(data_type))

    img.save()
    return HttpResponse(request.POST.get('selected'))


@shared_task
def get_classification_result(int_img_id):
    img = models.PeopleImage.objects.get(id=int_img_id)
    data = {
        'requested_url': img.url
    }
    headers = {
        'Content-Type': 'application/json'
    }
    
    # 이미 가져온건지 다시 확인 -> 작업 추가시에 중복되어 있을 수 있음
    existing_rating = models.Rating.objects.filter(image_id=int_img_id)
    need_to_request = True
    for rating in existing_rating:
        if rating.deep_model.domain == "people" and rating.deep_model.latest:
            need_to_request = False
            break

    if not need_to_request:
        return

    server = models.APIServers.objects.get(title="people_class")

    result = requests.post('http://{}:8000/people_classification'.format(server.ip),
                           json=data, headers=headers)
    json_data = json.loads(result.text)

    # 신규 모델인지 확인
    deep_model_filter = models.DeepLearningModel.objects.filter(domain="people")

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
        target_deep_model = models.DeepLearningModel(domain="people", version=json_data["version"])
        target_deep_model.save()

    rating = models.Rating(deep_model=target_deep_model, image_id=int_img_id,
                           data=json_data, positive=json_data["classification"][0])
    rating.save()


def people_classification_api(request):
    img_id = request.POST.get('image_id')
    if img_id:
        int_img_id = int(img_id.split('_')[1])

        # 이미 존재하는지 체크
        existing_rating = models.Rating.objects.filter(image_id=int_img_id)

        need_to_request = True

        json_data = None
        if existing_rating.count() != 0:
            # 존재함 -> 최신 모델인지 확인
            for rating in existing_rating:
                if rating.deep_model.domain == "people" and rating.deep_model.latest:
                    need_to_request = False
                    json_data = rating.data
                    break

        if need_to_request:
            # 미존재 혹은 최신 평가치 없음 -> 평가 요청
            get_classification_result.delay(int_img_id)
            json_data = {
                'status': 'requested',
                'classification': ['?', '?'],
                'label': '?'
            }

        response = {
            'img_id': img_id,
            'classification': json_data
        }

        return JsonResponse(response)
    return HttpResponseBadRequest("No Image Id")
