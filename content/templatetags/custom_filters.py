from django import template
from django.utils.html import urlize
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def urlize_newtab(value):
    # Use Django's urlize function to convert URLs into links
    value = urlize(value)
    # Add target="_blank" to each anchor tag
    value = re.sub(r'<a ', r'<a target="_blank" ', value)
    return mark_safe(value)
