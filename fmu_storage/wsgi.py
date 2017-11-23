"""
WSGI config for fmu_storage project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""
import json
import os
import os.path
import sys

from django.core.wsgi import get_wsgi_application
settings_file = os.path.join( os.path.dirname(__file__), "fmu_settings.json")
sys.stderr.write("Loading settings from:%s" % settings_fileimport os.path
)
if os.path.isfile(settings_file):
    with open(settings_file) as fileH:
        settings = json.load(fileH)

    for key,value in settings.iteritems():
        os.environ[key] = value
        sys.stderr.write("Setting %s=%s\n" % (key, value))

application = get_wsgi_application()
