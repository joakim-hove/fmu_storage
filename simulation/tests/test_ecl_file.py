import tempfile
import os.path


from ecl.ecl import EclGrid, EclGridGenerator, EclSum
from ecl.test import TestAreaContext
from ecl.test.ecl_mock import createEclSum

from django.core.files.base import ContentFile
from django.core.files import File
from django.test import TestCase, Client, override_settings

from simulation.models import *

def fopr(days):
    return days

def fopt(days):
    return days

def fgpt(days):
    if days < 50:
        return days
    else:
        return 100 - days

class EclFileTest(TestCase):

    def setUp(self):
        pass

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_create(self):
        name = tempfile.NamedTemporaryFile( )

        f = BaseFile( input_name = "NameX" )
        f.content.save( "input-name" , ContentFile("Content"))

        self.assertEqual( len(BaseFile.objects.all()) , 1 )

        with self.assertRaises(NotImplementedError):
            f.data( )

        self.assertTrue( os.path.isfile( f.path() ))


class GridFileTest(TestCase):

    def test_create(self):
        grid = EclGridGenerator.create_rectangular( (10,10,10) , (1,1,1))
        with TestAreaContext( "grid"):
            grid.save_EGRID( "TEST.EGRID")
            f = GridFile( input_name = "TEST.EGRID")
            with open("TEST.EGRID") as grid_file:
                f.content.save( "TEST.EGRID" , File( grid_file ))

        grid = f.data()
        self.assertTrue( isinstance(grid, EclGrid ))



class SummaryFileTest(TestCase):

    def test_create(self):
        length = 100
        case = createEclSum("CASE" , [("FOPT", None , 0) , ("FOPR" , None , 0), ("FGPT" , None , 0)],
                            sim_length_days = length,
                            num_report_step = 10,
                            num_mini_step = 10,
                            func_table = {"FOPT" : fopt,
                                          "FOPR" : fopr ,
                                          "FGPT" : fgpt })

        with TestAreaContext("summary"):
            case.fwrite( )
            summary = Summary.create( "CASE.SMSPEC" , "CASE.UNSMRY" )
            ecl_sum = summary.data( )
            self.assertTrue( isinstance( ecl_sum , EclSum ))

            with self.assertRaises(IOError):
                sum = Summary.create("CASE_DOES_NOT_EXIST" , "CASE.UNSMRY")

            with self.assertRaises(IOError):
                sum = Summary.create("CASE.SMSPEC" , "CASE.UNSMRY_XXX")

        sim = Simulation.objects.create( summary = summary )



