The Sensitivity Calculator can be initialized with your own input
values. This is described in the sections that follow.

See :doc:`User input <../calculator_info/user_input>` for
more information on the calculation input parameters.

Initializing the Calculator with a dictionary
*********************************************

The :class:`Calculator <atlast_sc.calculator.Calculator>` object accepts a dictionary as input.
First, create a dictionary with the input data you wish to use:

.. code-block:: python

    input_data = {
        't_int': {'value': 120, 'unit': 's'},
        'sensitivity': {'value': 0.01, 'unit': 'mJy'},
        'bandwidth': {'value': 7.5, 'unit': 'GHz'},
        'obs_freq': {'value': 200, 'unit': 'GHz'},
        'n_pol': {'value': 2},
        'weather': {'value': 25},
        'elevation': {'value': 25, 'unit': 'deg'}
    }

Next, create a new Calculator object, passing the ``input_data`` dictionary.

.. code-block:: python

    calculator = Calculator(input_data)

All values must be numeric (integer or float), and units (when required) must be presented as `astropy units <https://docs.astropy.org/en/stable/units/index.html>`__.
The Calculator will throw an error if any of the input parameter names are incorrect. If any of the
parameters have not been manually set via the input data dictionary, the calculator will use the
appropriate default values and units.


Reading data from an input file
*******************************

The :class:`FileHelper <atlast_sc.utils.FileHelper>` class can be used to
read data from a file and generate an input data dictionary.

First, import the file helper class from the :mod:`utils <atlast_sc.utils>` module:

.. code-block:: python

    from atlast_sc.utils import FileHelper


Next, call :meth:`read_from_file <atlast_sc.utils.FileHelper.read_from_file>`,
passing the directory (provide an absolute path, or a path relative to
directory in which your Python script is running) and the name of the data file:

.. code-block:: python

    input_data = FileHelper.read_from_file('<directory>', '<file name>')


This returns a dictionary that can be used to initialize the Calculator
object:

.. code-block:: python

    calculator = Calculator(input_data)
