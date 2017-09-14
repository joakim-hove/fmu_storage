# libecl [![Build Status](https://travis-ci.org/joakim-hove/fmu_storage.svg?branch=master)](https://travis-ci.org/joakim-hove/fmu_storage)


This is a small start of a WEB application which can be used to store
and manage FMU simulations. The only app in the project
currently is 'simulation', which can store one Eclipse
simulation. Further work will typically include an 'ensemble' app with
realisations and so on.

## Getting started ##

Before the web application can start you need to install the
requirements:

    pip install -r requirements

Then you need to set the environment variables DJANGO_SETTINSG_MODULE,
DATABASE_URL and STORAGE_ROOT. See the template file init_env_template
which can be used as starting point for a file to source.

The default setup assumes that you are just using sqlite, if you wish
to use another database like e.g. postgres you will need to install
driver for that and also create the database first.

When you have set up your environment correctly you can run the tests
with:

    ./manage.py test

And then afterwards you can start a webserver on localhost with:

    ./manage.py runserver


## URLs ##
```
/simulation/view/$ID/           : View a simulation - just a "summary" of the results available
/simulation/upload/             : A web form to upload results.
```

Very simple views to look at summary, data, init, restart and grid files.
```
/simulation/summary/view/$ID/
/simulation/data/view/$ID/
/simulation/init/view/$ID/
/simulation/restart/view/$ID/
/simulation/grid/view/$ID/
```

Download files:
```
/simulation/data/download/$ID/
/simulation/grid/download/$ID/
/simulation/init/download/$ID/
/simulation/restart/download/$ID/
```

API urls:
```
/api/simulation/summary/data/$ID/?key=FOPT&key=WWCT:OP_1&key=RPR:3&time_interval=1M
/api/simulation/parameters/data/$ID/
/api/simulation/upload/
```

## Adding simulation results ##

You can add simulation results interactively with the management
command:

    ./manage.py add_simulation /path/to/case

or only summary data with:

    ./manage.py add_summary /path/to/case


