Python Package Usage
====================

The Sensitivity Calculator may be used as a standalone package in your
Python code. See the :doc:`Installation Guide <installation>` for information
on setting up an isolated environment for your work and installing the
Sensitivity Calculator package.


See the Installation See the Public API documentation <TODO: link to doc> for more details.

Using the Calculator
--------------------

Basic usage
^^^^^^^^^^^
First, import the Python package:

.. code-block:: python

    from atlast_sc.calculator import Calculator

You may also find it useful to import astropy units:

.. code-block:: python

    import astropy.units as u

Next, initialize the calculator with its default values (see below for
information on initializing the calculator with your own input values).

.. code-block:: python

    calculator = Calculator()


A number of calculator parameters can be updated manually. For example, to
set the bandwidth after initializing the calculator:

.. code-block:: python

    calculator.bandwidth = 10*u.GHz

**NOTE**: All input parameters are validated by the calculator. You will see
an error if the values you provide are not invalid (e.g., are out of a specified
range or have invalid units).

**TODO: provide details of which parameters can be manually changed, and what
their valid values and units are.**

To obtain the sensitivity (in Jansky) for a given integration time:

.. code-block:: python

    calculated_sensitivity = calculator.calculate_sensitivity(calculator.t_int)

Conversely, to obtain the integration time required (in seconds) for a given sensitivity:

.. code-block:: python

    calculated_t_int = calculator.calculate_t_integration(calculator.sensitivity)


Providing input data to the calculator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The Sensitivity Calculator is pre-configured with default values for all
input parameters.
See <TODO: link to doc> for more information on the input parameters and their
default values. You may also initialize the calculator with your own input
values.

**TODO: describe how to do that**

Writing parameters to file
^^^^^^^^^^^^^^^^^^^^^^^^^^

**TODO: describe how to do that**

Running the demo
----------------
**TODO: remove this section and provide either static tutorial pages, or
interactive notebooks**

If you have cloned the GitHub repository, you can use the ``run.py`` script in the ``demo`` directory to
play with and learn how the calculator works.

Development of this demo is currently a work in progress. For now, the demo can be run by navigating to the root
directory of the repository and running the following:

.. code-block:: python

    python -m demo.run