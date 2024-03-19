![example workflow](https://github.com/ukatc/AtLAST_sensitivity_calculator/actions/workflows/lint-test.yml/badge.svg)


Background
==========

The Atacama Large Aperture Submillimeter Telescope (AtLAST) is a project to build a new 50m single-dish telescope to observe at sub-mm wavelengths that is currently in the design study phase. For further details on the project, see https://www.atlast.uio.no/.

The AtLast Sensitivity Calculator can be used to calculate the required
on source exposure time per pointing to achieve a given sensitivity or, conversely, the sensitivity
obtained for a given exposure time. The sensitivity calculator is designed on our current best estimates for the telescope and instrument parameters, but these are likely to be refined as the project develops.

Using the Sensitivity Calculator
================================
The calculator is available as both a web-based application and as a Python 
package. The web client is available here: https://senscalc.atlast.uio.no/.

Both the web client and Python package can be installed or
downloaded from this repository.

Documentation on how to install the Sensitivity Calculator Python package can be found
in the [``Python Package Installation Guide``](docs/source/user_guide/python_package_installation.rst). Information
on using the Python package is provided in the [``Using the Calculator guide``](docs/source/user_guide/using_the_calculator.rst).

See [``Running the Web Client``](docs/source/user_guide/running_the_web_client.rst) for instructions on
setting up the Sensitivity Calculator web application.

All the documentation is also available on Readthedocs: https://atlast-sensitivity-calculator.readthedocs.io/.

Guide for Developers
====================
Information on setting up your development environment, building, running, and deploying the application, running tests,
and generating the docs is provided in the [``Developing the application guide``](docs/source/developer_guide/developing_the_application.rst).

An overview of the application is provided [``here``](docs/source/developer_guide/application_overview.rst).

Information about the structure of the repository can be found [``here``](docs/source/developer_guide/repository_overview.rst).


Funding Acknowledgement
===============================

This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 951815
