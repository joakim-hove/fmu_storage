import tempfile
import os.path
import json

from ecl.test import TestAreaContext

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
                                       user = "user",
                                       ext_id = "MyEnsemble" )

        self.assertEqual( len(ens), 0 )

        for i in range(10):
            sim = Simulation.create( summary = self.sim_context.summary )
            real = Realisation.objects.create( iens = i,
                                               simulation = sim,
                                               ensemble = ens )

        self.assertEqual( len(ens), 10 )
        self.assertEqual( ens.size(), 10 )


    def test_create_api(self):
        client = Client( )
        url = reverse( "api.ensemble.get_or_create")
        response = client.post( url , {"name" : "My ensemble",
                                       "iteration" : 0,
                                       "user" : "xyz"})
        self.assertEqual( response.status_code , 400 )

        response = client.post( url , {"name" : "My ensemble",
                                       "iteration" : 0,
                                       "ext_id" : "SecretID"})
        self.assertEqual( response.status_code , 400 )

        response = client.post( url , {"name" : "My ensemble",
                                       "iteration" : 0,
                                       "ext_id" : "SecretID",
                                       "user" : "bjarne"})
        self.assertEqual( response.status_code , 200 )

        ens_id = response.content
        ens = Ensemble.objects.get( pk = ens_id )

        response = client.post(url, {"ext_id" : "SecretID"})
        self.assertEqual( response.status_code, 200)
        ens_id2 = response.content
        self.assertEqual(ens_id, ens_id2)


    def test_realisation_api(self):
        ens = Ensemble.objects.create( iteration = 0,
                                       name = "My ensemble",
                                       user = "user",
                                       ext_id = "MyEnsemble" )

        client = Client()
        url = reverse("api.ensemble.add_realisation", kwargs = {"ens_id" : ens.id})
        response = client.post(url , {"sim_id" : 100000})
        self.assertEqual( response.status_code, 404)

        url = reverse("api.ensemble.add_realisation", kwargs = {"ens_id" : "NoSuchEnsemble"})
        response = client.post(url , {"sim_id" : self.sim_context.simulation})
        self.assertEqual( response.status_code, 404)


    def test_simulation_api(self):
        ens = Ensemble.objects.create( iteration = 0,
                                       name = "My ensemble",
                                       user = "user",
                                       ext_id = "MyEnsemble" )

        client = Client()
        url = reverse("api.ensemble.add_simulation", kwargs = {"ens_id" : ens.id})
        with TestAreaContext("summary"):
            self.sim_context.case.fwrite( )
            # Missing group => 403
            response = client.post( url , {"smspec_file" : open("CASE.SMSPEC"),
                                           "unsmry_file" : open("CASE.UNSMRY"),
                                           "iens" : 100})
            self.assertEqual( response.status_code , 403 )

            # Missing iens => 400
            response = client.post( url , {"smspec_file" : open("CASE.SMSPEC"),
                                           "unsmry_file" : open("CASE.UNSMRY"),
                                           "group" : self.sim_context.group})
            self.assertEqual( response.status_code , 400 )

            # All good => 200
            response = client.post( url , {"smspec_file" : open("CASE.SMSPEC"),
                                           "unsmry_file" : open("CASE.UNSMRY"),
                                           "group" : self.sim_context.group,
                                           "iens" : 10})

            self.assertEqual( response.status_code , 200 )
            real_id1 = int(response.content)
            real = Realisation.objects.get( pk = real_id1 )
            sim_id1 = real.simulation.id

            response = client.post( url , {"smspec_file" : open("CASE.SMSPEC"),
                                           "unsmry_file" : open("CASE.UNSMRY"),
                                           "group" : self.sim_context.group,
                                           "iens" : 10})

            self.assertEqual( response.status_code , 200 )
            real_id2 = int(response.content)
            real = Realisation.objects.get( pk = real_id2 )
            sim_id2 = real.simulation.id

            self.assertEqual( real_id1, real_id2)
            self.assertNotEqual( sim_id1, sim_id2)



    def test_ensemble_view(self):
        ens = Ensemble.objects.create( iteration = 0,
                                       name = "MyEnsemble",
                                       user = "user",
                                       ext_id = "adfa" )
        client = Client()
        url = reverse("ensemble.list_view")
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse("ensemble.detail_view", kwargs = {"id" : 100000})
        response = client.get(url)
        self.assertEqual(response.status_code, 404)

        url = reverse("ensemble.detail_view", kwargs = {"id" : ens.id})
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        
        url = reverse("ensemble.realisation.detail_view", kwargs = {"id" : 100000})
        response = client.get(url)
        self.assertEqual(response.status_code, 404)


