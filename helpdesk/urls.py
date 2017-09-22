from django.conf.urls import url,include
from helpdesk.views import details

from django.contrib.auth import views as auth_views
urlpatterns = [
    url(r'^list.html',details.DetailsView.as_view(),name='helpdesk_details' ),
    url(r'^add_list.html',details.AddAssetView.as_view(),name='helpdesk_add_asset' ),
    url(r'^list-json.html',details.DetailsJsonView.as_view(),name='helpdesk_details_json' ),
#     url(r'^index', index.ac_login.as_view()),

]