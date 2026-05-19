Adding a New Instrument
=======================
When an instrument needs to be added to the calculator, a couple of files need to be created 
and modified to be able to integrate the new instrument to the existing calculator process. 

- creation of a YAML file with the name of the instrument
- creation of a Python module with the name of the instrument
- modifications to the configuration file

These changes will be made in the respective sub-directories and files within the 
*atlast_sc/instruments* directory. Details of these steps are provided in the 
following sub-sections. Once the required files are created and modified, the new instrument
should be visible on the CLI as well as the web UI and will be used in calculations when the
user input parameters correspond to the instrument's operational ranges. It should be noted 
that once the required files are in place, the developer should make sure to update the 
documentation to include the new instrument and its details, and to provide an example of 
how to use it in calculations.

For the following sections, we will take "Example" as the name of the new instrument to be added, 
and we will use this name in the examples provided.


Creating the instrument YAML file
---------------------------------
Firstly, a YAML file with the name of the instrument should be created in the 
sub-directory called :ref:`data <atlast-sc-data-module>`. It should include details of the instrument in the 
following format: 

.. code-block:: yaml

    name: "Example"
    allowed_ranges:
        observing_frequency:
            ranges: [(500.0-600.0),(700.0-800.0)]
            unit: GHz
        bandwidth: 
            ranges: [(10.9e4-1.8e8)]
            unit: Hz
    receiver_temperature: 
        values: [30.0,40.0]
        unit: K
    custom_parameter_with_unit:
        values: 1.0
        unit: unit of custom parameter
    custom_parameter_without_unit:
        values: 4.7

There are a couple of key points to note about the format of the YAML file:

- All ranges for a given parameter must be expressed in the same unit. (i.e. unit cannot be GHz 
  for the first observing frequency range, Hz for the second, etc.)
- Any recognised *astropy* units can be used for the unit entry. 
- If a parameter does not have a unit, the unit entry can be omitted.

It should be noted that the order of entries in the YAML file is not important, however the format 
of the entries should be followed as shown above to maintain consistency. For more details on the 
format and content of the YAML file, the Default instrument YAML file could be taken as a template 
and the other instrument YAML files could be taken as examples of how these files could be customised.

Creating the instrument Python module
-------------------------------------
Secondly, a Python module should be created in the *classes* sub-directory with the
new instrument name. Following the example above, the name of the module file should 
be "Example.py" to be consistent with that of the YAML file and the name of instrument 
class within it. The module should include a class with the name of the instrument 
that inherits from the base ``Instrument`` class. The module should also include any 
instrument specific parameters and methods that are required for the new instrument.
Following code block is a simple example on what the module could look like.

.. code-block:: python 

    """
    Example instrument parameters
    """        
    class Example(Instrument):
        def __init__(self, data):
            super().__init__(data)
            self._custom_parameter = data.custom_parameter

        ##################################
        # Instrument specific parameters #
        ##################################

        @property
        def custom_parameter(self):
            return self._custom_parameter

        @custom_parameter.setter
        def custom_parameter(self, value):
            self._custom_parameter = value

        ################################################
        # Additional instrument specific methods below #
        ################################################

        def calculate_system_temperature(self, parameters):
            # Custom calculation for system temperature, 
            # otherwise default calculation can be used.
            system_temp = 1 * u.K # Example value
            
            self.T_sys = system_temp
            return system_temp

        def custom_calculation_method(self):
            """
            Performs a custom calculation for the Example instrument. 
            This is just an example method and an example comment.
            """
            calculation_result = self.custom_parameter * 2
            return calculation_result
        
Setting the ``custom_parameter`` as a property with a setter method allows easy 
access and update of this parameter. If there are any specific validation 
requirements for the parameter, the developer can also include validation within the
setter method. Using properties with setter methods are also useful if a method within
the instrument module needs to update the parameter value for any reason.

The parameters set in the instrument YAML file can be accessed in the instrument module 
via the ``data`` argument in the initilisation method. There is no reason that the developer
needs to set each instrument parameter as a Python property. However, as mentioned in the 
previous paragraph, doing so allows more complexity to be added to the parameter if required.
The parameters in the YAML file can be used in any way within the instrument module. They 
can be used in methods to perform calculations, or they can be updated and used in calculations, 
etc.

Each instrument Python module must include a method with the name ``calculate_system_temperature`` 
that performs the calculation of system temperature for the instrument. This method will be 
required by the calculator to perform the sensitivity calculation when the instrument is selected.
If there is no specific calculation required for the new instrument, the method can simply
include the default calculation as shown below and in the *Default* instrument module. 

.. code-block:: python

    def calculate_system_temperature(self, parameters):
        """
        Returns system temperature, following calculation in [doc]

        :return: system temperature in Kelvin
        :rtype: astropy.units.Quantity
        """
        self.T_rx = self.calculate_receiver_temp(obs_freq)
        system_temp = 1 / (eta_eff * transmittance) * \
            (self.T_rx
            + (eta_eff * T_sky)
            + ((1 - eta_eff) * noise_temperature(T_amb, obs_freq))
            )
        self.T_sys = system_temp
        return system_temp

Note that there is a line to assign the variable ``T_sys`` to the calculated system temperature. 
This is important as the calculator will use this variable for the sensitivity calculation. 
As mentioned earlier, if the new instrument requires a different calculation for system temperature, 
the developer can modify the method accordingly, but the calculated value should still be assigned the to T_sys.
The ``T_sys`` variable should be an astropy quantity with units of Kelvin (or its equivalent in other units).

For more detail on how to construct the module, the Default instrument Python module
could be taken as the base example. Below are different types of instrument categories
where the individual Python modules could be taken as an example on how a new instrument 
module in the same category could be customised:

    - Heterodynes (FINER, SEPIA, CHAI)
    - Continuum/LEKID (MUSCAT)
    - IFU/MKID (TIFUUN)

Modifying the configuration file to add the new instrument
-----------------------------------------------------------
Thirdly, a couple of lines should be modified in :ref:`config.py <atlast-sc-instruments-module>` where they are 
indicated within the configuration file with comments.

In the initilisation method, a dictionary containing pointers to the new instrument's Python module 
and YAML file name should be added in similar format to the existing instruments. 

.. code:: python

    default_instrument = {'class': 'Default.py', 'data': 'Default.yaml'}
    # TODO: Add your custom instrument here.

After creating the dictionary variable for the new instrument, it should be added 
to the ``available_instruments`` list.

.. code:: python
    
    available_instruments = [
        default_instrument,
        # TODO: Add your custom instrument here.
    ]

When the new instrument is added to the necessary sections mentioned above in the configuration file, 
it will be available for selection in the calculator.