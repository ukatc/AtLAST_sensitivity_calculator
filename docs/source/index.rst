
AtLAST Sensitivity Calculator
=============================

The AtLAST Sensitivity Calculator can be used to calculate the required
exposure time to achieve a given sensitivity or, conversely, the sensitivity
obtained for a given exposure time.

About the Sensitivity Calculator
--------------------------------

.. TODO::

    **MARK TO FOLLOW-UP**

    The second paragraph here probably needs its references updated because of the re-structure

    This section (before moving into the sensitivity calculation) should also give an 'abstract' style
    summary of what to expect in the rest of this chapter. (i.e. main calc used, what this can produce
    and what families of instruments are included in this version of the calculator)1


The sensitivity calculator presented here will calculate either the sensitivity of the telescope, given an input on-source integration time, or the on-source integration time required to achieve the requested sensitivity.

More information on the calculation done within the sensitivity calculator can be found in section 2.1. A description of the parameters used as input for these calculations is is presented in section 2.2, which also shows which telescope properties are derived from those user inputs. An overview of how to use the weather package *am* can be found in section 2.3

.. toctree::
   :maxdepth: 3
   :caption: About the Sensitivity Calculator

   calculator_info/sensitivity
   calculator_info/calculation_inputs
   calculator_info/weather
   calculator_info/instrument_overview


Installation
--------------------

.. toctree::
   :maxdepth: 3
   :caption: Installation

   user_guide/python_package_installation


User Guide
----------
The calculator is available both as a web-based application and as a stand-alone
Python package.

The :doc:`Installation Guide <user_guide/python_package_installation>` provides
detailed instructions on how to install the Python
package.

See :doc:`Using the Calculator <user_guide/usage>` for information
on how to integrate the calculator into your Python code.

For information on running the web client, see
:doc:`Running the Web Client <user_guide/running_the_web_client>`.

Sections 2.4 and 2.5 talk about how to install and run the python version of the calculator, with section 2.6 describing the formatting of the input files that will work with the command line or python version of the calculator. Section 2.7 describes using the web front-end.


.. toctree::
   :maxdepth: 3
   :caption: User Guide

   user_guide/usage
   user_guide/input_and_output_files
   user_guide/running_the_web_client

Developer Guide
---------------
Sections 2.8 through to 2.13 describe in more detail how the package was constructed, tested, how the front and back end components interact with each other, and how the code can be extended by developers.

.. toctree::
   :maxdepth: 3
   :caption: Developer Guide

   developer_guide/application_overview
   developer_guide/repository_overview
   developer_guide/developing_the_application
   developer_guide/adding_new_instrument

Code Documentation
------------------
.. toctree::
   :maxdepth: 1
   :caption: Code Documentation

   code_docs/public_api
   code_docs/uml
   code_docs/openapi

