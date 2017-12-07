# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ecl.ecl import EclSumKeyWordVector

from django.shortcuts import render
from django.db import transaction
from django.views import View
from django.forms import ValidationError
from django.urls import reverse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseServerError,Http404

from simulation.models import *



class SummaryData(View):

    def get(self, request, id = None):
        if id is None:
            raise HttpResponseServerError("NO id supplied for summary")

        try:
            simulation = Simulation.objects.get( pk = int(id) )
        except Simulation.DoesNotExist:
            raise Http404("No summary with id:%s" % id)

        summary = simulation.summary
        ecl_sum = summary.data( )
        sum_keywords = EclSumKeyWordVector(ecl_sum)
        for key in request.GET.getlist("key"):
            if key in ecl_sum:
                sum_keywords.add_keyword( key )
            else:
                raise Http404("No such key: %s" % key)

        for key_pattern in request.GET.getlist("keys"):
            sum_keywords.add_keywords( key_pattern )

        if "time_interval" in request.GET:
            try:
                time_list = ecl_sum.time_range( interval = request.GET["time_interval"], extend_end = False )
            except TypeError:
                return HttpResponse( status = 400 )
        else:
            report_only = True
            time_list = ecl_sum.alloc_time_vector( report_only )

        result = { "time" : [ t.datetime() for t in time_list ] }
        data = {}
        for key in sum_keywords:
            data[key] = []

        for t in time_list:
            d = ecl_sum.get_interp_row( sum_keywords , t )
            for i in range(len(sum_keywords)):
                data[ sum_keywords[i] ].append( d[i] )

        result["data"] = data
        return JsonResponse( result )

class SummaryKeys(View):
    def get(self, request, id = None):
        if id is None:
            raise HttpResponseServerError("NO id supplied for summary")

        try:
            sim = Simulation.objects.get( pk = int(id) )
        except Simulation.DoesNotExist:
            raise Http404("No summary with id:%s" % id)

        summary = sim.summary
        ecl_sum = summary.data( )
        if "pattern" in request.GET:
            keys = []
            for pattern in request.GET.getlist("pattern"):
                keys += ecl_sum.keys( pattern = pattern )
        else:
            keys = ecl_sum.keys( )

        return JsonResponse( [ s for s in keys ] , safe = False)

class Parameters(View):

    def get(self, request, id = None):
        if id is None:
            raise HttpResponseServerError("NO id supplied for summary")

        try:
            simulation = Simulation.objects.get( pk = int(id) )
        except Simulation.DoesNotExist:
            raise Http404("No summary with id:%s" % id)

        return JsonResponse( simulation.parameters() )


    def post(self, request, id):
        try:
            simulation = Simulation.objects.get( pk = int(id) )
        except Simulation.DoesNotExist:
            raise Http404("No summary with id:%s" % id)

        Parameter.loads(simulation, request.POST["parameters"])
        return JsonResponse( simulation.parameters() ) 



class Upload(View):
    @classmethod
    def upload(cls, request, group):
        with transaction.atomic():
            unsmry_file = BaseFile.form_create( request.FILES.get("unsmry_file"), group)
            smspec_file = BaseFile.form_create( request.FILES.get("smspec_file"), group)
            ecl_sum = EclSum.load( smspec_file.path(), unsmry_file.path() )
            summary = Summary.objects.create( unsmry_file = unsmry_file,
                                              smspec_file = smspec_file)

            grid = GridFile.form_create( request.FILES.get("grid_file"), group )
            init = InitFile.form_create( request.FILES.get("init_file"), group )
            data = DataFile.form_create( request.FILES.get("data_file"), group )
            restart = RestartFile.form_create( request.FILES.get("restart_file"), group )

            simulation = Simulation.objects.create( summary = summary ,
                                                    grid = grid,
                                                    data = data,
                                                    init = init,
                                                    restart = restart )
            return simulation


    def post(self, request):
        if not "group" in request.POST:
            return HttpResponse( "Missing group attribute", status = 403 )
        group = request.POST["group"]

        try:
            simulation = self.upload(request, group)
            return JsonResponse( simulation.id_list( ) )
        except (ValueError,IOError) as error:
            return HttpResponse( str(error), status = 400 )


