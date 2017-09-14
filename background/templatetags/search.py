from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag
def category_all(article_type_id,category_id):
    '''
    :param arg_dict:get上传的数据
    :return: ###<a href="/backend/article-0-{{ category_id }}.html"> 全部 </a>
    '''
   # article_type_id = arg_dict['article_type_id']
   # category_nid = arg_dict['category_id']
   # p = arg_dict['p']  ##当前页
    url = reverse('article', kwargs={'article_type_id': 0, 'category_id':category_id })
    if article_type_id == 0:
    #    temp = '<a class="active" href="{}?p={}">全部</a>' .format(url,p)
        temp = '<a class="active" href="{}">全部</a>'.format(url)
    else:
        temp = '<a href="%s">全部</a>' % (url,)
    print(temp)
    return mark_safe(temp)

