from django.http import HttpResponse

from . import models


def set_rating(request):
    img = models.PeopleImage.objects.get(id=int(request.POST.get('image_id')))
    img.selected = request.POST.get('selected').lower() == 'yes'
    img.save()
    return HttpResponse(request.POST.get('selected'))
