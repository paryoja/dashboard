"""EPL 데이터 파싱."""
import typing

import requests
from bs4 import BeautifulSoup


def parse_lineup_html(soup):
    """라인업 HTML 가져오기."""
    line_up_html = soup.select_one("section.squads.mcMainTab")
    line_up_html["class"] = line_up_html.get("class", []) + ["active"]
    center = line_up_html.select_one("div.mcLineUpContainter.matchCentrePitchContainer")
    center.attrs["style"] = None

    for player in line_up_html.select("li.player"):
        player.select_one("img").extract()
        sub = player.select_one("div.name").select_one("span.sub")
        if sub:
            sub.extract()

    for line_ups in line_up_html.select("div.mcLineUpContainter"):
        header = line_ups.select_one("h3.substituteHeader")
        if header:
            header.extract()
        first = True
        for substitute in line_ups.select("ul.startingLineUpContainer"):
            if first:
                first = False
            else:
                substitute.extract()

    for link in line_up_html.select("a"):
        link["style"] = "pointer-events: none;"

    line_up_html = (
        line_up_html.prettify()
        .replace('src="//', 'src="https://')
        .replace('src="/', 'src="https://www.premierleague.com/')
    )
    return line_up_html


def parse_lineup(soup):
    """라인업 파싱."""
    data = soup.select("div.mcLineUpContainter")

    squad = {}

    for each in data:
        # 각 사이드
        team = each["data-ui-tab"]
        if team == "Pitch":
            # 중간에 Pitch 부분이 들어 있어서 스킵
            continue

        lineup = []
        starting = True
        for _ in each.select("ul.startingLineUpContainer"):
            # 선발과 출전 같은 class에 있으나 선발은 첫번째에 있다
            for player in each.select("li.player"):
                # name / 교체정보
                div_name = player.select_one("div.name")
                name = div_name.find(text=True, recursive=False).strip()

                position = (
                    player.select_one("span.position").select_one("span").text.strip()
                )
                # print(player)

                if not starting:
                    div_sub = div_name.select_one("span.icn.sub-on")
                    if div_sub:
                        participate = True
                    else:
                        participate = False
                else:
                    participate = True
                player_data = {
                    "position": position,
                    "name": name,
                    "starting": starting,
                    "participate": participate,
                }

                lineup.append(player_data)
            starting = False
        squad[team] = lineup
    return squad


def get_lineup(_match_id: int) -> typing.Tuple[dict, str]:
    """라인업 가져오기."""
    html = requests.get("https://www.premierleague.com/match/46922").text
    soup = BeautifulSoup(html, "html.parser")

    lineup = parse_lineup(soup)
    lineup_html = parse_lineup_html(soup)

    return lineup, lineup_html
