Usage
=====

Beyond the browser interface, the sensitivity calculator may be used as a standalone python package that can be incorporated into your python code.
This is described in the proceeding sections. See the Public API documentation for more details.

Configuration
-------------

To configure the inputs to the calculation, users may edit the file ``user_inputs.yaml``.
This is a .yaml config file which offers a structured input for the variables and their respective units, in the format:

.. code-block:: yaml

    ---
    t_int       : {value: 0,   unit: s}  
    sensitivity : {value: 0,   unit: mJy} 
    bandwidth   : {value: 7.5, unit: GHz}
    obs_freq    : {value: 350, unit: GHz}
    n_pol       : {value: 2,   unit: none} 
    weather     : {value: 50,  unit: none}
    elevation   : {value: 30,  unit: deg} 

By default, the integration time ``t_int`` and the sensitivity ``sensitivity`` are both set to zero; upon running the software the user will encounter an error if neither or both of these parameters are given a value. Other user configurable parameters are provided with default example values.
The user can modify these input parameters to match the observational setup required.

To modify the telescope setup, there are further configurable values in files stored in ``src/configs/``. These contain values such as the efficiency factors of the telescope system. However these are not intended to be configurable for users and can be ignored unless intrinsic telescope parameters should be adjusted.


Running the calculator
----------------------

A simple script ``run.py`` is provided in the ``demo`` directory, demonstrating the functionality of the calculator.

Development of this demo is currently a work in progress. For now, the demo can be run by navigating to the root
directory of the repository and run the following:

.. code-block:: python

    python -m atlast_sc.demo.run

How it works
************

To begin we initialise the input parameters from the configuration file ``user_inputs.yaml``:

.. code-block:: python

    from atlast_sc.sensitivity import Sensitivity
    from atlast_sc.configs.config import Config
    import astropy.units as u

    # Initialise the input parameters from Config
    calculator = Sensitivity(Config.from_yaml("user_inputs.yaml"))


To obtain a sensitivity given an integration time:

.. code-block:: python

    integration_time = 100 * u.s
    calculated_sensitivity = calculator.sensitivity(integration_time).to(u.mJy) 
    print("Sensitivity: {:0.2f} for an integration time of {:0.2f} ".format(calculated_sensitivity, integration_time))

And conversely, to obtain the integration time required for a given sensitivity:


.. code-block:: python

    sensitivity = 10 * u.mJy
    calculated_t_int = calculator.t_integration(sensitivity)
    print("Integration time: {:0.2f} to obtain a sensitivity of {:0.2f}".format(calculated_t_int, sensitivity))


To re-run the same calculation, we can store the input sensitivity and/or integration time to the config like so:

.. code-block:: python

    config.t_int = integration_time
    config.sensitivity = sensitivity

And then print the full configuration input parameters to a log file:

.. code-block:: python

    config.to_file("logs/log_output_parameters.txt")
