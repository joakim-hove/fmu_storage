# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import *
from simulation.models import *


class Ensemble(Model):
    ext_id = CharField( max_length = 256, unique = True, default = None)
    iteration = IntegerField("Iteration", default = 0 )
    name = CharField( max_length = 256 )
    creation_time = DateTimeField( auto_now_add=True )

    def size(self):
        return len(Realisation.objects.filter( ensemble = self ))


    def __len__(self):
        return self.size()


class Realisation(Model):
    iens = IntegerField("Realisation")
    simulation = OneToOneField( Simulation , on_delete = CASCADE )
    ensemble = ForeignKey( Ensemble , on_delete = CASCADE )

