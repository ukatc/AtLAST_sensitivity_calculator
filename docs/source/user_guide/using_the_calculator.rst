Using the Calculator
--------------------

After the package has been successfully installed and verified, the following workflow describes how to setup and perform
sensitivity or integration time calculations given weather, telescope and instrumentation settings and either a required sensitivity (to calculate
on source integration time) or an integration time (to calculate sensitivity).

Basic usage
^^^^^^^^^^^
After installing the package and creating the conda environment, follow these commands to import the calculator and required
packages and run simple time and sensitivity calculations for a given set of weather, telescope and instrument
parameters.

First, import the calculator package to interact with the calculator classes and methods:

.. code-block:: python

    from atlast_sc.calculator import Calculator


Since the sensitivity calculator depends on parameters being specified with units, you will also find
it useful to import ``astropy.units`` as this package is required for defining the user inputs:

.. code-block:: python

    import astropy.units as u


Next, initialise the calculator object. The Calculator class is the main interface to the sensitivity calculator, 
and provides a single point of access to all of the calculator's functionality. Initializing
a calculator object at the beginning of your python session ensures that your changes to setup parameters are
used consistently throughout.

.. code-block:: python

    calculator = Calculator()


The Sensitivity Calculator is pre-configured with default values for all
user input parameters. See :doc:`here <../calculator_info/user_input>` for
information on the calculation input parameters and their default values.

You may also initialize the calculator with your own
input values. This is described in the section :ref:`input data`. To see what values have already
been set, you can use:

.. code-block:: python

    calculator.user_input.show()



All input parameters can be updated manually, using the parameter names listed from ``calculator.user_input.show()``.
For example, to set the bandwidth after initializing the calculator:

.. code-block:: python

    calculator.user_input.bandwidth = 150*u.MHz


All input parameters are validated by the calculator. You will see
an error if the values you provide are invalid (e.g., are out of a specified
range or have invalid units), and the calculator will warn you if (or when) the input
parameters force it into a configuration that mandates a different instrument.

With all of the input parameters set to meet your required calculation, including integration time, call the
:meth:`calculate_sensitivity <atlast_sc.calculator.Calculator.calculate_sensitivity>`
method to obtain the sensitivity (in mJy):

.. code-block:: python

    calculated_sensitivity = calculator.calculate_sensitivity()



Alternatively, to obtain the integration time required having specified a sensitivity, call
:meth:`calculate_t_integration <atlast_sc.calculator.Calculator.calculate_t_integration>`:

.. code-block:: python

    calculated_t_int = calculator.calculate_t_integration()


If the calculated integration time or sensitivity is outside the permitted range
of values, the calculator will report a warning and the calculated value
will not be stored in the Calculator object.


Checking the parameters stored by the calculator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The calculator stores the user input parameters, instrument, telescope and environment setup parameters, and
any further derived parameters calculated from other inputs. You can output these
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
    dish_radius: 25.0 m
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

The user input and derived parameters can be output to a file as described in the :ref:`writing parameters to a file<section_writing_data>` section.

Resetting the calculator
^^^^^^^^^^^^^^^^^^^^^^^^

You can reset the user input parameters stored in the calculator to their initial values using the :meth:`reset <atlast_sc.calculator.Calculator.reset>` method:

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

    calculator = CalculatorFactory(input_data).calculator

All values must be numeric (integer or float), and units (when required) must be presented as `astropy units <https://docs.astropy.org/en/stable/units/index.html>`__.
The Calculator will throw an error if any of the input parameter names are incorrect. If any of the
parameters have not been manually set via the input data dictionary, the calculator will use the
appropriate default values and units.

The dictionary can be generated from an input file as described in :ref:`Reading data from an input file<section_reading_data>`.

.. _section_instrument_selection:
Instrument selection
^^^^^^^^^^^^^^^^^^^^

The AtLAST sensitivity calculator supports a range of instruments as described in the
:doc:`instrument overview <../calculator_info/instrument_overview>`. The calculator will
automatically pick an appropriate instrument based on the observing frequency and bandwidth.
The user will be notified whenever the instrument changes. For example:

.. code-block:: python

    >>> calculator.user_input.obs_freq = 270*u.GHz
    Instrument has been changed from Sepia to Finer.

The currently selected instrument can be checked using:

.. code-block:: python

    >>> calculator.chosen_instrument

The instrument can also be changed using the following (case insensitive) command:

.. code-block:: python

    >>> calculator.chosen_instrument = 'finer'



Choosing an instrument that is not appropriate for the current observing frequency and
bandwidth will result in an error, and a request for the user to either chose a different instrument
or update the observing frequency and/or bandwidth.

The observing frequency and bandwidth ranges for the instruments can be checked with:

.. code-block:: python

    >>> calculator.list_instruments()


