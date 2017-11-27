import tempfile
import os.path
import json
import requests

from ecl.test import TestAreaContext

from django.test import TransactionTestCase, TestCase, Client
from django.urls import reverse

from ensemble.models import *
from simulation.tests.context import TestContext as SimulationContext

class UrlTest(TransactionTestCase):


    def setUp(self):
        self.sim_context = SimulationContext( )

    def test_get(self):
       client = Client()
       url = reverse("api.urls")
       response = client.get(url)
       self.assertEqual( response.status_code, 200)
       url_map = json.loads( response.content )

       url = url_map["api.ensemble.get_or_create"][0]
       response = client.post(url ,  {"name" : "My ensemble",
                                      "iteration" : 0,
                                      "ext_id" : "sectreid",
                                      "user": "User"})
       self.assertEqual(response.status_code , 200)
       ens_id = int(response.content)

       ens = Ensemble.objects.get( pk = ens_id )


       url_fmt = url_map["api.ensemble.add_simulation"][0]
       with TestAreaContext("url_test"):
           self.sim_context.case.fwrite( )
           response = client.post(url_fmt.format( ens_id = ens.id ), {"smspec_file" : open("CASE.SMSPEC"),
                                                                      "unsmry_file" : open("CASE.UNSMRY"),
                                                                      "group" : self.sim_context.group,
                                                                      "iens" : 10})
       self.assertEqual( response.status_code, 200 )
       real_id = int(response.content)
       real = Realisation.objects.get( pk = real_id )

