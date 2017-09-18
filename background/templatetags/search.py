from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag
def category_all(article_type_id,category_id,p=1):
    '''
    :param arg_dict:get上传的数据
    :return: ###<a href="/backend/article-0-{{ category_id }}.html"> 全部 </a>
    '''
   # article_type_id = arg_dict['article_type_id']
   # category_nid = arg_dict['category_id']
   # p = arg_dict['p']  ##当前页
    url = reverse('article', kwargs={'article_type_id': 0, 'category_id':category_id })
    print(url)
    if article_type_id == 0:
    #    temp = '<a class="active" href="{}?p={}">全部</a>' .format(url,p)
        result = '<a class="active" href="{}?p={}">全部</a>'.format(url,p,)
    else:
        result = '<a href="{}?p={}">全部</a>'.format(url,p,)
    return mark_safe(result)

@register.simple_tag
def category_type_list(article_type_id,category_id,type_list,p=1):
    '''

    :param article_type_id:
    :param category_id:
    :param type_list:
    :param p:
    :return:  <a> 标签
    '''
    result = []
    for obj in type_list:
        url = reverse('article',kwargs={'article_type_id':obj['nid'],"category_id":category_id})
        if obj['nid'] == int(article_type_id):
            temp = '<a class ="active" href="{}?p={}">{}</a>'.format(url,p,obj['title'])
        else:
            temp = '<a href="{}?p={}">{}</a>'.format(url, p, obj['title'])
        result.append(temp)
    return mark_safe(''.join(result))
@register.simple_tag
def article_all(article_type_id,category_id,p=1):
    '''
    :param article_type_id:
    :param category_id:
    :param p:
    :return:
    '''
    url = reverse('article', kwargs={'article_type_id': article_type_id, 'category_id':0 })
    if not p:
        p = 1
    if category_id == 0:
    #    temp = '<a class="active" href="{}?p={}">全部</a>' .format(url,p)
        result = '<a class="active" href="{}?p={}">全部</a>'.format(url,p,)
    else:
        result = '<a href="{}?p={}">全部</a>'.format(url,p,)
    return mark_safe(result)

@register.simple_tag
def article_type_list(article_type_id,category_id,categroy_list,p=1):
    '''

    :param article_type_id:
    :param category_id:
    :param categroy_list:
    :param p:
    :return:
    '''
    result = []
    print(categroy_list)
    for obj in categroy_list:
        url = reverse('article', kwargs={'article_type_id': article_type_id, "category_id": obj.nid})
        if obj.nid == int(category_id):
            temp = '<a class ="active" href="{}?p{}">{}</a>'.format(url, p, obj.title)
        else:
            temp = '<a href="{}?p={}">{}</a>'.format(url, p, obj.title)
        result.append(temp)
    print(result)
    return mark_safe(''.join(result))