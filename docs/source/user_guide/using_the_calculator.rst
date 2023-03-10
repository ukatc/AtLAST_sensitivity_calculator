Using the Calculator
--------------------

Basic usage
^^^^^^^^^^^
First, import the Python package:

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

**TODO: provide details of which parameters can be manually changed, and what
their valid values and units are.**

To obtain the sensitivity (in Jansky):

.. code-block:: python

    calculated_sensitivity = calculator.calculate_sensitivity()

You can also specify an integration time to perform the sensitivity calculation:

.. code-block:: python

    t_int = 150*u.s
    calculated_sensitivity = calculator.calculate_sensitivity(t_int)


Conversely, to obtain the integration time required (in seconds):

.. code-block:: python

    calculated_t_int = calculator.calculate_t_integration()

You can also specify a sensitivity to perform the integration time calculation:

.. code-block:: python

    sens = 10*u.mJy
    calculated_t_int = calculator.calculate_t_integration(sens)


.. note::

    When the sensitivity or integration time calculations are performed,
    the values stored in the calculator are updated by default. To prevent this
    behaviour, set the ``update_calculator`` parameter to ``False``, as shown below:

    .. code-block:: python

        calculated_t_int = calculator.calculate_t_integration(update_calculator=False)

    You can then manually update the calculator with the new value:

    .. code-block:: python

        calculator.t_int = calculated_t_int



Providing input data to the calculator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: providing_input_data.rst

Writing parameters to file
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: writing_parameters_to_file.rst


Running the demo
----------------
**TODO: remove this section and provide either static tutorial pages, or
interactive notebooks**

If you have cloned the GitHub repository, you can use the ``run.py`` script in the ``demo`` directory to
play with and learn how the calculator works.

Development of this demo is currently a work in progress. For now, the demo can be run by navigating to the root
directory of the repository and running the following:

.. code-block:: python

    python -m demo.run