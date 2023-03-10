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
