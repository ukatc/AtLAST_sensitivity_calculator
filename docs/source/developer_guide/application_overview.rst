Overview
========
The sensitivity calculator consists of a Python package and a web application.
An overview of each component is provided below.

The calculator
--------------

The ``atlast_sc`` Python package contains the code that performs the sensitivity and
integration time calculations, configures
default and allowed values and units for the parameters used by the calculator,
and performs validation on data provided to the calculator. It
also provides utility tools for reading input data from a file and writing output
to file.

Information on using the Python package is provided :doc:`here <../user_guide/using_the_calculator>`.

Modules
^^^^^^^
Below is an overview description of each of the modules included in the
``atlast_sc`` package. More detailed information is provided in the
:doc:`Public API <../code_docs/public_api>` and :doc:`UML diagrams <../code_docs/uml>`
sections.

calculator
++++++++++
This module contains the main ``Calculator`` class that provides the interface
for performing sensitivity and integration time calculations. A ``Calculator``
object may be instantiated with default user input parameters, or by passing
one or more parameters as arguments to the constructor.

.. note::
    The ``Calculator`` may also be instantiated with user-defined instrument
    setup parameters. However, this is not intended to be standard functionality
    and could or should be removed. Note that the functionality has not been
    tested and so is not guaranteed to work.

This module also contains the ``Config`` class, which stores the calculation
inputs (user input and instrument setup). The class also stores a copy of the
parameters used to initialize the calculator, allowing the user to revert to
the initial state.

data
++++
The ``Data`` class stores all of the configuration information for each of the user input
and instrument setup parameters used by the calculator (default values, default units, etc.).

The ``Validator`` class provides methods for validating data provided to the calculator.

models
++++++
This module contains model definitions that describe the structure of the data
provided to the calculator. The module uses the ``pydantic`` library; models
within the module inherit from the pydantic ``BaseModel``. Custom validation methods
within the models ensures that input data is of the right type and satisfies the
constraints defined in the ``data.Data`` class.

derived_groups
++++++++++++++
This module contains classes that logically group derived parameters used by
the calculator. Derived parameters are those that are dependent on the data
provided to the calculator (user input and instrument setup). They are calculated
at runtime when the calculator is instantiated, and when any of the independent
parameters are updated.

The derived group classes are ``AtmosphereParams``, ``Efficiencies``, and
``Temperatures``. Although these classes are accessible via the public API, they
are primarily intended to be used internal to the calculator.

exceptions
++++++++++
This module contains the data validation exception and warning classes.

utils
+++++
A utility module containing classes and methods used throughout the application.

The web application
-------------------
The web client consists of a backend based on the `FastAPI web framework <https://fastapi.tiangolo.com/lo/>`__,
a standard, browser-based HTML/CSS/JavaScript frontend, and a REST API.

The FastAPI application renders the frontend using
the `Jinja templating engine <https://jinja.palletsprojects.com/en/3.1.x/>`__.

FastAPI also auto-generates an OpenAPI schema that can be used to render interactive,
browser-based documentation of the REST API. The documentation can be accessed via the following two URLs:

- ``<app_url>/docs`` to render with Swagger UI
- ``<app_url>/redoc`` to render with Redoc

where ``<app_url>`` is the root URL of the application (e.g., ``localhost:8000``).