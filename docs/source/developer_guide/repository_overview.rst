Repository overview
===================

| **AtLAST_sensivity_calculator**
| ├── .github
| ├── am_code 
| ├── atlast_sc
| │   ├── ...
| ├── atlast_sc_tests
| │   ├── ...
| ├── dev_utils
| ├── docs
| │   ├── ...
| ├── fastapi_tests
| ├── web_client
| │   ├── ...
| ├── HISTORY.rst
| ├── LICENSE
| ├── makefile
| ├── README.md
| └── environment.yml
| 

GitHub actions
--------------
The ``.github`` directory contains a ``workflows`` directory where GitHub actions
configuration files are stored.

At present, linting, ``atlast_sc`` package testing, and testing of the FastAPI web
application are run as automated tasks using GitHub actions. Future work should
automate building and deploying the Python package and web application.

am_code
-------
| ├── **am_code**
| │   ├── configs
| │   └── output
| 

The ``am_code`` directory contains AM atmospheric modelling files and code that was 
used to generate a grid of atmospheric parameters used by the calculator. This 
directory could be removed from the repository.

atlast_sc package
-----------------
| ├── **atlast_sc**
| │   ├── instruments
| │       ├── classes
| │       ├── data
| │   ├── parameters
| │   └── static/lookups
| 

The ``atlast_sc`` directory contains all of the code and files that make up the
calculator Python package.

instruments
###########
Contains instrument data files and their respective Python classes, as well as the
configuration file to set each instrument up.

parameters
##########
Classes for each of the calculation parameter category.

static/lookups
##############
Tabular information files for parameters sky temperature (`T_atm`) and transmittance
(`tau_atm`).

atlast_sc tests
---------------
| ├── **atlast_sc_tests**
| │   ├── functional_tests
| │   └── unit_tests
| 

Unit and functional tests for the ``atlast_sc`` package are contained in the
``atlast_sc_tests`` directory.

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
| ├── **docs**
| │   ├── source
| 

| ├── **source**
| │  ├── calculator_info
| │  ├── code_docs
| │  ├── developer_guide
| │  ├── user_guide
| 

The ``docs`` directory contains all the files and scripts used to generate (this)
documentation. The documentation is generated using Sphinx.

Web client
----------
| ├── **web_client**
| │   ├── scripts
| │   ├── static
| │   ├── templates
| 

The ``web_client`` directory contains all the web application files and scripts.
This directory also contains a ``Dockerfile`` that can be used to build a docker
image for running the web application inside a container.

Web client tests
----------------
Unit tests for the FastAPI application are located in the ``fastapi_tests`` directory.

Changes from calculator v1.0
----------------------------
- Refactored the codebase to have a more modular structure for the calculation process. In the
  previous version, the code was structured in a singular streamlined process that made it difficult
  to modify the calculation process. The new structure allows for better organisation of the
  code and makes it easier to add new instruments or to modify the calculation process in the
  future. These changes include separating the calculation input parameters into different classes 
  based on their category, and introducing instrument modules where instrument data and methods are 
  stored (see :ref:`Class Structure <class structure>` for high level view of the new structure).

- Introduced instrument modules where instrument data and methods are stored. The users can 
  select the instrument they want to use and the relevant data and methods for that instrument 
  will be used in the calculations (see section  in :ref:`Instrument Selection <instrument selection>`
  for more details.). This is a significant change from the previous version where
  all of the data and methods for a generic heterodyne instrument were stored in a single module. 
  This new structure makes it easier to add new instruments in the future (see section in 
  :ref:`Add a New Instrument <add new instrument>`).

.. .. TODO::

..     **ILGIN TO FOLLOW-UP**

..     This section needs to be significantly longer. You've refactored the entire code,
..     added the ability to use units, included instrument modules and (will eventually) update
..     the web ui as well.  All of that needs to be captured.   ASC-118 