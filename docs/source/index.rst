
AtLAST Sensitivity Calculator
=============================

The Atacama Large Aperture Submillimeter Telescope (AtLAST) is a project to build a new 50m single-dish telescope to observe at sub-mm wavelengths that is currently in the design study phase. For further details on the project, see https://www.atlast.uio.no/.

The AtLAST Sensitivity Calculator can be used to calculate the required on source exposure time per pointing to achieve a given sensitivity or, conversely, the sensitivity obtained for a given exposure time. The sensitivity calculator is designed on our current best estimates for the telescope and instrument parameters, but these are likely to be refined as the project develops.

About the Sensitivity Calculator
--------------------------------

This chapter provides information on the inner workings of the calculator. :doc:`The sensitivity calculation <calculator_info/sensitivity>` describes the overriding equations for calculating the sensitivity. :doc:`Calculation inputs <calculator_info/calculation_inputs>` lists the calculator parameters (both the user inputs and those of the telescope) along with their default values and units. :doc:`Weather <calculator_info/weather>` describes the atmospheric model and how this is used in the equations. :doc:`Instrument overview <calculator_info/instrument_overview>` describes how we represent instruments in the calculator. There are then separate pages for each of the instruments with further details of the instrument and the equations specific to them.

.. toctree::
   :maxdepth: 3
   :caption: About the Sensitivity Calculator

   calculator_info/sensitivity
   calculator_info/calculation_inputs
   calculator_info/weather
   calculator_info/instrument_overview


Installation
--------------------

This chapter provides information on :doc:`installing the calculator <user_guide/python_package_installation>` as a Python package.

.. toctree::
   :maxdepth: 3
   :caption: Installation

   user_guide/python_package_installation


User Guide
----------
This chapter describes how to use the calculator as a Python package in :doc:`using the Calculator <user_guide/usage>`. :doc:`Input and output files <user_guide/input_and_output_files>` provides information on how files can be used to input data into the calculator, the format they need to be in and how to export the results as a file. The calculator can also be run as a web client. Instructions for setting this up locally are given in :doc:`running the web client <user_guide/running_the_web_client>`.


.. toctree::
   :maxdepth: 3
   :caption: User Guide

   user_guide/usage
   user_guide/input_and_output_files
   user_guide/running_the_web_client

Developer Guide
---------------
This chapter is for the benefit of future developers of the software. It starts with an overview of the inner workings of the :doc:`application <developer_guide/application_overview>` and structure of the :doc:`repository <developer_guide/repository_overview>`. :doc:`Developing the application <developer_guide/developing_the_application>` provides information on setting up and maintaining the various parts of the application. Instructions are also provided on how to :doc:`add a new instrument <developer_guide/adding_new_instrument>` to the application.

.. toctree::
   :maxdepth: 3
   :caption: Developer Guide

   developer_guide/application_overview
   developer_guide/repository_overview
   developer_guide/developing_the_application
   developer_guide/adding_new_instrument

Code Documentation
------------------
This chapter details the :doc:`application programming interface (API) <code_docs/public_api>` for the software and :doc:`unified modelling language (UML) diagrams <code_docs/uml>` to illustrate the connections between the different modules.

.. toctree::
   :maxdepth: 1
   :caption: Code Documentation
   
   code_docs/public_api
   code_docs/uml
   code_docs/openapi

