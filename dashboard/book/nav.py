def get_nav_collapse(child_list, button_url, icon, description):
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


def get_nav_item(template, icon, description, current_page):
    return {
        "collapse": False,
        "template": "book:{}".format(template),
        "icon": icon,
        "description": description,
        "active": "active" if template == current_page else "",
    }


def get_render_dict(current_page):
    render_dict = {}

    study_list = list()
    study_list.append(get_nav_item("slide", "fa fa-file-powerpoint", "슬라이드", current_page))
    study_list.append(get_nav_item("paper", "fa fa-file-pdf", "논문", current_page))
    study_list.append(get_nav_item("colab", "fa fa-file-code", "실습자료", current_page))

    pokemon_list = list()
    pokemon_list.append(get_nav_item("pokemon_classification", "fa fa-check-square", "분류하기", current_page))
    pokemon_list.append(get_nav_item("pokemon_result", "fa fa-poll", "분류결과", current_page))

    invest_list = list()
    invest_list.append(get_nav_item("leading_stocks", "fa fa-money-check-alt", "Leading Stocks", current_page))
    invest_list.append(get_nav_item("live_currency", "fa fa-exchange-alt", "Currency History", current_page))
    invest_list.append(get_nav_item("krx_price_query", "fa fa-search-dollar", "Price Query", current_page))
    invest_list.append(get_nav_item("lotto", "fa fa-money-bill-wave", "Lottery", current_page))
    invest_list.append(get_nav_item("real_estate", "fa fa-building", "부동산", current_page))
    invest_list.append(get_nav_item("recommend_book", "fa fa-book", "책", current_page))

    classifier_list = list()
    classifier_list.append(get_nav_item("people", "fa fa-users", "인명사전", current_page))
    classifier_list.append(get_nav_item("people_result", "fa fa-user-friends", "인명", current_page))
    classifier_list.append(get_nav_item("people_high_expectation", "fa fa-user-check", "예상", current_page))

    other_list = list()
    other_list.append(get_nav_item("food", "fa fa-utensils", "맛집", current_page))
    other_list.append(get_nav_item("wine", "fa fa-wine-bottle", "Wine", current_page))
    other_list.append(get_nav_item("law_search", "fa fa-gavel", "법률 검색", current_page))
    other_list.append(get_nav_item("todo", "fa fa-check", "Todo List", current_page))
    other_list.append(get_nav_item("algorithm", "fe fe-video", "비디오", current_page))
    other_list.append(get_nav_collapse(classifier_list, "sidebarClassifier", "fa fa-tags", "분류기"))
    other_list.append(get_nav_item("idea", "fe fe-zap", "아이디어 모음", current_page))

    nav_list = list()
    nav_list.append(get_nav_item("index", "fe fe-home", "Home", current_page))
    nav_list.append(get_nav_collapse(study_list, "sidebarLecture", "fa fa-chalkboard-teacher", "스터디 정리"))
    nav_list.append(get_nav_collapse(pokemon_list, "sidebarPokemon", "fa fa-gamepad", "포켓몬"))
    nav_list.append(get_nav_item("corona", "fa fa-exclamation-triangle", "코로나", current_page))
    nav_list.append(get_nav_item("chatbot", "fa fa-comments", "챗봇", current_page))
    nav_list.append(get_nav_item("link", "fe fe-link", "링크", current_page))
    nav_list.append(get_nav_collapse(invest_list, "sidebarInvest", "fe fe-dollar-sign", "투자"))
    nav_list.append(get_nav_collapse(other_list, "sidebarOther", "fe fe-star", "그 외"))

    render_dict['nav_list'] = nav_list
    return render_dict
