from django import template
from core.auth import in_group

register = template.Library()


@register.filter(name="in_group")
def in_group_filter(user, name):
    return in_group(user, name)
