Application overview
====================
The sensitivity calculator consists of the calculator itself (a Python package) and a web application view of the calculator.
An overview of each component is provided below.

The overall calculation process begins with the creation of a Calculator object using
CalculatorFactory, where the calculator is initialised with default values. If the calculator
is used via the Python command line interface (CLI), any of the user input parameters can be changed before calculating
the sensitivity/integration time. If the parameters are not changed, the calculations will be done with default
values. In the web user interface (UI), the first calculation is done with the default values and any specified user
input parameters will be considered within the calculations once the user clicks the "Calculate" button.

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

calculator_factory
++++++++++++++++++
This module creates a calculator instance according to user input that has been specified.

.. TODO::

    **ILGIN TO FOLLOW-UP**

    Please give a description here of what a python factory is, they're not often used in astronomy packages
    (in a way that astronomers see). This could form part of the work for ASC-137


calculator
++++++++++
This module contains the main ``Calculator`` class that provides the interface
for performing sensitivity and integration time calculations. A ``Calculator``
object may be instantiated with default parameter setup object, or by passing
user input parameters as arguments to the parameter setup object constructor.

This module provides methods exclusively for calculating sensitivity and integration time.
It retrieves parameter sets, including user inputs, telescope and environmental
conditions, and derived parameters, through the parameter setup object. This design
simplifies the process for users by providing a unified interface to access information 
from each parameter class.

.. TODO::

    **ILGIN TO FOLLOW-UP**

    Please describe why users (yes, I know this is the developer guide) need to use the factory,
    and not just ``calculator`` directly


parameter_setup
+++++++++++++++
This class serves as a centralised container for all parameter classes. When a parameter is 
updated in its respective class, the new value can be retrieved through this class. It 
provides access to all models used in calculations and methods for operations related to 
identifying applicable instruments. The class also stores a copy of the
parameters used to initialize the calculator, allowing the user to revert to
the initial state.

.. TODO::

    **ILGIN TO FOLLOW-UP**

    I found the first 2 sentences above hard to follow, and I'm still not sure I understand. what's 'this class' at the
    end of the 2nd sentence? I think the word (used 4 times in 2 sentences) somewhat lost its meaning. is ``parameter_setup``
    a class of classes?

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

.. TODO::

    **ILGIN TO FOLLOW-UP**

    Such as.... (validation checkers, file IO, and unit conversions (via astropy))

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
Instrument selection in both the python and web interafacesis executed in the background
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
.. TODO::

    **ILGIN TO FOLLOW-UP**

    I've bumped up the level of the 'adding a new instrument' heading.
    There needs to be a paragraph here explaining the workflow before getting into the specifics of the
    kinds of files to be created and where to put them:

    - What equation are they slotting into
    - What kinds of files are needed
    - What other modifications do the developers need to make, and where (yes, ``config.py``, but also the documentation)
    - does the user have to do anything to the web-UI to make their instrument locally visible? what process do they need to follow to have their instrument visible on the Oslo hosted site?

    I have re-opened ASC-114 to track this work

    I would also suggest to re-order these sub-sections to show the python module first, since it's arguably
    more important / the bulk of the work to be done.

    Related to that last point, is there a reason the 'adding a module' instructions are in the ``application_overview``
    section/document rather than the ``developing_the_application`` section/document? I think it might fit better there


Creating the instrument YAML file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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

.. TODO::

    **ILGIN TO FOLLOW-UP**

    We talked about putting a more functional example in here, and I still think that would be
    useful.  Maybe including a stripped down version of the 'default' module, and pointing
    to the included instrument classes for further examples?

    - Heterodynes (FINER, SEPIA, CHAI)
    - Continuum/LEKID (MUSCAT)
    - IFU/MKID (TIFUUN)

Modifying the configuration file to add the new instrument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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