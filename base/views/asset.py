from django.shortcuts import render

from django.views import View



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