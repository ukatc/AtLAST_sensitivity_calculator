Application overview
====================
The sensitivity calculator consists of the calculator itself (a Python package) and a web application view of the calculator.
An overview of each component is provided below.

The overall calculation process begins with the creation of a Calculator object using
user specified input parameters, where if not specified, the calculator is initialised with default
user input values. If the calculator is used via the Python command line interface (CLI), any of the user input
parameters can be changed before calculating the sensitivity/integration time. If the parameters are not changed, 
the calculations will be done with default values. In the web user interface (UI), the first calculation is done 
with the default values and any specified user input parameters will be considered within the calculations once 
the user clicks the "Calculate" button.

Given the input parameters, the application will choose instrument specific equations for calculating
sensitivity/integration. The user can override instrument choice manually as described in the user guide
(see :ref:`Instrument Selection <instrument selection>` section). Currently, only the CLI users are
able to choose a specific instrument to use in their calculations.



.. TODO::

    **ILGIN TO FOLLOW-UP**

    Based on the comments about removing the free-floating Python files (ASC-127), I assume this section will need
    a lot of revision?

    Could this also be moved to become part of the :doc:`Repository Overview <repository_overview>`, since the first
    section of the repository overview is the ``atlast_sc`` section?

    What happened to the repository/directory structure I saw as part of ASC-88? (see our comment discussion
    on 17 Feb in that ticket)

The calculator
--------------

The ``atlast_sc`` Python package contains the code that performs the sensitivity and
integration time calculations. It additionally configures
default and allowed values and units for the parameters used by the calculator,
and performs validation on data provided to the calculator. It
also provides utility tools for reading input data from a file and writing output
to file.

The following documentation describes the contents of the python package,
information on using the Python package is provided :doc:`through this link to the user guide <../user_guide/using_the_calculator>`.

Modules
^^^^^^^
Below is an overview description of each of the modules included in the
``atlast_sc`` package. More detailed information on parameters and relationships is provided in the
:doc:`Public API <../code_docs/public_api>` and :doc:`UML diagrams <../code_docs/uml>`
sections.

calculator
++++++++++
This module contains the main ``Calculator`` class that provides the interface
for performing sensitivity and integration time calculations. A ``Calculator``
object may be instantiated with user input parameters constructor, or with the default
user input parameter constructor.

This module provides methods exclusively for calculating sensitivity and integration time.
It retrieves parameter sets, including user inputs, telescope and environmental
conditions, and derived parameters, through the parameter setup object. This design
simplifies the process for users by providing a unified interface to access information 
from each parameter class.


parameter_setup
+++++++++++++++
This class serves as a centralised container for storing and accessing the values of each 
parameter in the following parameter classes:
- user input parameters
- telescope and environment parameters
- derived parameters

When a parameter is updated in its respective class, the new value of the parameter 
can be retrieved through this class. It provides access to all models used in 
calculations and methods for operations related to identifying applicable instruments. 
This class also stores a copy of the parameter values used to initialize the calculator, 
allowing the user to revert to the initial state.


data
++++
The ``Data`` class stores all of the configuration information for each of the user input, 
telescope and environment parameters and subsequently derived parameters used in and by the calculator.

The ``Validator`` class provides methods for validating data provided to the calculator.



models
++++++
This module contains model definitions that describe the structure of the data
provided to the calculator. The module uses the ``pydantic`` library; models
within the module inherit from the pydantic ``BaseModel``. Custom validation methods
within the models ensure that input data is of the right type and satisfies the
constraints defined in the ``data.Data`` class.

derived_groups
++++++++++++++
This module contains classes that logically group parameters derived by the calculator
for use in the calculations. Derived parameters are those that are dependent on the data
provided to the calculator (user input and telescope and environmental properties). They are
calculated at runtime when the calculator is instantiated, and when any of the 
independent parameters are updated.

The derived group classes are ``AtmosphereParams``, ``Efficiencies``, and
``Temperatures``. Although these classes are accessible via the public API, they
are primarily intended to be used internally.

exceptions
++++++++++
This module contains the data validation exception and warning classes so that the user is informed
about why their setup cannot generate a valid output.

utils
+++++
This is a utility module that contains classes and methods used throughout the application. 
The contents include helper methods for validating and updating parameters, performing 
unit conversions, and file input/output methods for reading and writing data to file.


Class Structure
^^^^^^^^^^^^^^^
General class structure can be visualised with the UML diagrams below.

.. image:: imgs/calculator_class.png
    :alt: Diagram of relation between Calculator and CalculatorFactory class
    :align: center

The diagram above shows how the ``CalculatorFactory`` class has the ``Calculator`` class as a dependency.
The diagram below shows how each of the parameter classes depend on each other and how the
ParameterSetup class acts as the container for the current state of each parameter class.

.. image:: imgs/parameter_classes.png
    :alt: Diagram of parameter classes that make up the calculation process
    :align: center



.. _instrument selection:

Instrument Selection
--------------------
Instrument selection in both the python and web interfaces is executed in the background
when the user inputs observing frequency and bandwidth values in the boxes specified and
clicks the "Calculate" button, and validates the instrument choice against its operational ranges.
In the case where the user input parameters correspond to more than one instrument, the 
calculator will choose the first applicable instrument. If there are no applicable instruments,
the calculator will proceed with the Default instrument. 

On the CLI, the user can override an instrument selection. Because of the internal validation, user input
observing frequency and bandwidth should be specified before selecting an instrument or overriding default selections.
In the case where the user attempts to
select an instrument before specifying the appropriate observing frequency and bandwidth
values, the calculator will return a validation error.

The applicable observing frequency and bandwidth ranges for each instrument along with some
other information about the instruments can be accessed by listing the instruments on the CLI via
``calculator.list_instruments``.

Adding a New Instrument
----------------------------------------
The application is constructued in a specific way that allows new instruments to be added to the
calculation process. When an instrument needs to be added to the calculator, a couple of steps 
need to be executed within the *atlast_sc/instruments* directory. The process is detailed in the
:doc:`Developing the Application <./developing_the_application>` section of the developer guide. 

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
