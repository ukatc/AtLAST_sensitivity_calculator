Application overview
====================
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

calculator_factory
++++++++++++++++++
This module creates a calculator instance according to user input that has been specified. 

calculator
++++++++++
This module contains the main ``Calculator`` class that provides the interface
for performing sensitivity and integration time calculations. A ``Calculator``
object may be instantiated with default parameter setup object, or by passing
user input parameters as arguments to the parameter setup object constructor.

This module provides methods exclusively for calculating sensitivity and integration time.
It retrieves parameter sets —including user inputs, telescope and environmental 
conditions, and derived parameters— through the parameter setup object. This design 
simplifies the process for users by providing a unified interface to access information 
from each parameter class.

parameter_setup
+++++++++++++++
This class serves as a centralised container for all parameter classes. When a parameter is 
updated in its respective class, the new value can be retrieved through this class. It 
provides access to all models used in calculations and methods for operations related to 
identifying applicable instruments. The class also stores a copy of the
parameters used to initialize the calculator, allowing the user to revert to
the initial state.

data
++++
The ``Data`` class stores all of the configuration information for each of the user input, 
telescope and environment parameters used by the calculator (default values, default units, etc.), 
and calculated parameters.

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
This module contains classes that logically group derived parameters used by
the calculator. Derived parameters are those that are dependent on the data
provided to the calculator (user input and telescope and environment). They are 
calculated at runtime when the calculator is instantiated, and when any of the 
independent parameters are updated.

The derived group classes are ``AtmosphereParams``, ``Efficiencies``, and
``Temperatures``. Although these classes are accessible via the public API, they
are primarily intended to be used internal to the calculator.

exceptions
++++++++++
This module contains the data validation exception and warning classes.

utils
+++++
This is a utility module that contains classes and methods used throughout the application.

Class Structure
^^^^^^^^^^^^^^^
General class structure can be visualised with the UML diagrams below.

The below diagram shows how each of the parameter classes depend on each other and how the 
ParameterSetup class acts as the container for the current state of each parameter class.

.. image:: imgs/parameter_classes.png
    :alt: Diagram of parameter classes that make up the calculation process
    :align: center

Integration Overview
--------------------
The overall calculation process is kickstarted with a creation of a Calculator object using the
Calculator class. Initially, the calculator is created with default values. If the calculator 
is used via the Python CLI, any of the user input parameters can be changed before calculating 
the sensitivity/integration time. If they don't, the calculations will be done with default 
values. In the UI, the first calculation is done with the default values and any specified user
input parameters will be considered within the calculations once the user clicks the "Calculate" 
button. 

The application will choose an instrument to use specific equations when calculating 
sensitivity/integration time according to the user input parameters. The user can also change
the chosen instrument manually. Currently, only the CLI users are able to choose a specific 
instrument to use in their calculations. For more details about the instrument selection 
process refer to the :ref:`Instrument Selection <instrument selection>` section.

Once the instrument has been selected by the appropriate method, the calculator will use any 
instrument specific equations or parameters -where available- to calculate sensitivity/integration 
time. These instrument specific equations or parameters would have been defined within the
relative instrument YAML files and classes. 

.. _instrument selection:

Instrument Selection
--------------------
Instrument selection on the UI is executed in the background when the user inputs observing 
frequency and bandwidth values in the boxes specified and clicks the "Calculate" button. The
calculator retrieves the observing frequency and bandwidth entered by the user and verifies 
them against the supported ranges for each instrument and chooses the applicable instrument.
In the case where the user input parameters correspond to more than one instrument, the 
calculator will choose the first applicable instrument. If there are no applicable instruments,
the calculator will proceed with the Default instrument. 

However, on the CLI, the user can make an instrument selection. This selection should be 
executed in a specific order in relation to other parameter assignments. Any user input 
parameter should be specified before selecting an instrument. For example, if the user 
wants to set a specific observing frequency to do calculations and also select an instrument, 
they have to make sure that the observing frequency they are specifying falls into the
observing frequency ranges of the instrument they want to select. They should also take
care to do the same with the bandwidth values. In the case where the user attempts to 
select an instrument before specifying the appropriate observing frequency and bandwidthv
values, the calculator will throw an error. 

The applicable observing frequency and bandwidth ranges for each instrument along with some
other information can be accessed by listing the instruments on the CLI. 

Adding a new instrument
^^^^^^^^^^^^^^^^^^^^^^^

Creating the instrument YAML file
+++++++++++++++++++++++++++++++++
If an instrument needs to be added, this should be done by executing a couple of steps
within the *atlast_sc/instruments* directory.

Firstly, a YAML file with the name of the instrument should be creating in the 
sub-directory called *data*. It should include details of the instrument in the 
following format: 

.. code-block:: yaml

    name: "Example"
    allowed_ranges:
        observing_frequency:
            ranges: [(500.0-600.0),(700.0-800.0)]
            unit: GHz
        bandwidth: 
            ranges: [(10.9e4-1.8e8)]
            unit: Hz
    receiver_temperature: 
        values: [30.0,40.0]
        unit: K

Any other instrument specific parameter should be added following the same format. The
Default instrument YAML file could be taken as a template and the other instrument 
YAML files could be taken as example on how these files could be customised. 

Creating the instrument Python module
+++++++++++++++++++++++++++++++++++++
Secondly, a Python module should be created in the *classes* sub-directory with the 
new instrument name. Following the example above, the name of the module file should 
be "Example.py" and it should include the following class format: 

.. code-block:: python 

    """
    Example instrument parameters
    """        
    class Example(Instrument):
        def __init__(self, data):
            super().__init__(data)

For more detail on how to construct the module, the Default instrument Python module
could be taken as an example and other instrument Python modules could be taken as
example on how these modules could be customised. 

Modifying the configuration file to add the new instrument
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Thirdly, a couple of lines should be modified in ``config.py`` where they are 
indicated within the configuration file with comments. In the initilisation 
method, a dictionary containing pointers to the new instrument's Python module 
and YAML file name should be added in similar format to the existing instruments. 
After creating the dictionary variable for the new instrument, it should be added 
to the ``available_instruments`` list.

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