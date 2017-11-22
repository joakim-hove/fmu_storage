# This file will set up temporary directory for testing, the sqlite database and
# files created during testing will be located in this directory. The
# environment variable $FMU_STORAGE_TEST_AREA will be set to point to this
# directory. When the tests have completed:
#
#     rm -rf $FMU_STORAGE_TEST_AREA
#
# should clean up.

export FMU_STORAGE_TEST_AREA=$(mktemp -d)
export DJANGO_SETTINGS_MODULE=fmu_storage.settings
export DATABASE_URL="sqlite:////$FMU_STORAGE_TEST_AREA/fmu_storage.sqlite"
export STORAGE_ROOT=$FMU_STORAGE_TEST_AREA/storage
