# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from simulation.models import *

admin.site.register(BaseFile)
admin.site.register(Summary)
admin.site.register(InitFile)
admin.site.register(GridFile)
admin.site.register(DataFile)
admin.site.register(RestartFile)
admin.site.register(Parameter)
admin.site.register(Simulation)
