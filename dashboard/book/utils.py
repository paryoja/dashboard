import json

import requests
from django.core import exceptions

from .models import Lotto


def new_lotto(draw_number):
    is_new = False
    try:
        obj = Lotto.objects.get(draw_number=draw_number)
        result = obj.numbers
    except exceptions.ObjectDoesNotExist:
        try:
            params = {
                'method': 'getLottoNumber',
                'drwNo': draw_number,
            }
            result = requests.get(
                "https://www.nlotto.co.kr/common.do", params=params)
            result = json.loads(result.text)
            if not result['returnValue'] == 'fail':
                obj = Lotto(draw_number=draw_number, numbers=result)
                obj.save()
                is_new = True
        except Exception as e:
            result = str(e)

    return result, is_new
