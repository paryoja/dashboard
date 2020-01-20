from django.http import HttpResponse, HttpResponseBadRequest

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
