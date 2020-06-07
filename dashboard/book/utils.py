"""유틸 함수."""
import base64
import csv
import json
import typing

import lz4.frame
import requests
from django import forms
from django.contrib import admin
from django.core import exceptions, serializers
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import path

from .models import Lotto


class CsvImportForm(forms.Form):
    """CSV Import 시 사용할 Form."""

    csv_file = forms.FileField()


class ExportCsvMixin(admin.ModelAdmin):
    """CSV Export 기능 제공용 Mixin."""

    csv_file = forms.FileField()
    field_names = None

    def export_as_csv(self, request, queryset):
        """CSV으로 Export."""
        meta = self.model._meta
        if self.field_names:
            field_names = self.field_names
        else:
            field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

    def get_urls(self):
        """Get urls."""
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        """Import CSV File."""
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            reader = csv.DictReader(
                csv_file.read().decode("utf-8").splitlines(), delimiter=","
            )
            for r in reader:
                if "id" in r:
                    r["id"] = int(r["id"])
                obj = self.model(**r)
                obj.save()

            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(request, "admin/csv_form.html", payload)


def new_lotto(draw_number):
    """로또 정보."""
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
            # https://www.nlotto.co.kr/common.do?method=getLottoNumber&drwNo=912
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
    """페이지 정보."""
    paginator = Paginator(object_list, count)
    p = paginator.page(page)

    start_10 = (page - 1) // 10 * 10 + 1
    end_10 = min(start_10 + 9, paginator.num_pages)

    page_list = [i for i in range(start_10, end_10 + 1)]

    page_info = {
        "page": page,
        "prev": page - 1 if p.has_previous() else 0,
        "next": page + 1 if p.has_next() else 0,
        "page_list": page_list,
    }

    return p, page_info


def get_compressed_result(image_list, count, page):
    """데이터 압축해서 제공."""
    paginator = Paginator(image_list, count)
    p = paginator.page(page)

    image_list = serializers.serialize("json", p)

    result = {"has_next": p.has_next(), "image_list": json.loads(image_list)}

    compressed = lz4.frame.compress(json.dumps(result).encode("utf-8"))
    return HttpResponse(base64.b85encode(compressed))


def to_table(contents: typing.List, row_count: int) -> typing.List[typing.List]:
    """
    테이블 형태로 grouping.

    :param contents: list 형태의 데이터.
    :param row_count: 한줄에 포함될 element 개수
    :return: grouping 된 테이블
    """
    row = []
    table = []
    for count, img in enumerate(contents):
        row.append(img)
        count += 1

        if count % row_count == 0:
            table.append(row)
            row = []
    if row:
        table.append(row)

    return table
