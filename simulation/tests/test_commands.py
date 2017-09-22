import tempfile
import os.path
from argparse import ArgumentParser

from ecl.ecl import EclGrid, EclGridGenerator, EclSum
from ecl.test import TestAreaContext
from ecl.test.ecl_mock import createEclSum

from django.core.files.base import ContentFile
from django.core.files import File
from django.test import TestCase, Client, override_settings

from simulation.models import *
from .context import TestContext
from .object_count import ObjectCount, Count

from simulation.management.commands.add_summary import Command as AddSummary
from simulation.management.commands.add_simulation import Command as AddSimulation

class CommandTest(TestCase):

    def setUp(self):
        self.context = TestContext( )

    def test_add_summary(self):
        with TestAreaContext("add_summary"):
            self.context.case.fwrite( )

            parser = ArgumentParser( )
            add_summary = AddSummary( )
            add_summary.add_arguments( parser )
            count0 = ObjectCount( )
            add_summary.handle( case = ["CASE"] )
            count1 = ObjectCount( )
            self.assertEqual( 1 , count1.summary - count0.summary )


    def test_add_simulation(self):
        with TestAreaContext("add_simulation"):
            self.context.case.fwrite( )
            self.context.grid.save_EGRID("CASE.EGRID")

            parser = ArgumentParser( )
            add_sim = AddSimulation( )
            add_sim.add_arguments( parser )
            count0 = ObjectCount( )
            add_sim.handle( case = ["CASE"] )
            count1 = ObjectCount( )
            self.assertEqual( 1 , count1.summary - count0.summary )
            self.assertEqual( 1 , count1.grid - count0.grid )
