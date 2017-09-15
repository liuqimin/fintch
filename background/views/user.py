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

class article(View):
    def get(self,request,*args,**kwargs):
        # blog_id = request.session['user_info']['blog_nid']
        # article_type_list = models.Article.type_choices

        result = {}
        type_list = map(lambda item: {'nid': item[0], 'title': item[1]},
                        models.Article.type_choices)  ##map 对象，用list可以获取，可以迭代
        categroy_list = models.Category.objects.all()
        result['type_list'] = type_list
        result['categroy_list'] = categroy_list
        if kwargs:
            print(request.path_info)
            condition = {}
            for k, v in kwargs.items():
                kwargs[k] = int(v)
                if v == '0':
                    result[k] = 0
                else:
                    condition[k] = int(v)
                    result[k] = int(v)
            content_count = models.Article.objects.filter(**condition).count()
            page_info = PageInfo(request.GET.get('p', None), content_count)
            result['page_info'] = {
                "page_str": page_info.pager(),
                #  "page_start":page_info.start,
                "p": request.GET.get('p', 1),
                "content_count": content_count,
            }
            print(result['page_info'],333)
            blog_content_list = models.Article.objects.filter(**condition).values('nid', 'title', 'summary')[
                                page_info.start:page_info.end]
            result['content'] = blog_content_list
            #  print(page_info)
            # result['content'] = page_info
            #   print(result)
            # exit(1)
            return render(request, 'backend/article.html', result)

        else:

            print(result)
            return render(request, 'backend/article.html', result)

    def post(self,request,*args,**kwargs):
        pass
