from django.shortcuts import render,HttpResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from base import form,models
from django.http import JsonResponse
import json
from base.service import server
# Create your views here.
from django.db import IntegrityError
class ac_login(View):
    def get(self, request, *args, **kwargs):
        #   user = User.objects.create_user('te1stsfafa3','422171714@qq.com','test@42217171')
        #obj = User.objects.filter(username='test1')
        #print(obj)
        #ff=User.objects.get(username='test1').id
      #  print(ff.id)

     #   obj=models.UserProfile(id=1,name='test',user_id=1)
     #   print('test')
    #    obj.save()
        return render(request, 'login.html')
    def post(self,request,*args,**kwargs):
        user = request.POST.get('username')
        passwd = request.POST.get('pwd')
        print(user,passwd)
        result = authenticate(username=user,password=passwd)
        if result is not None:
            print(1)
            login(request,result)

            return HttpResponse('ok')
        else:
            print(2)
            return render(request, 'login.html')

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


class asset(View):
    def get(self,request,*args, **kwargs):
        return render(request, 'asset.html')
    def post(self,request, *args, **kwargs):
        return render(request, 'asset.html')
class assets(View):
    def get(self,request, *args, **kwargs):
        pass
    def post(self,request, *args, **kwargs):
        pass

class BaseResponse(object):
    def __init__(self):
        self.status = True
        self.data = None
        self.message = None
class ServerView(View):
    def get(self,request,*args, **kwargs):
        return render(request,'server.html')

class ServerJsonView(View):
    def get(self, request):
        obj = server.Server()
        print(request)
        response = obj.fetch_services(request)
        print(response.__dict__)
        return JsonResponse(response.__dict__)