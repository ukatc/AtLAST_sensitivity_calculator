The Sensitivity Calculator can be initialized with your own input
values from a file. The :class:`FileHelper <atlast_sc.utils.FileHelper>` class can be used to
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
