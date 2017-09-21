# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views import View
from django.http import HttpResponse

from ensemble.models import *

class Create(View):

    def post(self, request):
        try:
            name = request.POST.get("name")
            iteration = int(request.POST.get("iteration"))
            ensemble = Ensemble.objects.create( name = name,
                                                iteration = iteration )

            return HttpResponse( str(ensemble.id) )
        except:
            return HttpResponse( str(error), status = 400 )
