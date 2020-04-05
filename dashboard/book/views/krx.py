"""KRX 데이터 파싱."""

import logging

from book import models
from book.nav import get_render_dict
from book.xml_helper import XmlDictConfig, get_xml_request
from django.core import exceptions
from django.shortcuts import render

logger = logging.getLogger(__name__)

krx_price_query_url = "http://asp1.krx.co.kr/servlet/krx.asp.XMLSise?code={}"
krx_statement_query_url = "http://asp1.krx.co.kr/servlet/krx.asp.XMLJemu?code={}"
balance_order = [
    "hangMok",
    "year1Money",
    "year1GuSungRate",
    "year1JungGamRate",
    "year2Money",
    "year2GuSungRate",
    "year2JungGamRate",
    "year3Money",
    "year3GuSungRate",
    "year3JungGamRate",
]
cash_order = [
    "hangMok",
    "year1Money",
    "year1JungGamRate",
    "year2Money",
    "year2JungGamRate",
    "year3Money",
    "year3JungGamRate",
]


def krx_realtime(realtime_result, query, render_dict):
    """실시간 데이터 분석."""
    realtime_json = XmlDictConfig(realtime_result[1].find("stockInfo"))
    info_json = XmlDictConfig(realtime_result[1].find("TBL_StockInfo"))
    render_dict["market_close"] = (
        realtime_json["myJangGubun"] == "장마감" or realtime_json["myJangGubun"] == "장개시전"
    )
    render_dict["realtime_result"] = (
        realtime_json,
        realtime_result[0],
        info_json,
    )

    if "JongName" in info_json and info_json["JongName"]:
        try:
            models.Stock.objects.get(code=query)
        except exceptions.ObjectDoesNotExist:
            stock = models.Stock(code=query, name=info_json["JongName"])
            stock.save()


def krx_statement(statement_result, render_dict):
    """회계정보 분석."""
    balance_sheet = XmlDictConfig(statement_result[1].find("TBL_DaeCha"))
    if "TBL_DaeCha_data" in balance_sheet:
        hangmok_list = []
        for item in balance_sheet["TBL_DaeCha_data"]:
            # 항목 이름 뒤에 숫자를 붙여 둬서 쓰기 어려우므로 제거
            item = {k[:-1]: v for k, v in item.items()}
            hangmok_list.append([item[order] for order in balance_order])
        balance_sheet["TBL_DaeCha_data"] = hangmok_list
        render_dict["balance_sheet"] = balance_sheet

    income_statement = XmlDictConfig(statement_result[1].find("TBL_SonIk"))
    if "TBL_SonIk_data" in income_statement:
        hangmok_list = []
        for item in income_statement["TBL_SonIk_data"]:
            # 항목 이름 뒤에 숫자를 붙여 둬서 쓰기 어려우므로 제거
            item = {k[:-1]: v for k, v in item.items()}
            hangmok_list.append([item[order] for order in balance_order])
        income_statement["TBL_SonIk_data"] = hangmok_list
        render_dict["income_statement"] = income_statement

    cash_flow = XmlDictConfig(statement_result[1].find("TBL_CashFlow"))
    if "TBL_CashFlow_data" in cash_flow:
        hangmok_list = []
        for item in cash_flow["TBL_CashFlow_data"]:
            # 항목 이름 뒤에 숫자를 붙여 둬서 쓰기 어려우므로 제거
            item = {k[:-1]: v for k, v in item.items()}
            hangmok_list.append([item[order] for order in cash_order])
        cash_flow["TBL_CashFlow_data"] = hangmok_list
        render_dict["cash_flow"] = cash_flow
    render_dict["statement_result"] = statement_result


def krx_price_query(request):
    """
    가격 정보.

    :param request:
    :return:
    """
    render_dict = get_render_dict("krx_price_query")
    if request.POST:
        query = request.POST["query"]
        render_dict["query"] = query

        realtime_result = get_xml_request(krx_price_query_url.format(query))
        if realtime_result:
            krx_realtime(realtime_result, query, render_dict)

        statement_result = get_xml_request(krx_statement_query_url.format(query))
        if statement_result:
            krx_statement(statement_result, render_dict)

    stocks = models.Stock.objects.all().order_by("code")
    render_dict["stocks"] = stocks
    return render(request, "book/investment/krx_price_query.html", render_dict)
