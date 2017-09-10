from simulation.models import *

class Count(object):

    def __init__(self, simulation = None, summary = None, grid = None, init = None, data = None):
        self.simulation = 0
        self.summary = 0
        self.grid = 0
        self.init = 0
        self.data = 0

        if not simulation is None:
            self.simulation = simulation

        if not summary is None:
            self.summary = summary

        if not grid is None:
            self.grid = grid

        if not grid is None:
            self.grid = grid

        if not init is None:
            self.init = init

    def __eq__(self,other):
        if self.simulation != other.simulation:
            return False

        if self.summary != other.summary:
            return False

        if self.grid != other.grid:
            return False

        if self.init != other.init:
            return False

        if self.data != other.data:
            return False

        return True


    def __sub__(self, other):
        return Count( simulation = self.simulation - other.simulation,
                      summary = self.summary - other.summary,
                      grid = self.grid - other.grid,
                      init = self.init - other.init,
                      data = self.data - other.data )

    def __str__(self):
            return "<Simulations:%d  Summary:%d  Grid:%d  Init:%d  Data:%d>" % (self.simulation, self.summary, self.grid, self.init, self.data)

    def __repr__(self):
        return str(self)

class ObjectCount(Count):

    def __init__(self):
        self.simulation = len(Simulation.objects.all())
        self.summary = len(Summary.objects.all())
        self.grid = len(GridFile.objects.all())
        self.init = len(InitFile.objects.all())
        self.data = len(DataFile.objects.all())


