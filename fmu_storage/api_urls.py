from django.conf.urls import url,include

import simulation.api.urls
import ensemble.api.urls


urlpatterns = [
    url(r"^simulation/", include(simulation.api.urls)),
    url(r"^ensemble/", include(ensemble.api.urls))
]
