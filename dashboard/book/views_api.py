import json

import requests
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


def people_classification_api(request):
    img_id = request.POST.get('image_id')
    if img_id:
        int_img_id = int(img_id.split('_')[1])
        img = models.PeopleImage.objects.get(id=int_img_id)
        data = {
            'requested_url': img.url
        }
        headers = {
            'Content-Type': 'application/json'
        }
        server = models.APIServers.objects.get(title="people_class")

        result = requests.post('http://{}:8000/people_classification'.format(server.ip),
                               json=data, headers=headers)
        response = {
            'img_id': img_id,
            'classification': json.loads(result.text)
        }
        return JsonResponse(response)
    return HttpResponseBadRequest("No Image Id")
