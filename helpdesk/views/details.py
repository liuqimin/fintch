from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.db import transaction
from django.urls import reverse
from helpdesk.form import Asset_form
from django.views import View
from utils.pager import PageInfo
import json
import os
from helpdesk.service import details
from base.views.base import BaseResponse
from helpdesk import models
class DetailsView(View):
    def get(self,request,*args,**kwargs):

        return render(request, 'helpdesk/detail.html')

    def post(self,request,*args,**kwargs):
        pass

class DetailsJsonView(View):
    def get(self,request,*args,**kwargs):
        obj = details.Asset()
        response = obj.fetch_asset(request)

        return JsonResponse(response.__dict__)
    def post(self,request,*args,**kwargs):
        pass
    def delete(self, request):
        print('111')
        obj = details.Asset()
        response = obj.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        obj = details.Asset()
        response = obj.put_assets(request)
        return JsonResponse(response.__dict__)

class AddAssetView(View):
    def get(self,request,*args,**kwargs):
       # bb=Asset_form()
        kwargs = {
            'form': Asset_form(),
        }
        return render(request, 'helpdesk/add_detail.html',kwargs)
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