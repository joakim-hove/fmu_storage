from django.conf.urls import url,include

import simulation.api.urls
import ensemble.api.urls
from api.views import *

urlpatterns = [
    url(r"^simulation/", include(simulation.api.urls)),
    url(r"^ensemble/", include(ensemble.api.urls)),
    url(r"^urls/", ApiUrls.as_view(), name = "api.urls")
]
