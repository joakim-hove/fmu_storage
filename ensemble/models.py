# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import *
from simulation.models import *


class Ensemble(Model):
    ext_id = CharField( max_length = 256, unique = True, default = None)
    iteration = IntegerField("Iteration", default = 0 )
    name = CharField( max_length = 256 )
    creation_time = DateTimeField( auto_now_add=True )
    user = CharField( max_length = 32, default = None)

    def size(self):
        return len(Realisation.objects.filter( ensemble = self ))

    def __unicode__(self):
        return self.name

    def __len__(self):
        return self.size()


    def realisations(self):
        return Realisation.objects.filter( ensemble = self )

class Realisation(Model):
    iens = IntegerField("Realisation")
    simulation = OneToOneField( Simulation , on_delete = CASCADE )
    ensemble = ForeignKey( Ensemble , on_delete = CASCADE )


    class Meta:
        unique_together = ("iens", "ensemble")


    def __unicode__(self):
        return "%s:%d" % (self.ensemble.name, self.iens)

    @classmethod
    def update_or_create(cls, ensemble, iens, simulation):
        try:
            realisation = Realisation.objects.get( iens = iens, ensemble = ensemble)
        except Realisation.DoesNotExist:
            realisation = Realisation(iens = iens, ensemble = ensemble)

        realisation.simulation = simulation
        realisation.save()
        return realisation
