from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def category_all(arg_dict):
    article_type_id = arg_dict['article_type_id']
    category_nid = arg_dict['category_id']
    p = arg_dict['']
