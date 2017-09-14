from django.shortcuts import render
from django.shortcuts import render,HttpResponse
# Create your views here.
from utils import sshBase
from django.views import View

class index(View):
    def get(self,request,*args,**kwargs):
        b = sshBase.test()

        return HttpResponse('fuck')
    def post(self,request,*args,**kwargs):
        pass