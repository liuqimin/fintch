from django.shortcuts import render,HttpResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth.models import User
from base import form,models
from django.http import JsonResponse
import json
from base.service import server
# Create your views here.
from django.db import IntegrityError


class BaseResponse(object):
    def __init__(self):
        self.status = True
        self.data = None
        self.message = None