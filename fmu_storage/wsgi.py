"""
WSGI config for fmu_storage project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""
import json
import os
import os.path

from django.core.wsgi import get_wsgi_application
settings_file = os.path.join( os.path.dirname(__file__), "fmu_settings.json")
if os.path.isfile(settings_file):
    with open(settings_file) as fileH:
        settings = json.load(fileH)

    for key,value in settings.iteritems():
        os.environ[key] = value

application = get_wsgi_application()
