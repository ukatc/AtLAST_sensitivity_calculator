The :class:`FileHelper <atlast_sc.utils.FileHelper>` method
:meth:`write_to_file <atlast_sc.utils.FileHelper.write_to_file>` writes
all user inputs and derived parameters to a
plain-text, `YAML <https://en.wikipedia.org/wiki/YAML>`__,
or `JSON <https://en.wikipedia.org/wiki/JSON>`__ formatted file.

For example, to write data to a ``YAML`` file called ``output_parameters.yml``
in the directory ``logs``:

.. code-block:: python

    FileHelper.write_to_file(calculator, "logs", "output_parameters", "yml")


Below is an example of a ``YAML``-formatted output file:

.. code-block::

    t_int           : {value:      100.0, unit: s}
    sensitivity     : {value: 0.0016932450280061624, unit: Jy}
    bandwidth       : {value:      100.0, unit: MHz}
    obs_freq        : {value:      100.0, unit: GHz}
    n_pol           : {value:        2.0}
    weather         : {value:       25.0}
    elevation       : {value:       45.0, unit: deg}
    tau_atm         : {value: 0.027620396974877098}
    T_atm           : {value:   7.757599, unit: K}
    T_rx            : {value: 23.996215366831105, unit: K}
    eta_a           : {value: 0.6995318165809129}
    eta_s           : {value:       0.99}
    T_sys           : {value: 114.70931842978237, unit: K}
    sefd            : {value: 2.306081307192973e-24, unit: J / m2}
    area            : {value: 1963.4954084936207, unit: m2}
