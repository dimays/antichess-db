from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def intcomma(value):
    """Formats an integer with commas as separators."""
    try:
        value = int(value)
    except ValueError:
        return value

    orig = str(value)
    new = ""
    while orig != "":
        new = "," + orig[-3:] + new
        orig = orig[:-3]
    return new[1:]

@register.filter
@stringfilter
def lower(value):
    """Returns a lowercase value"""

    return value.lower()