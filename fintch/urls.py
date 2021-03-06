"""fintch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from base.views import logininfo
from django.contrib.auth import views as auth_views
from base import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^base/',include('base.urls')),
    url(r'^backend/',include('background.urls')),
    url(r'^net/',include('nettool.urls')),
    url(r'^asset/',include('helpdesk.urls')),
    url(r'^logout', logininfo.logout,name='logout'),
]
