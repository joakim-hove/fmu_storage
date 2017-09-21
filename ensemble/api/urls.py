from django.conf.urls import url, include

from .views import *

urlpatterns = [
    url(r'^create/$' , Create.as_view() , name = "api.ensemble.create")
]
