# This is a template file with environment settings which are required
# for Django to work properly. You are advised to make a copy of this
# file with your personal settings, and then source that before you
# start development - your personal file should not be under version
# control.


# This should be the PYTHONPATH to the settings module which applies
# to this project. Your python environment should be so that:
#
#  python -m $DJANGO_SETTINGS_MODULE
#
# works without error.
export DJANGO_SETTINGS_MODULE=fmu_storage.settings


# This should be a database connection string, the string will be
# parsed by dj_database_url.parse( ) function.
export DATABASE_URL="sqlite:///fmu_storage.sqlite"


# A very important part of the ecl_storage application is to store
# files from eclipse simulations. The environment variable
# STORAGE_ROOT should point to the root of the file storage area. The
# files will eventually be stored in:
#
# $STORAGE_ROOT/fmu_storage/$YEAR/$MONTH/$DAY/

export STORAGE_ROOT=$(pwd)/storage

