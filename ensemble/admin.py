# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from simulation.models import *

admin.site.register(Ensemble)
admin.site.register(Realisation)
