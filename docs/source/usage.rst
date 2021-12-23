Usage
=====

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

