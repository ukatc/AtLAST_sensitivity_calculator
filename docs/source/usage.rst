Usage
=====

Beyond the browser interface, the sensitivity calculator may be used as a standalone python package that can be incorporated into your python code.
This is described in the following sections. See the Public API documentation for more details.

Configuration
-------------

To configure the inputs to the calculation, create a ``yaml`` file containing each of the input parameters along with
their respective values and units. An example ``yaml`` file is shown below.

.. code-block:: yaml

    ---
    t_int       : {value: 100, unit: s}
    sensitivity : {value: 0.3, unit: mJy}
    bandwidth   : {value: 7.5, unit: GHz}
    obs_freq    : {value: 100, unit: GHz}
    n_pol       : {value: 2,   unit: none} 
    weather     : {value: 50,  unit: none}
    elevation   : {value: 30,  unit: deg} 

You may also use the calculator without specifying these input parameters. In this case, the values shown above will
be used by default (see the next section).

Using the calculator
--------------------

First, import the required Python packages:

.. code-block:: python

    import astropy.units as u
    from atlast_sc.calculator import Calculator
    from atlast_sc import utils

Next, we read the input parameters from our configuration file ``user_inputs.yaml`` and initialise the calculator.

**Note**: Here we are assuming that the ``yaml`` file is in a directory ``input_data``, which is a subdirectory of our
current location.

.. code-block:: python

    # Read the user input from a yaml file
    user_input = utils.from_yaml('input_data', 'user_inputs.yaml')
    # Initialise the Calculator with user inputs dictionary
    calculator = Calculator(user_input)

Alternatively, you may initialise the calculator with the default values.

.. code-block:: python

    calculator = Calculator()

To obtain a sensitivity for a given integration time:

.. code-block:: python

    # Specify an integration time and pass this to the calculator
    integration_time = 100 * u.s
    calculated_sensitivity = calculator.calculate_sensitivity(integration_time).to(u.mJy)

Alternatively, you may use the integration time configured in the calculator from your input file:

.. code-block:: python

    calculated_sensitivity = calculator.calculate_sensitivity(calculator.t_int).to(u.mJy)

Conversely, to obtain the integration time required for a given sensitivity:

.. code-block:: python

    # Specify a sensitivity and pass this to the calculator
    sensitivity = 10 * u.mJy
    calculated_t_int = calculator.calculate_t_integration(sensitivity)

Alternatively, you may use the sensitivity configured in the calculator from your input file:

.. code-block:: python

    calculated_t_int = calculator.calculate_t_integration(calculator.sensitivity)

We can store the input sensitivity and/or integration time in the calculator like so:

.. code-block:: python

    calculator.t_int = integration_time
    calculator.sensitivity = sensitivity

The output can be written to a text file as follows:

.. code-block:: python

    utils.to_file(calculator.sensitivity_calc_params.calculator_params(), "logs/output_parameters.txt")

You can also write the output to a ``yaml`` file:

.. code-block:: python

    utils.to_yaml(calculator.sensitivity_calc_params.calculator_params(), "logs/output_parameters.yaml")

Running the demo
----------------

If you have cloned the GitHub repository, you can use the ``run.py`` script in the ``demo`` directory to
play with and learn how the calculator works.

Development of this demo is currently a work in progress. For now, the demo can be run by navigating to the root
directory of the repository and running the following:

.. code-block:: python

    python -m demo.run