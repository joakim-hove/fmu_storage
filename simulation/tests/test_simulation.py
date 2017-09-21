import tempfile
import os.path
import json

from ecl.ecl import EclGrid, EclGridGenerator, EclSum
from ecl.test import TestAreaContext
from ecl.test.ecl_mock import createEclSum

from django.test import TestCase, Client
from django.urls import reverse

from simulation.models import *

from .context import TestContext
from .object_count import ObjectCount, Count

class SimulationTest(TestCase):


    def setUp(self):
        self.context = TestContext( )

    def test_create(self):
        params = {"P1" : 100,
                  "P2" : 200,
                  "P3" : 300}
        sim = Simulation.create( self.context.summary, parameters = params)
        params_get = sim.parameters( )
        for key in params:
            self.assertTrue(key in params_get)
            self.assertEqual( params_get[key] , params[key] )


    def test_summary(self):
        with TestAreaContext("summary"):
            with open("CASE.SMSPEC","w") as f:
                f.write("Hei ...")

            with open("CASE.UNSMRY","w") as f:
                f.write("Hei ...")

            with self.assertRaises(IOError):
                summary = Summary.create( "CASE.SMSPEC" , "CASE.UNSMRY" , self.context.group)


    def test_view(self):
        client = Client( )
        url = reverse( "simulation.view.detail" , kwargs = {"id" : self.context.simulation.id})
        response = client.get( url )
        self.assertEqual( response.status_code , 200 )

        url = reverse( "simulation.view.detail" , kwargs = {"id" : 99999 })
        response = client.get( url )
        self.assertEqual( response.status_code , 404 )

        url = reverse( "simulation.summary.view.detail" , kwargs = {"id" : self.context.summary.id})
        response = client.get( url )
        self.assertEqual( response.status_code , 200 )

        url = reverse( "simulation.summary.view.detail" , kwargs = {"id" : 9999})
        response = client.get( url )
        self.assertEqual( response.status_code , 404 )

        url = reverse( "api.simulation.summary.data" , kwargs = {"id" : 971672})
        response = client.get( url )
        self.assertEqual( response.status_code , 404 )

        url = reverse( "api.simulation.summary.data" , kwargs = {"id" : self.context.summary.id })
        response = client.get( url , {"key" : ["MISSING_KEY"]})
        self.assertEqual( response.status_code , 404 )

        url = reverse( "api.simulation.summary.data" , kwargs = {"id" : self.context.summary.id })
        response = client.get( url , {"key" : ["FOPT","FOPR"]})
        self.assertEqual( response.status_code , 200 )
        data = json.loads( response.content )
        self.assertTrue( "data" in data )
        self.assertTrue( "time" in data )
        values = data["data"]
        self.assertIn( "FOPR" , values )
        self.assertIn( "FOPT" , values )


        url = reverse( "api.simulation.summary.data" , kwargs = {"id" : self.context.summary.id })
        response = client.get( url , {"keys" : ["FOP*"]})
        self.assertEqual( response.status_code , 200 )
        data = json.loads( response.content )
        self.assertTrue( "data" in data )
        self.assertTrue( "time" in data )
        values = data["data"]
        self.assertIn( "FOPR" , values )
        self.assertIn( "FOPT" , values )

        url = reverse( "api.simulation.summary.data" , kwargs = {"id" : self.context.summary.id })
        response = client.get( url , {"keys" : ["FOPT","FOPR"], "time_interval" : "1X"})
        self.assertEqual( response.status_code , 400 )

    def test_form_post(self):
        client = Client( )
        url = reverse( "simulation.upload.view")
        with TestAreaContext("summary"):
            self.context.case.fwrite( )
            count0 = ObjectCount( )
            response = client.post( url , {"smspec_file" : open("CASE.SMSPEC"),
                                           "unsmry_file" : open("CASE.UNSMRY")})
            self.assertEqual( response.status_code , 200 )

            response = client.post( url , {"smspec_file" : open("CASE.SMSPEC"),
                                           "unsmry_file" : open("CASE.UNSMRY"),
                                           "group" : self.context.group })
            self.assertEqual( response.status_code , 302 )
            count1 = ObjectCount( )
            self.assertEqual( 1 , count1.simulation - count0.simulation )

            with open("file" , "w") as f:
                f.write("Hell ...")

            response = client.post( url , {"smspec_file" : open("file"),
                                           "unsmry_file" : open("CASE.UNSMRY"),
                                           "group" : self.context.group })
            self.assertEqual( response.status_code , 200 )

            count2 = ObjectCount( )
            self.assertEqual( count1 , count2 )

            # Invalid grid
            response = client.post( url , {"smspec_file" : open("CASE.SMSPEC"),
                                           "unsmry_file" : open("CASE.UNSMRY"),
                                           "grid_file"   : open("CASE.UNSMRY"),
                                           "group" : self.context.group })

            count2 = ObjectCount( )
            self.assertEqual( count1 , count2 )

            # OK
            self.context.grid.save_EGRID("CASE.EGRID")
            response = client.post( url , {"smspec_file" : open("CASE.SMSPEC"),
                                           "unsmry_file" : open("CASE.UNSMRY"),
                                           "grid_file"   : open("CASE.EGRID"),
                                           "group" : self.context.group })

            count3 = ObjectCount( )
            self.assertEqual( count3 - count2 , Count( simulation = 1 , summary = 1 , grid = 1))


    def test_api_post(self):
        client = Client( )
        url = reverse( "simulation.upload.view")
        with TestAreaContext("summary"):
            self.context.case.fwrite( )
            self.context.grid.save_EGRID("CASE.EGRID")
            count0 = ObjectCount( )

            url = reverse( "api.simulation.upload")
            response = client.post( url , {"smspec_file" : open("CASE.SMSPEC"),
                                           "unsmry_file" : open("CASE.UNSMRY"),
                                           "grid_file"   : open("CASE.EGRID"),
                                           "group" : self.context.group })
            self.assertEqual( response.status_code , 200 )


            url = reverse( "api.simulation.upload")
            response = client.post( url , {"smspec_file" : open("CASE.SMSPEC"),
                                           "unsmry_file" : open("CASE.UNSMRY"),
                                           "grid_file"   : open("CASE.UNSMRY"),
                                           "group" : self.context.group })
            self.assertEqual( response.status_code , 400 )


