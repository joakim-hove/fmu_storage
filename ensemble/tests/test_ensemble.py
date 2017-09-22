import tempfile
import os.path
import json

from django.test import TransactionTestCase, TestCase, Client
from django.urls import reverse

from ensemble.models import *
from simulation.tests.context import TestContext as SimulationContext

class EnsembleTest(TransactionTestCase):


    def setUp(self):
        self.sim_context = SimulationContext( )

    def test_create(self):
        ens = Ensemble.objects.create( iteration = 0,
                                       name = "My ensemble",
                                       id = "MyEnsemble" )

        self.assertEqual( len(ens), 0 )

        for i in range(10):
            sim = Simulation.create( summary = self.sim_context.summary )
            real = Realisation.objects.create( iens = i,
                                               simulation = sim,
                                               ensemble = ens )

        self.assertEqual( len(ens), 10 )
        self.assertEqual( ens.size(), 10 )


    def test_api(self):
        client = Client( )
        url = reverse( "api.ensemble.create")
        response = client.post( url , {"name" : "My ensemble",
                                       "iteration" : 0})
        self.assertEqual( response.status_code , 400 )

        response = client.post( url , {"name" : "My ensemble",
                                       "iteration" : 0,
                                       "id" : "SecretID" })
        print response.content
        self.assertEqual( response.status_code , 200 )

        ens_id = response.content
        ens = Ensemble.objects.get( pk = ens_id )

