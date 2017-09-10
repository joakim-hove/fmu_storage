from django.conf.urls import url, include

from .views import *

urlpatterns = [
    url(r'^summary/data/(?P<id>[0-9]+)/$' , SummaryData.as_view() , name = "api.simulation.summary.data"),
    url(r'^parameters/data/(?P<id>[0-9]+)/$' , Parameters.as_view() , name = "api.simulation.parameters"),
    url(r'^upload/$' , Upload.as_view() , name = "api.simulation.upload")
]
