from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from base.views import base
from helpdesk.form import Asset_form
from django.views import View
from helpdesk import form
from helpdesk.service import details
from base.auth.auth import check_login
from helpdesk import models
from django.utils.decorators import method_decorator
from crequest.middleware import CrequestMiddleware
class DetailsView(View):

    def dispatch(self, request, *args, **kwargs):
        return super(DetailsView, self).dispatch(request, *args, **kwargs)

    @method_decorator(check_login)
    def get(self,request,*args,**kwargs):
        current_request = CrequestMiddleware.get_request()
        bb= CrequestMiddleware.set_request(request)
        print(current_request,333,bb)
        return render(request, 'helpdesk/detail.html')

    def post(self,request,*args,**kwargs):
        pass


class DetailsJsonView(View):
    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super(DetailsJsonView, self).dispatch(request, *args, **kwargs)


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
    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super(AddAssetView, self).dispatch(request, *args, **kwargs)

    def get(self,request,*args,**kwargs):
       # bb=Asset_form()
        kwargs = {
            'form': Asset_form(),
        }

       # return render(request, 'helpdesk/add_detail.html',locals())
        return render(request, 'helpdesk/add_detail.html',kwargs)
    def post(self,request,*args,**kwargs):
        asset_form = form.Asset_form(request.POST)
        print(request.POST)
        result = base.BaseResponse()
        if asset_form.is_valid():
          #  print(**asset_form.changed_data)
            asset_form.save()
            result.status = True
            result.message = "增加成功"
        else:
            result.status = False
            result.message = str(asset_form.jsonlist)
        return JsonResponse(result.__dict__)

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