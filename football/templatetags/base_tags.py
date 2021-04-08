from django import template
from ..models import Category

register = template.Library()

@register.simple_tag
def title():
    return 'وبلاگ فوتبالی جواد'

@register.inclusion_tag('football/category_navbar.html')
def category_navbar(active):
    return {
        'active': active,
        'categories': Category.objects.all()
    }

@register.inclusion_tag('football/top_navbar.html')
def top_navbar(user):
    return {
        'user': user,
    }

@register.inclusion_tag('football/article_card.html')
def article_card(article):
    return {
        'article': article,
    }

@register.inclusion_tag('football/article_pagination.html')
def article_pagination(page_obj):
    return {
        'articles': page_obj,
    }