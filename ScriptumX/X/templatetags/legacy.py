"""Legacy template filters removed from modern Django."""
import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='removetags', is_safe=True)
def removetags(value, tags):
    """
    Remove the given HTML tags from the string (Django 1.x compatible).
    Usage: {{ value|removetags:"a span" }}
    """
    if value is None:
        return ''
    text = str(value)
    for tag in str(tags).split():
        tag = tag.strip()
        if not tag:
            continue
        text = re.sub(r'</?%s(\s[^>]*)?>' % re.escape(tag), '', text, flags=re.I)
    return mark_safe(text)
