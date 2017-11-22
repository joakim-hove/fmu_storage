# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views import View
from django.http import HttpResponse

from ensemble.models import *
from simulation.api.views import Upload as Simulation

class GetOrCreate(View):

    def post(self, request):
        ext_id = request.POST.get("ext_id")
        try:
            ensemble = Ensemble.objects.get( ext_id = ext_id )
            return HttpResponse( ensemble.id )
        except Ensemble.DoesNotExist:
            pass


        try:
            name = request.POST.get("name")
            iteration = int(request.POST.get("iteration"))
            ensemble = Ensemble.objects.create( name = name,
                                                iteration = iteration ,
                                                ext_id = ext_id )
            return HttpResponse( ensemble.id )
        except Exception as exc:
            return HttpResponse( str(exc), status = 400 )


class AddRealisation(View):

    def post(self, request, ens_id):
        try:
            ens = Ensemble.objects.get( ext_id = ens_id )
        except:
            return HttpResponse( "No such ensemble:%s" % ens_id, status = 404)

        try:
            sim_id = int(request.POST["sim_id"])
            iens = int(request.POST["iens"])
            simulation = Simulation.objects.get( pk = sim_id )
        except KeyError,Simulation.DoesNotExist:
            return HttpResponse( "No such simulation ???", status = 404)

        realisation = Realisation.objects.create( iens = iens,
                                                  simulation = sim,
                                                  ensemble = ens )

        return HttpResponse( realisation.id, status = 200)


class AddSimulation(View):

    def post(self, request, ens_id):
        try:
            ens = Ensemble.objects.get( ext_id = ens_id )
        except:
            return HttpResponse( "No such ensemble:%s" % ens_id, status = 404)

        if not "iens" in request.POST:
            return HttpResponse("Missing iens value in POST payload", status = 400)

        if not "group" in request.POST:
            return HttpResponse( "Missing group attribute", status = 403 )


        iens = int(request.POST["iens"])
        group = request.POST["group"]
        try:
            sim = Simulation.upload(request, group)
        except (ValueError,IOError) as error:
            return HttpResponse( str(error), status = 400 )

        realisation = Realisation.objects.create( iens = iens,
                                                  simulation = sim,
                                                  ensemble = ens )

        return HttpResponse( realisation.id, status = 200)

