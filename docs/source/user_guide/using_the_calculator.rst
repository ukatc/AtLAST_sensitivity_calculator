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
default values.

You may also initialize the calculator with your own input
values. This is described below.

Initializing the Calculator with a dictionary
*********************************************

The ``Calculator`` object accepts a ``dictionary`` as input. First, create a
dictionary with the input data you wish to use:

.. code-block:: python

    input_data = {
        't_int': {
            'value': 120,
            'unit': 's'
        },
        'sensitivity': {
            'value': 0,
            'unit': 'mJy'
        },
        'bandwidth': {
            'value': 7.5,
            'unit': 'GHz'
        },
        'obs_freq': {
            'value': 200,
            'unit': 'GHz'
        },
        'n_pol': {
            'value': 2
        },
        'weather': {
            'value': 25
        },
        'elevation': {
            'value': 25,
            'unit': 'deg'
        }
    }

All values must be numeric (integer or float). Units must be valid string
representations of
`astropy units <https://docs.astropy.org/en/stable/units/index.html>`__.

Next, create a new ``Calculator`` object, passing the ``input_data`` dictionary.

.. code-block:: python

    calculator = Calculator(input_data)

If any of the expected parameters are missing from ``input_data``, the calculator
will use the appropriate defaults.

Reading data from an input file
*******************************

The ``FileHelper`` class can be used to read data from a file and generate an
input data dictionary. (See :doc:`Input Files and Formats <input_files_formats>`
for more information on supported file formats and the required structure.)

First, import the file helper class:

.. code-block:: python

    from atlast_sc.utils import FileHelper


Next, call the ``read_from_file`` method, passing the directory and name of
the data file:

.. code-block:: python

    input_data = FileHelper.read_from_file('<directory>', '<file name>')


This returns a ``dictionary`` that can be used to initialize the ``Calculator``
object:

.. code-block:: python

    calculator = Calculator(input_data)

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