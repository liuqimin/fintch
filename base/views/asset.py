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