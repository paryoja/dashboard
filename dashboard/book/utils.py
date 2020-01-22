import json

import requests
from django.core import exceptions
from django.core.paginator import Paginator

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


def get_page_info(object_list, page, count):
    pagenator = Paginator(object_list, count)
    p = pagenator.page(page)

    start_10 = (page - 1) // 10 * 10 + 1
    end_10 = min(start_10 + 9, pagenator.num_pages)

    page_list = [i for i in range(start_10, end_10 + 1)]

    page_info = {
        'page': page,
        'prev': page - 1 if p.has_previous() else 0,
        'next': page + 1 if p.has_next() else 0,
        'page_list': page_list,
    }

    return p, page_info
