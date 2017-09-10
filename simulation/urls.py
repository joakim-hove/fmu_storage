from django.conf.urls import url, include
from .views import *


urlpatterns = [
    url(r'^view/(?P<id>[0-9]+)/$' , ViewSimulation.as_view() , name = "simulation.view.detail"),
    url(r'^upload/', UploadSimulation.as_view() , name = "simulation.upload.view"),
    url(r'^summary/view/(?P<id>[0-9]+)/$' , ViewSummary.as_view() , name = "simulation.summary.view.detail"),
    url(r'^data/view/(?P<id>[0-9]+)/$' , ViewDataFile.as_view() , name = "simulation.data_file.view.detail"),
    url(r'^init/view/(?P<id>[0-9]+)/$' , ViewInit.as_view() , name = "simulation.init.view.detail"),
    url(r'^restart/view/(?P<id>[0-9]+)/$' , ViewRestart.as_view() , name = "simulation.restart.view.detail"),
    url(r'^grid/view/(?P<id>[0-9]+)/$' , ViewGrid.as_view() , name = "simulation.grid.view.detail"),
    #
    url(r'^data/download/(?P<id>[0-9]+)/$' , DataFileDownload.as_view() , name = "simulation.data_file.download"),
    url(r'^grid/download/(?P<id>[0-9]+)/$' , GridDownload.as_view() , name = "simulation.grid.download"),
    url(r'^init/download/(?P<id>[0-9]+)/$' , InitDownload.as_view() , name = "simulation.init.download"),
    url(r'^restart/download/(?P<id>[0-9]+)/$' , RestartDownload.as_view() , name = "simulation.restart.download"),
]
