from django.conf.urls import url,include

import simulation.api.urls

urlpatterns = [
    url(r"^simulation/", include(simulation.api.urls))
]
