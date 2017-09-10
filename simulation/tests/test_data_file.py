import tempfile
import os.path
import json

from ecl.ecl import EclGrid, EclGridGenerator, EclSum
from ecl.test import TestAreaContext
from ecl.test.ecl_mock import createEclSum

from django.core.files.base import ContentFile
from django.core.files import File
from django.test import TestCase, Client, override_settings
from django.urls import reverse

from simulation.models import *


class DataFileTest(TestCase):

    def setUp(self):
        pass

    def test_url(self):
        with self.assertRaises(IOError):
            data_file = DataFile.create( "file/dose/not/exist")

        data_file = DataFile.create( os.path.join( os.path.dirname( __file__ ) , "data" , "SPE1.DATA"))

        client = Client( )
        url = reverse( "simulation.data_file.view.detail" , kwargs = {"id" : 100000})
        response = client.get( url )
        self.assertEqual( response.status_code , 404 )

        url = reverse( "simulation.data_file.view.detail" , kwargs = {"id" : data_file.id})
        response = client.get( url )
        self.assertEqual( response.status_code , 200 )

        url = reverse( "simulation.data_file.download" , kwargs = {"id" : 191823})
        response = client.get( url )
        self.assertEqual( response.status_code , 404 )

        url = reverse( "simulation.data_file.download" , kwargs = {"id" : data_file.id})
        response = client.get( url )
        self.assertEqual( response.status_code , 200 )

