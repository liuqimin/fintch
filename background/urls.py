from django.conf.urls import url
from django.conf.urls import include
from .views import user

urlpatterns = [
    url(r'^index.html',user.index),
    url(r'^base_info.html',user.base_info),
    url(r'^tag.html',user.tag),
    url(r'^upload-avatar.html',user.upload_avatar.as_view()),
    url(r'^category.html', user.categroy),
    #url(r'^article.html', user.article.as_view(), name='articleindex'),
    url(r'^article-(?P<article_type_id>\d+)-(?P<category_id>\d+).html$', user.article.as_view(), name='article'),
    #url(r'^article-(?P<article_type_id>\d+)-(?P<category_id>\d+).html$', user.article, name='article'),
]
