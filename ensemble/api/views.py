# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views import View
from django.http import HttpResponse, JsonResponse

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
            user = request.POST.get("user")
            ensemble = Ensemble.objects.create( name = name,
                                                iteration = iteration ,
                                                user = user,
                                                ext_id = ext_id )
            return HttpResponse( ensemble.id )
        except Exception as exc:
            return HttpResponse( str(exc), status = 400 )


class AddRealisation(View):

    def post(self, request, ens_id):
        try:
            ens = Ensemble.objects.get( id = ens_id )
        except:
            return HttpResponse( "No such ensemble:%s" % ens_id, status = 404)

        try:
            sim_id = int(request.POST["sim_id"])
            iens = int(request.POST["iens"])
            simulation = Simulation.objects.get( pk = sim_id )
        except KeyError,Simulation.DoesNotExist:
            return HttpResponse( "No such simulation ???", status = 404)

        realisation = Realisation.update_or_create(ens, iens, sim)

        return HttpResponse( realisation.id, status = 200)


class AddSimulation(View):

    def post(self, request, ens_id):
        try:
            ens = Ensemble.objects.get( id = ens_id )
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

        if "parameters" in request.POST:
            Parameter.loads( sim, request.POST["parameters"])

        realisation = Realisation.update_or_create(ens, iens, sim)
        return HttpResponse( realisation.id, status = 200)


class Realisations(View):

    def get(self, request, ens_id):
        try:
            ens = Ensemble.objects.get(id = ens_id)
        except Ensemble.DoesNotExist:
            return HttpResponse("No such ensemble:{}".format(ens_id), status = 404)

        realisations = {}
        for real in Realisation.objects.filter( ensemble = ens ):
            realisations[real.id] = real.simulation.id

        return JsonResponse(realisations)


class EnsembleInfo(View):

    def get(self, request, ens_id):
        try:
            ens = Ensemble.objects.get(id = ens_id)
        except Ensemble.DoesNotExist:
            return HttpResponse("No such ensemble:{}".format(ens_id), status = 404)

        result = {"name"    : ens.name,
                  "id"      : ens.id,
                  "run_id"  : ens.ext_id,
                  "user"    : ens.user,
                  "created" : ens.creation_time}

        realisations = {}
        for real in ens.realisations(): 
            simulation = real.simulation
            summary_id = simulation.summary.id

            realisations[real.iens] = {"simulation" : {"id" : simulation.id,  "summary" : summary_id }}

        result["realisations"] = realisations
        return JsonResponse(result)


class SummaryData(View):
    time_interval = "3M"


    def get(self, request, ens_id):
        try:
            ens = Ensemble.objects.get(id = ens_id)
        except Ensemble.DoesNotExist:
            return HttpResponse("No such ensemble:{}".format(ens_id), status = 404)

        time_interval = request.GET.get("time_interval", SummaryData.time_interval)

        results = {}
        for real in ens.realisations():
            summary = real.simulation.summary
            status, result = summary.GET(request.GET.getlist("key"),
                                          request.GET.getlist("keys"),
                                          time_interval)
            if status != 200:
                return HttpResponse(result, status = status)

            results[real.iens] = result

        return JsonResponse(results)
