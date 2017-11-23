from django.conf.urls import url, include
from .views import *


urlpatterns = [
    url(r'^view/$' , EnsembleList.as_view() , name = "ensemble.list_view"),
    url(r'^view/(?P<id>\d+)/$' , EnsembleDetail.as_view() , name = "ensemble.detail_view")
]

