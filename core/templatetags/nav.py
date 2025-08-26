from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()

@register.simple_tag(takes_context=True)
def active_url(context, url_name):
  request = context.get('request')
  try:
    url = reverse(url_name)
  except NoReverseMatch:
    return ''
  if request.path == url:
    return 'active'
  return ''
