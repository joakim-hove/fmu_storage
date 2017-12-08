from django.conf.urls import url, include

from .views import *

urlpatterns = [
    url(r'^get_or_create/$' , GetOrCreate.as_view() , name = "api.ensemble.get_or_create"),
    url(r'^(?P<ens_id>[\d\w]+)/add_realisation/$', AddRealisation.as_view(), name = "api.ensemble.add_realisation"),
    url(r'^(?P<ens_id>[\d\w]+)/add_simulation/$', AddSimulation.as_view(), name = "api.ensemble.add_simulation"),
    url(r'^(?P<ens_id>[\d\w]+)/realisations/$', Realisations.as_view(), name = "api.ensemble.realisations"),
    url(r'^(?P<ens_id>[\d\w]+)/simulations.summary.data', SummaryData.as_view(), name = "api.ensemble.simulations.summary.data"),
    url(r'^(?P<ens_id>[\d\w]+)/info/$' , EnsembleInfo.as_view(), name = "api.ensemble.info")
]
