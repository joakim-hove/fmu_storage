import os.path
import grp
import os
from django.core.management.base import BaseCommand, CommandError
from simulation.models import *

def get_group(fname):
    stat = os.stat( fname )
    return grp.getgrgid( stat.st_gid )[0]


def add_file(sim, case, ext, method):
    fname = '%s.%s' % (case, ext)
    if os.path.isfile(fname):
        if ext == "json":
            method(sim, fname)
        else:
            method(sim, fname, get_group(fname))


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('case', nargs='+', type=str)

    def handle(self, *args, **options):
        for arg in options['case']:
            case = os.path.splitext(arg)[0]
            smspec_file = '%s.SMSPEC' % case
            unsmry_file = '%s.UNSMRY' % case
            if not os.path.isfile(smspec_file):
                raise CommandError('No suche file: %s' % smspec_file)
            if not os.path.isfile(unsmry_file):
                raise CommandError('No suche file: %s' % unsmry_file)

            summary = Summary.create(smspec_file, unsmry_file, get_group(smspec_file))
            simulation = Simulation.objects.create(summary=summary)
            for ext, method in [('EGRID', Simulation.add_grid),
                                ('UNRST', Simulation.add_restart),
                                ('INIT', Simulation.add_init),
                                ('json', Simulation.add_parameters)]:
                add_file(simulation, case, ext, method)

            self.stdout.write(self.style.SUCCESS('Successfully create simulation object %s:%d' % (case, simulation.id)))
