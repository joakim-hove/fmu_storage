from ecl.ecl import EclGrid, EclGridGenerator, EclSum, openFortIO, EclFile
from ecl.test import TestAreaContext
from ecl.test.ecl_mock import createEclSum

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

class TestContext(object):

    def __init__(self):
        length = 100
        case = createEclSum("CASE" , [("FOPT", None , 0) , ("FOPR" , None , 0), ("FGPT" , None , 0)],
                            sim_length_days = length,
                            num_report_step = 10,
                            num_mini_step = 10,
                            func_table = {"FOPT" : fopt,
                                          "FOPR" : fopr ,
                                          "FGPT" : fgpt })

        self.case = case
        with TestAreaContext("summary"):
            case.fwrite( )
            self.summary = Summary.create( "CASE.SMSPEC" , "CASE.UNSMRY" )

        self.simulation = Simulation.create( summary = self.summary )
        self.grid = EclGridGenerator.create_rectangular( (10,10,10),(1,1,1) )


    def create_INIT(self):
        ecl_kw = EclKW(1000 , "PORV" , EclDataType.ECL_FLOAT )
        with openFortIO("CASE.INIT", FortIO.WRITE_MODE) as f:
            ecl_kw.fwrite( f )

        return EclFile( "CASE.INIT" )


    def create_UNRST(self):
        ecl_kw = EclKW(1000 , "PRESSURE" , EclDataType.ECL_FLOAT )
        with openFortIO("CASE.UNRST", FortIO.WRITE_MODE) as f:
            ecl_kw.fwrite( f )

        return EclFile( "CASE.UNRST" )
