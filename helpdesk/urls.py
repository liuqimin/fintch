from django.conf.urls import url,include
from helpdesk.views import details

from django.contrib.auth import views as auth_views
urlpatterns = [
    url(r'^list',details.DetailsView.as_view() ),
    url(r'^list-json.html',details.DetailsJsonView.as_view() ),
#     url(r'^index', index.ac_login.as_view()),

]