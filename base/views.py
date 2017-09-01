from django.shortcuts import render,HttpResponse
from django.views import View
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from base import form
# Create your views here.
class login(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.create_user('test333','422171714@qq.com','test@42217171')
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

            username = obj.cleaned_data.get('username')
            password = obj.cleaned_data.get('password')
            name = obj.cleaned_data.get('name')

            mode

        return render(request, 'userlist.html', {'form': obj})





