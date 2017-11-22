from django.conf.urls import url, include

from .views import *

urlpatterns = [
    url(r'^get_or_create/$' , GetOrCreate.as_view() , name = "api.ensemble.get_or_create"),
    url(r'^add_realisation/(?P<ens_id>[\d\w]+)/$', AddRealisation.as_view(), name = "api.ensemble.add_realisation"),
    url(r'^add_simulation/(?P<ens_id>[\d\w]+)/$', AddSimulation.as_view(), name = "api.ensemble.add_simulation")
]
