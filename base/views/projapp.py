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



class ProjAppView(View):
    def get(self,request,*args, **kwargs):
        print('server')
        return render(request,'proj_app.html')

class ProjAppJsonView(View):
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