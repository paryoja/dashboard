import re

from django import template

register = template.Library()

user_pattern = re.compile("@([A-Za-z0-9._]+)")


@register.filter(name="highlight_user")
def highlight_user(value):
    """Removes all values of arg from the given string"""
    user_highlight = user_pattern.sub(r"https://www.instagram.com/\1", value)

    return user_highlight


@register.filter(name="get_split")
def get_split(value, index):
    try:
        return value.split("/")[index]
    except IndexError:
        return None
