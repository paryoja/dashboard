"""템플릿에서 필요한 함수."""
import re

from django import template

register = template.Library()

user_pattern = re.compile("@([A-Za-z0-9._]+)")


@register.filter(name="highlight_user")
def highlight_user(value):
    """Remove all values of arg from the given string."""
    user_highlight = user_pattern.sub(r"https://www.instagram.com/\1", value)

    return user_highlight


@register.filter(name="get_split")
def get_split(value, index):
    """슬래시로 나눈 sub-string 가져옴."""
    try:
        return value.split("/")[index]
    except IndexError:
        return None


@register.filter(name="get_value")
def get_value(collection, key):
    """Dictionary에서 value 값을 꺼내온다."""
    try:
        return collection[key]
    except KeyError:
        return None
