from django.shortcuts import render,HttpResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate,login,get_user
from django.contrib.auth.models import User
from base import form,models
from django.http import JsonResponse
from base import models
from base.views.base import BaseResponse
from utils.pager import PageInfo
from io import BytesIO
from utils.check_code import create_validate_code
import json
from base.service import server
# Create your views here.
from django.db import IntegrityError

class ac_login(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')
    def post(self,request,*args,**kwargs):
        data = BaseResponse()
        fuck= get_user(request)
        print(fuck.id,333)
        user = request.POST.get('username')
        passwd = request.POST.get('password')
        check_code = request.POST.get("check_code")
        if request.session.has_key('CheckCode') and request.session.get('CheckCode') ==check_code:
            print('哈哈')
            #
            result = authenticate(username=user, password=passwd)
            if result is not None:
              #  print(1)
                login(request, result)
                user = get_user(request)

                name = models.UserProfile.objects.get(user_id=user.id)

                request.session['login_info_user'] = str(user)
                request.session['login_info_name'] = str(name)
                data.status = True
                return HttpResponse(json.dumps(data.__dict__))
            else:
                data.status = False
                data.message = "用户密码错误"
                print(data.__dict__)
                return HttpResponse(json.dumps(data.__dict__))

        else:
            data.status = False
            data.message = "验证码错误"
            print(data.__dict__)
            return HttpResponse(json.dumps(data.__dict__))


class registerview(View):
    def get(self,request,*args,**kwargs):
        obj = form.CreateUserForm()
        kwargs ={
            'form':obj,
        }
        return render(request,'userlist.html',kwargs)
    def post(self,request,*args,**kwargs):
        print(request.POST)
        obj = form.CreateUserForm(request.POST, request.FILES)
        if obj.is_valid():
            values = obj.clean()
            print(values)
            print('ok')

            u_username = obj.cleaned_data.get('username')
            u_password = obj.cleaned_data.get('password')
            u_name = obj.cleaned_data.get('name')
            u_email = obj.cleaned_data.get('mail')
            print(u_username,u_password,u_email)
            try:
                result = User.objects.create_user(u_username,u_email,u_password)
                result.save()
                print(result.id)
                models.UserProfile.objects.filter(user_id=result.id).update(name=u_name)
            except IntegrityError as e:
                pass



            return HttpResponseRedirect(reverse('password_change_done'))
        else:
            return render(request, 'userlist.html', {'form': obj})

class CheckCcode(View):
    def get(self, request, *args, **kwargs):

        stream = BytesIO()
        img,code = create_validate_code()
        img.save(stream, 'PNG')
        print(img,code)
        request.session['CheckCode'] = code
        return HttpResponse(stream.getvalue())

    def post(self, request, *args, **kwargs):
        pass