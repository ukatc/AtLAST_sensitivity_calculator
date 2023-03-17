Using the Calculator
--------------------

Basic usage
^^^^^^^^^^^
First, import the :class:`Calculator <atlast_sc.calculator.Calculator>` class from
the :mod:`atlast_sc.calculator` module:

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

.. note::

    All input parameters are validated by the calculator. You will see
    an error if the values you provide are invalid (e.g., are out of a specified
    range or have invalid units).

.. TODO: provide details of which parameters can be manually changed, and what
    their valid values and units are.**

Call the :meth:`calculate_sensitivity <atlast_sc.calculator.Calculator.calculate_sensitivity>`
method to obtain the sensitivity (in Jansky):

.. code-block:: python

    calculated_sensitivity = calculator.calculate_sensitivity()

You can also specify an integration time to perform the sensitivity calculation:

.. code-block:: python

    t_int = 150*u.s
    calculated_sensitivity = calculator.calculate_sensitivity(t_int)


Conversely, to obtain the integration time required (in seconds), call
:meth:`calculate_t_integration <atlast_sc.calculator.Calculator.calculate_t_integration>`:

.. code-block:: python

    calculated_t_int = calculator.calculate_t_integration()

You can also specify a sensitivity to perform the integration time calculation:

.. code-block:: python

    sens = 10*u.mJy
    calculated_t_int = calculator.calculate_t_integration(sens)


.. note::

    When the sensitivity or integration time calculations are performed,
    the corresponding parameters stored in the Calculator object are updated by default.
    To prevent this behaviour, set the ``update_calculator`` parameter to ``False``, as shown below:

    .. code-block:: python

        calculated_t_int = calculator.calculate_t_integration(update_calculator=False)

    You can then manually update the calculator with the new value:

    .. code-block:: python

        calculator.t_int = calculated_t_int


Resetting the calculator
^^^^^^^^^^^^^^^^^^^^^^^^

You can reset the parameters stored in the calculator to their initial values
using the :meth:`reset <atlast_sc.calculator.Calculator.reset>` method:

.. code-block:: python

        # initialize the calculator with its default values
        calculator = Calculator()

        # change the value of one of the parameters
        calculator.bandwidth = 150*u.MHz

        # reset the calculator
        calculator.reset()

        # check the bandwidth value stored in the calculator
        print('bandwidth', calculator.bandwidth)
        # expected output
        # bandwidth 100.0 MHz


Providing input data to the calculator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: providing_input_data.rst

Writing parameters to file
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: writing_parameters_to_file.rst
