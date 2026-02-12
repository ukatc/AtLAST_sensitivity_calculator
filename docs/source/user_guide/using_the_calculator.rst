Using the Calculator
--------------------
Basic usage
^^^^^^^^^^^
First, import the :class:`Calculator <atlast_sc.calculator.Calculator>` class from
the :mod:`atlast_sc.calculator` module:

.. code-block:: python

    from atlast_sc.factory import CalculatorFactory

You may also find it useful to import astropy units as these are required for defining the user inputs:

.. code-block:: python

    import astropy.units as u

Next, initialize the calculator as follows.

.. code-block:: python

    calculator = CalculatorFactory().calculator

.. note::

    The Sensitivity Calculator is pre-configured with default values for all
    user input parameters. See :doc:`here <../calculator_info/user_input>` for
    information on the calculation input parameters and their default values.

    You may also initialize the calculator with your own
    input values. This is described in the section :ref:`input data`.


All input parameters can be updated manually. For example, to
set the bandwidth after initializing the calculator:

.. code-block:: python

    calculator.user_input.bandwidth = 150*u.MHz

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

.. _section_instrument_selection:

Instrument selection
^^^^^^^^^^^^^^^^^^^^

The calculator supports a range of instruments as described in the 
:doc:`instrument overview <../calculator_info/instrument_overview>`. The calculator will 
automatically pick an appropriate instrument based on the observing frequency and bandwidth. 
The user will be notified whenever the instrument changes. For example:

.. code-block:: python

    >>> calculator.user_input.obs_freq = 270*u.GHz
    Instrument has been changed from Sepia to Finer.

The currently selected instrument can be checked using:

.. code-block:: python

    >>> calculator.chosen_instrument

The instrument can also be changed using this as follows (note that this is case 
insensitive):

.. code-block:: python

    >>> calculator.chosen_instrument = 'finer'

.. warning::
    
    Choosing an instrument that is not appropriate for the current observing frequency and 
    bandwidth will result in an error. 

The observing frequency and bandwidth ranges for the 
instruments can be checked with:

.. code-block:: python

    >>> calculator.list_instruments()


Resetting the calculator
^^^^^^^^^^^^^^^^^^^^^^^^

You can reset the parameters stored in the calculator to their initial values
using the :meth:`reset <atlast_sc.calculator.Calculator.reset>` method:

.. code-block:: python

        # initialize the calculator with its default values
        calculator = CalculatorFactory().calculator

        # change the value of one of the parameters
        calculator.user_input.bandwidth = 150*u.MHz

        # reset the calculator
        calculator.reset()

        # check the bandwidth value stored in the calculator
        print('bandwidth', calculator.user_input.bandwidth)
        # expected output
        # bandwidth 100.0 MHz


Checking the parameters stored by the calculator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The calculator stores the user input parameters, instrument setup parameters, and
derived parameters that are calculated from other inputs. You can output these
parameters to the console as follows:

.. code-block:: bash

    # Check the user input parameters
    >>> calculator.user_input.show()
    bandwidth: 100.0 MHz
    elevation: 45.0 deg
    n_pol: 2.0
    obs_freq: 100.0 GHz
    sensitivity: 3.0 mJy
    t_int: 100.0 s
    weather: 25.0

    # Check the telescope and environment parameters
    >>> calculator.telescope_and_environment.show()
    T_amb: 270.0 K
    T_cmb: 2.726 K
    dish_radius: 30.0 m
    eta_block: 0.94
    eta_eff: 0.95
    eta_ill: 0.8
    eta_pol: 0.995
    eta_spill: 0.95
    surface_rms: 25.0 micron


    # Check the derived parameters
    >>> calculator.derived_parameters.show()
    T_atm: 401.094323096683 K
    T_sky: 13.652788658783503 K
    T_sys: 54.61020434562856 K
    eta_a: 0.7030648055535439
    eta_s: 0.99
    sefd: 7.585764213938477e-25 J / m2
    transmittance: 0.9727575584355762


.. _input data:

Providing input data to the calculator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: providing_input_data.rst

Writing parameters to file
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: writing_parameters_to_file.rst
