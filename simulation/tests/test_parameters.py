import tempfile
import os.path
import json


from django.test import TestCase, Client
from django.urls import reverse
from simulation.models import *

from .context import TestContext

class ParameterTest(TestCase):


    def setUp(self):
        self.context = TestContext( )


    def test_create(self):
        parameter = Parameter.objects.create( name = "MULTPV",
                                              value = 1.0 ,
                                              simulation = self.context.simulation )

        self.context.simulation.add_parameter( "MULTPV2" , 2.0 )
        p = self.context.simulation.parameters( )
        self.assertEqual( len(p) , 2 )
        self.assertEqual( p["MULTPV"] , 1.0 )
        self.assertEqual( p["MULTPV2"] , 2.0 )

        client = Client( )
        url = reverse( "api.simulation.parameters" , kwargs = {"id" : self.context.simulation.id })
        response = client.get( url )
        self.assertEqual( response.status_code , 200 )
        data = json.loads( response.content )
        self.assertEqual( len(data) , 2 )
        self.assertEqual( data["MULTPV"] , 1.0 )
        self.assertEqual( data["MULTPV2"] , 2.0 )


        url = reverse( "api.simulation.parameters" , kwargs = {"id" : 0123471})
        response = client.get( url )
        self.assertEqual( response.status_code , 404 )


        with self.assertRaises(ValueError):
            Parameter.loads( self.context.simulation, "PARAM1 = 100\n")

        with self.assertRaises(ValueError):
            Parameter.loads( self.context.simulation, "PARAM1 : 100\n")

        with self.assertRaises(ValueError):
            Parameter.loads( self.context.simulation, "PARAM1  100X\n")

        Parameter.loads( self.context.simulation, "PARAM1 100\nPARAM2 200")

        url = reverse( "api.simulation.parameters" , kwargs = {"id" : self.context.simulation.id })
        response = client.get( url )
        self.assertEqual( response.status_code , 200 )
        data = json.loads( response.content )
        self.assertEqual( len(data) , 4 )
        self.assertEqual( data["PARAM1"] , 100 )
        self.assertEqual( data["PARAM2"] , 200 )

        Parameter.loads( self.context.simulation, '{"PARAM3" :  300, "PARAM4" : 400}')
        url = reverse( "api.simulation.parameters" , kwargs = {"id" : self.context.simulation.id })
        response = client.get( url )
        self.assertEqual( response.status_code , 200 )
        data = json.loads( response.content )
        self.assertEqual( len(data) , 6 )
        self.assertEqual( data["PARAM3"] , 300 )
        self.assertEqual( data["PARAM4"] , 400 )


        url = reverse( "api.simulation.parameters" , kwargs = {"id" : self.context.simulation.id })
        response = client.post(url, {"parameters" : "PARAM5 500\nPARAM6 600"})

        response = client.get( url )
        self.assertEqual( response.status_code , 200 )
        data = json.loads( response.content )
        self.assertEqual( len(data) , 8 )
        self.assertEqual( data["PARAM5"] , 500 )
        self.assertEqual( data["PARAM6"] , 600 )

