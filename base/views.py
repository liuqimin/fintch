from django.shortcuts import render,HttpResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from base import form,models
import json
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
    def get(self,request,*args, **kwargs):
        response = BaseResponse()
        try:
            # 获取要显示的列
            # 获取数据
            table_config = [
                {
                    'q': 'id',
                    'title': '主机名',
                    'display':0,
                    'text': {},
                    'attr': {}
                },
                {
                    'q': 'hostname',
                    'title': '主机名',
                    'display':1,
                    'text': {'content': '{m}','kwargs': {'m':'@hostname'}},
                    'attr': {'orginal':'@hostname','k2':'v2'}
                },
                # '{n}-{m}'.format({'n': 'hostname','m':'@hostname'}) => hostname-c1.com
                {
                    'q': 'ext_ip',
                    'title': '外部IP',
                    'display':1,
                    'text': {'content': '{m}','kwargs': {'m':'@port'}},
                    'attr': {'k1':'@port','k2':'v2'}
                },
                {
                    'q': 'int_ip',
                    'title': '内部ip',
                    'display':1,
                    # 去全局变量business_unit_list = [
                    #      {id:1,name:'WEB'},
                    #      {id:2,name:'存储'},
                    #      {id:3,name:'商城'},
                    # ]
                    'text': {'content': '{m}','kwargs': {'m':'@@business_unit_list'}},
                    'attr': {'k1':'@business_unit_id','k2':'v2'}
                },
            ]

            values_list = []
            for item in table_config:
                if item['q']:
                    values_list.append(item['q'])

            data_list = models.Base.objects.values(*values_list)
            # [{},{}]
            data_list = list(data_list)
            print(data_list)
            response.data = {
                'table_config': table_config,
                'data_list': data_list,
            }
        except Exception as e:
            response.status = False
            response.message = str(e)
        return HttpResponse(json.dumps(response.__dict__))