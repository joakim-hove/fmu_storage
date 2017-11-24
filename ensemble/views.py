# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .models import *


class EnsembleList(View):

    def get(self, request):
        return render( request, "ensemble/list.html" , {"ensemble_list" : Ensemble.objects.all()}) 


class EnsembleDetail(View):

    def get(self, request, id):
        try:
            ensemble = Ensemble.objects.get(pk=int(id))
            return render(request, "ensemble/view.html", {"ensemble" : ensemble})
        except Ensemble.DoesNotExist:
            return HttpResponse("No such ensemble: %s" % id, status=404)


class RealisationDetail(View):

    def get(self, request, id):
        try:
            realisation = Realisation.objects.get(pk=int(id))
            return render(request, "ensemble/realisation_view.html", {"realisation" : realisation})
        except Realisation.DoesNotExist:
            return HttpResponse("No such realisation: %s" % id, status=404)
