import getpass
import os
import grp
import random

from ecl.ecl import EclGrid, EclGridGenerator, EclSum, openFortIO, EclFile
from ecl.test import TestAreaContext
from ecl.test.ecl_mock import createEclSum

from simulation.models import *

def fopr(days):
    return days

def random_fopr(days):
    return fopr(days) * random.random( )


def fopt(days):
    return days

def random_fopt(days):
    return fopt(days) * random.random()


def fgpt(days):
    if days < 50:
        return days
    else:
        return 100 - days

def random_fgpt(days):
    return fgpt(days) * random.random()



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
        self.user = getpass.getuser()
        self.group = grp.getgrgid( os.getgid( ) )[0]
        self.case = case
        with TestAreaContext("summary"):
            case.fwrite( )
            self.summary = Summary.create( "CASE.SMSPEC" , "CASE.UNSMRY" , self.group )

        self.simulation = Simulation.create( summary = self.summary, parameters = [("CPARAM1", 100), ("CPARAM2", 200)] )
        self.grid = EclGridGenerator.create_rectangular( (10,10,10),(1,1,1) )


    @classmethod
    def create_INIT(cls):
        ecl_kw = EclKW(1000 , "PORV" , EclDataType.ECL_FLOAT )
        with openFortIO("CASE.INIT", FortIO.WRITE_MODE) as f:
            ecl_kw.fwrite( f )

        return EclFile( "CASE.INIT" )


    @classmethod
    def create_UNRST(cls):
        ecl_kw = EclKW(1000 , "PRESSURE" , EclDataType.ECL_FLOAT )
        with openFortIO("CASE.UNRST", FortIO.WRITE_MODE) as f:
            ecl_kw.fwrite( f )

        return EclFile( "CASE.UNRST" )


    @classmethod
    def random_simulation(cls):
        length = 100
        case = createEclSum("CASE" , [("FOPT", None , 0) , ("FOPR" , None , 0), ("FGPT" , None , 0)],
                            sim_length_days = length,
                            num_report_step = 10,
                            num_mini_step = 10,
                            func_table = {"FOPT" : random_fopt,
                                          "FOPR" : random_fopr ,
                                          "FGPT" : random_fgpt })

        group = grp.getgrgid( os.getgid( ) )[0]
        with TestAreaContext("summary"):
            case.fwrite( )
            summary_case = Summary.create( "CASE.SMSPEC" , "CASE.UNSMRY" , group )

        return Simulation.create( summary = summary_case, parameters = [("CPARAM1", 100*random.random()), ("CPARAM2", 200*random.random())] )
