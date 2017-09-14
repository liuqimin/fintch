from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.db import transaction
from django.urls import reverse
from django.views import View
from background import models
from utils.pager import PageInfo
import json
import os
from base.views.base import BaseResponse
import uuid
def index(request):
    return render(request,'backend/index.html')

def base_info(request):

    return render(request,'backend/base_info.html')

class upload_avatar(View):
    def get(self,request,*args,**kwargs):
        print(request.FILES)
    def post(self, request, *args, **kwargs):
        print('post')
        result= BaseResponse()
        file_obj = request.FILES.get('avatar_img')
        if not file_obj:
            return HttpResponse(json.dump(result.__dict__))
        else:
            file_name = str(uuid.uuid4())
            file_path = os.path.join('static/imgs/avatar',file_name)
            f = open(file_path,'wb')
            for chunk in file_obj.chunks():
                f.write(chunk)
            f.close()
            result.status = True
            result.data = file_path
            print(result.__dict__)
            return HttpResponse(json.dumps(result.__dict__))

def tag(request):
    return render(request,'backend/tag.html')

def categroy(request):
    return render(request, 'backend/categroy.html')

def article(request,*args,**kwargs):
    #blog_id = request.session['user_info']['blog_nid']
   # article_type_list = models.Article.type_choices

    result = {}
    type_list = map(lambda item: {'nid': item[0], 'title': item[1]},
                    models.Article.type_choices)  ##map 对象，用list可以获取，可以迭代
    categroy_list = models.Category.objects.all()
   # asset_count = models.Base.objects.filter(conditions).count()

    page_info = PageInfo(request.GET.get('pager', None), asset_count)
    result['type_list'] = type_list
    result['categroy_list'] = categroy_list
    if kwargs:
        print(request.path_info)
        condition ={}
        for k,v in kwargs.items():
            kwargs[k] = int(v)
            if v == '0':
                result[k] = 0
            else:
                condition[k] = int(v)
                result[k] = int(v)
        content_count = models.Article.objects.filter(**condition).count()
        page_info = PageInfo(request.GET.get('pager', None), content_count)
        result['content'] = page_info
        print(result)
        return render(request, 'backend/article.html',result)

    else:

        print(result)
        return render(request,'backend/article.html',result)

