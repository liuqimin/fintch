from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.db import transaction
from django.urls import reverse
from django.views import View
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
    return render(request,'backend/article.html')
