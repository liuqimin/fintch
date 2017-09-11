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



class ServerView(View):
    def get(self,request,*args, **kwargs):
        print('server')
        return render(request,'server.html')

class ServerJsonView(View):
    def get(self, request):
        obj = server.Server()
        print(request)
        response = obj.fetch_services(request)
        print(response.__dict__)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        print('111')
        response = server.Server.delete_assets(request)
        print('now')
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = server.Server.put_assets(request)
        return JsonResponse(response.__dict__)

class ServerAddView(View):

    def get(self,request,*args,**kwargs):
        obj = form.CreateServerForm()
        kwargs = {
            'form': obj,
        }

        result = map(lambda x: (x[0],x[1]), models.Base.status_choices)
        return render(request,'add_server.html',kwargs)

    def post(self,request):
        #print(request.POST)
        obj = form.CreateServerForm(request.POST, request.FILES)
        kwargs = {
            'form':obj,
        }
        print(obj)
        print('cao')
        if obj.is_valid():
            values = obj.clean()
            print(values)
            print('ok')
            u_dict = {
                'hostname':obj.cleaned_data.get('username'),
                'ext_ip':obj.cleaned_data.get('ext_ip'),
                'int_ip':obj.cleaned_data.get('int_ip'),
                'status':obj.cleaned_data.get('status')
            }
            try:
                result = models.Base.objects.create(**u_dict)
                ret = {'result': 'add success'}
                return JsonResponse(ret)
            except Exception as e:
                ret = {'result': e}
                print(e)
                return JsonResponse(ret)
        else:
            print(obj.errors)
           # print('shibai')
            ret = {'result': obj.errors}
            return JsonResponse(ret)
