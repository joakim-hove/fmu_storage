# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os.path

from ecl.ecl import EclGrid, EclSum, EclFile

from django.core.files import File
from django.db.models.signals import post_delete, pre_delete
from django.dispatch.dispatcher import receiver
from django.db.models import *
from django.db import IntegrityError


def make_file_field(cls, name, FILES):
    if name in FILES:
        form_field = FILES[name]
        instance = cls.objects.create( content = form_field,
                                       input_name = form_field.name )
        if instance.is_valid( ):
            return instance
        else:
            instance.delete( )
            raise ValueError

    return None




class BaseFile(Model):
    input_name = CharField( max_length = 132 )
    content = FileField( upload_to = "%Y/%m/%d" )

    def data(self):
        raise NotImplementedError("The data() method is not implemented in the base class")

    def path(self):
        return self.content.path

    def __unicode__(self):
        return self.input_name

    def is_valid(self):
        if self.content:
            return os.path.exists( self.content.path )
        return False


    @classmethod
    def form_create(cls, form_field):
        if form_field is None:
            return None

        instance = cls.objects.create( content = form_field,
                                       input_name = form_field.name )
        if instance.is_valid( ):
            return instance
        else:
            instance.delete( )
            raise ValueError("Invalid input to create: %s" % cls)



class InitFile(BaseFile):

    def data(self):
        return EclFile( self.path() )

    @classmethod
    def create(cls,filename):
        ecl_file = EclFile( filename )
        init_file = InitFile( )
        with open(filename, "r") as f:
            init_file.content.save( os.path.basename( filename ), File(f))
        return init_file


class RestartFile(BaseFile):

    def data(self):
        return EclFile( self.path() )


    @classmethod
    def create(cls,filename):
        ecl_file = EclFile( filename )
        restart_file = RestartFile( )
        with open(filename, "r") as f:
            restart_file.content.save( os.path.basename( filename ), File(f))
        return restart_file


class DataFile(BaseFile):

    def data(self):
        return open( self.path( )).read( )


    @classmethod
    def create(cls, filename):
        data_file = DataFile(  )
        with open(filename, "r") as f:
            data_file.content.save( os.path.basename( filename ), File(f))
        return data_file


class GridFile(BaseFile):

    def data(self):
        return EclGrid( self.path( ) )


    def is_valid(self):
        try:
            f = EclGrid( self.path( ) )
            return True
        except:
            return False

    @classmethod
    def create(cls, filename):
        g = EclGrid( filename )
        grid = GridFile(  )
        with open(filename, "r") as f:
            grid.content.save( os.path.basename( filename ), File(f))
        return grid


class Summary(Model):
    unsmry_file = ForeignKey( BaseFile , related_name = "unsmry_file", on_delete = CASCADE)
    smspec_file = ForeignKey( BaseFile , related_name = "smspec_file", on_delete = CASCADE)

    def data(self):
        return EclSum.load( self.smspec_file.path() , self.unsmry_file.path() )

    def __unicode__(self):
        return os.path.splitext( self.smspec_file.input_name )[0]


    @classmethod
    def create(self, smspec_file, unsmry_file):
        ecl_sum = EclSum.load( smspec_file, unsmry_file )
        smspec_name = os.path.basename( smspec_file )
        unsmry_name = os.path.basename( unsmry_file )

        smspec = BaseFile( input_name = smspec_name )
        with open(smspec_file, "r") as f:
            smspec.content.save( smspec_name , File(f))

        unsmry = BaseFile( input_name = unsmry_name)
        with open(unsmry_file, "r") as f:
            unsmry.content.save( unsmry_name , File(f))

        summary = Summary.objects.create( unsmry_file = unsmry,
                                          smspec_file = smspec )
        return summary


class Simulation(Model):
    summary = ForeignKey( Summary , on_delete = CASCADE)
    restart = ForeignKey( RestartFile, null = True , on_delete = SET_NULL)
    grid = ForeignKey( GridFile , null = True , on_delete = SET_NULL)
    data = ForeignKey( DataFile , null = True , on_delete = SET_NULL)
    init = ForeignKey( InitFile , null = True , on_delete = SET_NULL)

    @classmethod
    def create(cls, summary, restart = None, grid = None, data = None, init = None, parameters = None):
        simulation = cls.objects.create( summary = summary,
                                         restart = restart,
                                         grid = grid,
                                         data = data,
                                         init = init)

        if parameters:
            for (param,value) in parameters.items():
                simulation.add_parameter( param , value )

        return simulation



    def id_list(self):
        d = {"simulation" : self.id,
             "summary" : self.summary.id }
        return d


    def add_grid(self, grid_file):
        self.grid = GridFile.create( grid_file )
        self.save( )


    def parameters(self):
        params = {}
        for p in self.parameter_set.all():
            params[p.name] = p.value
        return params


    def add_parameter(self, name , value):
        p = Parameter.objects.create( name = name,
                                      value = value,
                                      simulation = self )

    def add_parameters(self, parameters):
        for key,value in parameters.items():
            self.add_parameters(key, value)

    def add_restart(self, restart_file):
        self.restart = RestartFile.create( restart_file )
        self.save( )

    def add_init(self, init_file):
        self.init = InitFile.create( init_file )
        self.save( )



class Parameter(Model):
    name = CharField( max_length = 64 )
    value = FloatField( )
    simulation = ForeignKey( Simulation , on_delete = CASCADE )


@receiver(post_delete, sender=BaseFile)
def delete_file(sender, instance, *args, **kwargs):
    if instance.content:
        if os.path.isfile(instance.content.path):
            os.remove( instance.content.path )
