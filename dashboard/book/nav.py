from django.conf import settings

VERSION = getattr(settings, "VERSION", "0.0.1")


def get_nav_collapse(child_list, button_url, icon, description) -> dict:
    active = ""
    for item in child_list:
        if item["active"]:
            active = "active"

    return {
        "collapse": True,
        "button_url": button_url,
        "icon": icon,
        "description": description,
        "child_list": child_list,
        "active": active,
    }


def get_nav_item(template, icon, description, current_page, arg=None) -> dict:
    if arg:
        active_page = "{}_{}".format(template, arg)
    else:
        active_page = template

    return {
        "collapse": False,
        "template": "book:{}".format(template),
        "arg": arg,
        "icon": icon,
        "description": description,
        "active": "active" if active_page == current_page else "",
    }


def get_study_sub_list(current_page: str) -> dict:
    study_list = list()
    study_list.append(
        get_nav_item("slide", "fa fa-file-powerpoint", "슬라이드", current_page)
    )
    study_list.append(get_nav_item("paper", "fa fa-file-pdf", "논문", current_page))
    study_list.append(get_nav_item("colab", "fa fa-file-code", "실습자료", current_page))

    collapse = get_nav_collapse(
        study_list, "sidebarLecture", "fa fa-chalkboard-teacher", "스터디 정리"
    )
    return collapse


def get_pokemon_sub_list(current_page: str) -> dict:
    pokemon_result_list = list()
    pokemon_result_list.append(
        get_nav_item("pokemon_result", "far fa-thumbs-up", "적합", current_page, "yes")
    )
    pokemon_result_list.append(
        get_nav_item(
            "pokemon_result", "fa fa-angle-right", "단순 처리", current_page, "little"
        )
    )
    pokemon_result_list.append(
        get_nav_item(
            "pokemon_result", "fa fa-angle-double-right", "복잡 처리", current_page, "more"
        )
    )
    pokemon_result_list.append(
        get_nav_item("pokemon_result", "far fa-thumbs-down", "부적합", current_page, "no")
    )

    pokemon_list = list()
    pokemon_list.append(
        get_nav_item("pokemon_classification", "fa fa-check-square", "분류", current_page)
    )
    pokemon_list.append(
        get_nav_collapse(
            pokemon_result_list, "sidebarPokemonResult", "fa fa-poll", "분류결과"
        )
    )
    pokemon_list.append(
        get_nav_item(
            "pokemon_sorted", "fa fa-sort-numeric-down", "Yes 순 분류", current_page
        )
    )
    pokemon_list.append(
        get_nav_item("pokemon_relabel", "fa fa-edit", "분류 수정", current_page)
    )

    collapse = get_nav_collapse(pokemon_list, "sidebarPokemon", "fa fa-gamepad", "포켓몬")
    return collapse


def get_invest_sub_list(current_page: str) -> dict:
    invest_list = list()
    invest_list.append(
        get_nav_item(
            "leading_stocks", "fa fa-money-check-alt", "Leading Stocks", current_page
        )
    )
    invest_list.append(
        get_nav_item(
            "live_currency", "fa fa-exchange-alt", "Currency History", current_page
        )
    )
    invest_list.append(
        get_nav_item(
            "krx_price_query", "fa fa-search-dollar", "Price Query", current_page
        )
    )
    invest_list.append(
        get_nav_item("lotto", "fa fa-money-bill-wave", "Lottery", current_page)
    )
    invest_list.append(
        get_nav_item("real_estate", "fa fa-building", "부동산", current_page)
    )
    invest_list.append(get_nav_item("recommend_book", "fa fa-book", "책", current_page))

    collapse = get_nav_collapse(invest_list, "sidebarInvest", "fe fe-dollar-sign", "투자")
    return collapse


def get_other_sub_list(current_page: str) -> dict:
    classifier_list = list()
    classifier_list.append(get_nav_item("people", "fa fa-users", "미분류", current_page))
    classifier_list.append(
        get_nav_item("people_result", "fa fa-user-check", "선택", current_page, "True")
    )
    classifier_list.append(
        get_nav_item("people_result", "fa fa-user-times", "미선택", current_page, "False")
    )
    classifier_list.append(
        get_nav_item("people_high_expectation", "fa fa-user-plus", "예상", current_page)
    )
    classifier_list.append(
        get_nav_item("people_relabel", "fa fa-user-edit", "수정", current_page)
    )

    other_list = list()
    other_list.append(get_nav_item("food", "fa fa-utensils", "맛집", current_page))
    other_list.append(get_nav_item("wine", "fa fa-wine-bottle", "Wine", current_page))
    other_list.append(get_nav_item("law_search", "fa fa-gavel", "법률 검색", current_page))
    other_list.append(get_nav_item("todo", "fa fa-check", "Todo List", current_page))
    other_list.append(get_nav_item("algorithm", "fe fe-video", "비디오", current_page))
    other_list.append(
        get_nav_collapse(classifier_list, "sidebarClassifier", "fa fa-tags", "분류기")
    )
    other_list.append(get_nav_item("idea", "fe fe-zap", "아이디어 모음", current_page))
    collapse = get_nav_collapse(other_list, "sidebarOther", "fe fe-star", "그 외")
    return collapse


def get_render_dict(current_page: str) -> dict:
    render_dict = {}

    study_list = get_study_sub_list(current_page)
    pokemon_list = get_pokemon_sub_list(current_page)
    invest_list = get_invest_sub_list(current_page)
    other_list = get_other_sub_list(current_page)

    nav_list = list()
    nav_list.append(get_nav_item("index", "fe fe-home", "Home", current_page))
    nav_list.append(study_list)
    nav_list.append(pokemon_list)
    nav_list.append(
        get_nav_item("corona", "fa fa-exclamation-triangle", "코로나", current_page)
    )
    nav_list.append(get_nav_item("chatbot", "fa fa-comments", "챗봇", current_page))
    nav_list.append(get_nav_item("link", "fe fe-link", "링크", current_page))
    nav_list.append(invest_list)
    nav_list.append(other_list)

    render_dict["nav_list"] = nav_list
    render_dict["version"] = VERSION
    return render_dict
