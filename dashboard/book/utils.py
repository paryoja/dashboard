import base64
import json

import lz4.frame
import requests
from django.core import exceptions, serializers
from django.core.paginator import Paginator
from django.http import HttpResponse

from .models import Lotto


def new_lotto(draw_number):
    is_new = False
    try:
        obj = Lotto.objects.get(draw_number=draw_number)
        result = obj.numbers
    except exceptions.ObjectDoesNotExist:
        try:
            params = {
                "method": "getLottoNumber",
                "drwNo": draw_number,
            }
            result = requests.get("https://www.nlotto.co.kr/common.do", params=params)
            result = json.loads(result.text)
            if not result["returnValue"] == "fail":
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
        "page": page,
        "prev": page - 1 if p.has_previous() else 0,
        "next": page + 1 if p.has_next() else 0,
        "page_list": page_list,
    }

    return p, page_info


def get_compressed_result(image_list, count, page):
    paginator = Paginator(image_list, count)
    p = paginator.page(page)

    image_list = serializers.serialize("json", p)

    result = {"has_next": p.has_next(), "image_list": json.loads(image_list)}

    compressed = lz4.frame.compress(json.dumps(result).encode("utf-8"))
    return HttpResponse(base64.b85encode(compressed))


def to_table(contents, row_count):
    table = []
    row = []
    for count, img in enumerate(contents):
        row.append(img)
        count += 1

        if count % row_count == 0:
            row = []
            table.append(row)
    if row:
        table.append(row)

    return table
