"""PerfectCRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from base.views import logininfo,server,projapp,asset

from django.contrib.auth import views as auth_views
urlpatterns = [

     url(r'^login', logininfo.ac_login.as_view()),
     url(r'^registeruser', logininfo.registerview.as_view()),

   # url('^', include('django.contrib.auth.urls')),
    url(r'^password_change/$', auth_views.PasswordChangeView.as_view(), name='password_change'),
    url(r'^password_change/done/$', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #url(r'asset',views.asset.as_view(),name='asset_list'),
    #url(r'assets',views.assets.as_view()),
    url(r'^server.html', server.ServerView.as_view()),
    url(r'^server-json.html', server.ServerJsonView.as_view()),
    url(r'^proj_app.html', projapp.ProjAppView.as_view()),
    url(r'^proj_app-json.html', projapp.ProjAppJsonView.as_view()),
    url(r'^check_code.html', logininfo.CheckCcode.as_view()),
   # url(r'^add-server.html', views.ServerAddView.as_view(),name='add_server'),
]

