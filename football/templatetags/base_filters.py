from django import template
from extensions.utils import numbers_to_persian, date_to_jalali_str
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def to_persian(mystr):
    return numbers_to_persian(mystr)

@register.filter
@stringfilter
def underscored(mystr):
    return mystr.replace(' ', '_')

@register.filter
def date_to_jalali(mystr):
    return date_to_jalali_str(mystr)