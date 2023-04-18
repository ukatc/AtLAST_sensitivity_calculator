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

Next, initialize the calculator as follows.

.. code-block:: python

    calculator = Calculator()

.. note::

    The Sensitivity Calculator is pre-configured with default values for all
    user input parameters. See :doc:`here <../calculator_info/user_input>` for
    information on the calculation input parameters and their default values.

    You may also initialize the calculator with your own
    input values. This is described in the section :ref:`input data`.


All input parameters can be updated manually. For example, to
set the bandwidth after initializing the calculator:

.. code-block:: python

    calculator.bandwidth = 10*u.GHz

.. note::

    All input parameters are validated by the calculator. You will see
    an error if the values you provide are invalid (e.g., are out of a specified
    range or have invalid units).

Call the :meth:`calculate_sensitivity <atlast_sc.calculator.Calculator.calculate_sensitivity>`
method to obtain the sensitivity (in mJy):

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


.. warning::

    If any of the parameters stored in the Calculator object are updated, the
    sensitivity or integration time will *not* be recalculated automatically.


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


Checking the parameters stored by the calculator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The calculator stores the user input parameters, instrument setup parameters, and
derived parameters that are calculated from other inputs. You can output these
parameters to the console as follows:

.. code-block:: bash

    # Check the user input parameters
    >>> print(calculator.user_input)
    t_int: 100 s
    sensitivity: 3 mJy
    bandwidth: 100 MHz
    obs_freq: 100 GHz
    n_pol: 2
    weather: 25
    elevation: 45 deg

    # Check the instrument setup parameters
    >>> print(calculator.instrument_setup)
    g: 1
    surface_rms: 25 micron
    dish_radius: 25 m
    T_amb: 270 K
    eta_eff: 0.8
    eta_ill: 0.8
    eta_spill: 0.95
    eta_block: 0.94
    eta_pol: 0.99
    eta_r: 1

    # Check the derived parameters
    >>> print(calculator.derived_parameters)
    tau_atm: 0.0276204
    T_atm: 7.7576 K
    T_rx: 23.9962 K
    eta_a: 0.699532
    eta_s: 0.99
    T_sys: 206.499 K
    sefd: 4.15139e-24 J / m2
    area: 1963.5 m2

.. _input data:

Providing input data to the calculator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: providing_input_data.rst

Writing parameters to file
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: writing_parameters_to_file.rst
