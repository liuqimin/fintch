from django.conf.urls import url,include
from nettool import views
from django.contrib.auth import views as auth_views
urlpatterns = [

     url(r'^index', views.index.as_view()),

]