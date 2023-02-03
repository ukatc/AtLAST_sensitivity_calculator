![example workflow](https://github.com/ukatc/AtLAST_sensitivity_calculator/actions/workflows/backend-tests.yml/badge.svg)


Background
==========

In progress software to calculate either:

1. required exposure time for a given sensitivity 

2. the reverse, the sensitivity for a given exposure time.

To be packaged as a standalone python package (WIP).

A simple web interface is included, follow installation instructions below.

Testing is incomplete but initial tests can be run using ``make test``.

The [``benchmarking``](https://github.com/ukatc/AtLAST_sensitivity_calculator/blob/benchmarking/README.md) branch is a work-in-progress to test the results of the calculator matching the input and setup to JCMT. This exercise is incomplete. As it includes changes to the underlying code (the efficiency calculation), it should **not** be merged with ``main``. 
After validation of the calculator results and before publication of this package, the ``benchmarking`` branch can be deleted.


Using The Sensitivity Calculater
================================
Eventually this calculator will be hosted on a server and made available publicly.

For the time being it can be installed or downloaded from this repository.

Documentation on how to install and use the Sensitivity Calculater can be found
in the [``Installation Guide``](docs/source/installation.rst).


Guide for Developers
====================
Information on setting up your development environment, building, running, and deploying the application, running tests,
and generating the docs is provided in the [``Guide for Developers``](docs/source/guide_for_developers.rst).
