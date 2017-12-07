from django.conf.urls import url, include

from .views import *

urlpatterns = [
    url(r'^(?P<id>[0-9]+)/summary/data/' , SummaryData.as_view() , name = "api.simulation.summary.data"),
    url(r'^(?P<id>[0-9]+)/summary/keys/$' , SummaryKeys.as_view() , name = "api.simulation.summary.keys"),
    url(r'^(?P<id>[0-9]+)/parameters/$' , Parameters.as_view() , name = "api.simulation.parameters"),
    url(r'^upload/$' , Upload.as_view() , name = "api.simulation.upload")
]
