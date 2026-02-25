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

    calculator.bandwidth = 150*u.MHz

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

    When the sensitivity or integration time calculations are performed, by default,
    the calculated values are stored in the Calculator object. Similarly, an
    integration time passed to ``calculate_sensitivity`` or sensitivity passed
    to ``calculate_t_integration`` are stored by the Calculator object.
    To prevent this behaviour, set the ``update_calculator`` parameter to ``False``,
    as shown below:

    .. code-block:: python

        new_sens = 15*u.mJy
        calculated_t_int = calculator.calculate_t_integration(new_sens, update_calculator=False)

    You may then manually update the calculator with the new values:

    .. code-block:: python

        calculator.t_int = calculated_t_int
        calculator.sensitivity = new_sens

.. note::

    If the calculated integration time or sensitivity is outside the permitted range
    of values, the calculator will report a warning and the calculated value
    will not be stored in the Calculator object.


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
    g: 0
    surface_rms: 25 micron
    dish_radius: 25 m
    T_amb: 270 K
    eta_eff: 0.95
    eta_ill: 0.8
    eta_spill: 0.95
    eta_block: 0.94
    eta_pol: 0.995

    # Check the derived parameters
    >>> print(calculator.derived_parameters)
    tau_atm: 0.02762
    T_atm: 401.094323096683 K
    T_rx: 23.996215366831105 K
    eta_a: 0.703065
    eta_s: 0.99
    T_sys: 54.61020434562856 K
    T_sky: 13.652788658783503 K
    sefd: 1.0923500468071407e-24 J / m2

.. _input data:

Providing input data to the calculator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: providing_input_data.rst

Writing parameters to file
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: writing_parameters_to_file.rst
