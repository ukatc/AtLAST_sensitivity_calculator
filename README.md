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
in the [``installation guide``](docs/source/installation.rst).


Guide for Developers
====================
Setting up your environment
---------------------------

1. Clone the repository:

   ```
   $ git clone https://github.com/ukatc/AtLAST_sensitivity_calculator.git
   ```

2. Create a conda environment:

   ```
   $ conda env create -f environment.yml
   ```
   
3. Activate the conda environment

   ```
   $ conda activate sens-calc
   ```



Running the web client
----------------------

1. Navigate to the `web_client` directory
2. Start a server with Flask (note: this may take a minute to load)

   ```
   $ flask run
   ```

4. Point your browser at http://127.0.0.1:5000/. You should now see the sensitivity calculator web client!


Generating the Documentation
-------------

To build the html version of the documentation:

1. Navigate to the [`docs`](docs/) directory.
2. Build the docs:

   ```
   $ make html
   ```

This will create the html and other resources in `docs/build/`.

Open the file `docs/build/html/index.html` in your browser to view the built documentation.