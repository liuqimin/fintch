from django.shortcuts import render,HttpResponse
from django.views import View
from django.contrib.auth import authenticate,login
from base import form
# Create your views here.
class login(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')
    def post(self,request,*args,**kwargs):
        user = request.POST.get('username')
        passwd = request.POST.get('pwd')
        print(user,passwd)
        result = authenticate(username=user,password=passwd)
        if result is not None:
            login(request,result)

            return HttpResponse('ok')
        else:
            return render(request, 'login.html')

class registerview(View):
    def get(self,request,*args,**kwargs):
        return render(request,'user_register.html ')
    def post(self,request,*args,**kwargs):
        print('POST')
        print(request.POST)
        return render(request, 'user_register.html ')

class userlist(View):
    def get(self,request,*args,**kwargs):
        obj = form.BaseForm()
        return  render(request,'userlist.html',{'form':obj})
    def post(self,request,*args,**kwargs):
        pass