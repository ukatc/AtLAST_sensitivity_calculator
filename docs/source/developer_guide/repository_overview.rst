Repository overview
===================

atlast_sc package
-----------------
The ``atlast_sc`` directory contains all of the code and files that make up the
calculator Python package.

atlast_sc tests
---------------
Unit and functional tests for the ``atlast_sc`` package are contained in the
``atlast_sc_tests`` directory.

Web client
----------
The ``web_client`` directory contains all the web application files and scripts.
This directory also contains a ``Dockerfile`` that can be used to build a docker
image for running the web application inside a container.

Web client tests
----------------
Unit tests for the FastAPI application are located in the ``fastapi_tests`` directory.

GitHub actions
--------------
The ``.github`` directory contains a ``workflows`` directory where GitHub actions
configuration files are stored.

At present, linting, ``atlast_sc`` package testing, and testing of the FastAPI web
application are run as automated tasks using GitHub actions. Future work should
automate building and deploying the Python package and web application.

Developer utilities
-------------------
The ``dev_utils`` directory should be used for any files or scripts that may be
useful to developers.

It currently contains an input data ``yaml`` file and a Python script that uses
the ``atlast_sc`` package. Note that this script is intended for doing quick checks
or demonstrations of the calculator. If should not be used for testing
the application. Test scripts for the ``atlast_as`` package are located in
the ``atlast_sc_tests`` directory.

Documentation
-------------
The ``docs`` directory contains all the files and scripts used to generate (this)
documentation. The documentation is generated using Sphinx.

AM atmospheric modelling
------------------------
The ``am_code`` directory contains files and code that was used to generate a grid
of atmospheric parameters used by the calculator. This directory could be removed
from the repository.