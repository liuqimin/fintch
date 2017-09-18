from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
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
class DetailsView(View):
    def get(self,request,*args,**kwargs):

        return render(request, 'helpdesk/detail.html')
    def post(self,request,*args,**kwargs):
        pass

class DetailsJsonView(View):
    def get(self,request,*args,**kwargs):
        return JsonResponse(response.__dict__)
    def post(self,request,*args,**kwargs):
        pass



'''
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
'''