# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError,Http404
from django.urls import reverse
from django.db import transaction

from .models import *
from .forms import UploadForm


class UploadSimulation(View):
    def post(self , request , id = None):

        form = UploadForm( request.POST , request.FILES)
        if form.is_valid():
            group = request.POST["group"]
            try:
                with transaction.atomic():
                    unsmry_file = BaseFile.form_create( request.FILES.get("unsmry_file"), group )
                    smspec_file = BaseFile.form_create( request.FILES.get("smspec_file"), group )
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
                url = reverse( "simulation.view.detail" , kwargs = {"id" : simulation.id})
                return HttpResponseRedirect( url )
            except (ValueError,IOError) as error:
                return render( request, "simulation/upload.html" , {"form" : form, "error" : str(error) })

        return render( request, "simulation/upload.html" , {"form" : form})



    def get(self, request):
        return render( request, "simulation/upload.html" , {"form" : UploadForm()})

class ViewSimulation(View):

    def get(self, request, id = None):
        if id is None:
            raise HttpResponseServerError("NO id supplied for simulation")

        try:
            simulation = Simulation.objects.get( pk = int(id) )
        except Simulation.DoesNotExist:
            raise Http404("No simulation with id:%s" % id)

        return render( request, "simulation/view.html" , {"simulation": simulation})



class ViewDetail(View):

    def detail(self, model_cls, request, template , id = None):
        if id is None:
            raise HttpResponseServerError("NO id supplied for simulation")

        try:
            model = model_cls.objects.get( pk = int(id) )
        except model_cls.DoesNotExist:
            raise Http404("No simulation with id:%s" % id)

        return render( request, template , {"model": model})


class ViewSummary(ViewDetail):

    def get(self, request, id = None):
        return self.detail( Summary, request , "simulation/summary/view.html" , id)

class ViewDataFile(ViewDetail):

    def get(self, request, id = None):
        return self.detail( DataFile, request , "simulation/data_file/view.html" , id)


class ViewInit(ViewDetail):

    def get(self, request, id = None):
        return self.detail( InitFile, request , "simulation/init/view.html" , id)


class ViewRestart(ViewDetail):

    def get(self, request, id = None):
        return self.detail( RestartFile, request , "simulation/restart/view.html" , id)


class ViewGrid(ViewDetail):

    def get(self, request, id = None):
        return self.detail( GridFile, request , "simulation/grid/view.html" , id)


class DownLoad(View):


    def download(self, model_cls, request,id):
        if id is None:
            raise HttpResponseServerError("NO id supplied for data file")

        try:
            file = model_cls.objects.get( pk = int(id) )
        except model_cls.DoesNotExist:
            raise Http404("No data file with id:%s" % id)

        with open(file.path(), 'rb') as f:
            response = HttpResponse(f.read(),
                                    content_type="application/octet-stream")
            response['Content-Disposition'] = 'inline; filename=' + file.input_name
            return response

        return render( request, "simulation/data_file/view.html" , {"data_file" : file })


class DataFileDownload(DownLoad):

    def get(self, request, id = None):
        return self.download( DataFile , request , id)


class GridDownload(DownLoad):

    def get(self, request, id = None):
        return self.download( GridFile , request , id)


class InitDownload(DownLoad):

    def get(self, request, id = None):
        return self.download( InitFile , request , id)


class RestartDownload(DownLoad):

    def get(self, request, id = None):
        return self.download( RestartFile , request , id)
