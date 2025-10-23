import copy, re
from atlast_sc.models import UserInput
from atlast_sc.models import InstrumentSpecific
from atlast_sc.models import CalculationInput
from atlast_sc.models import TelescopeAndEnvironment

from atlast_sc.instruments.config import InstrumentConfig

class ParameterSetup:
    """
    Class that holds the user input and instrument setup parameters
    used to perform the sensitivity calculations.
    """
    def __init__(self, user_input={}, instrument_specific={}, telescope_and_environment={}, finetune=False):
        """
        Initialises all the required parameters from user_input and
        instrument_specific.

        :param user_input: A dictionary of user inputs of structure
        {'param_name':{'value': <value>, 'unit': <unit>}}
        :type user_input: dict
        :param instrument_specific: A dictionary of instrument setup parameters
        of structure
        {'param_name':{'value': <value>, 'unit': <unit>}}
        :type instrument_specific: dict
        """

        # Make sure the user input doesn't contain any unexpected parameter names
        self._check_input_param_names(user_input)

        self.finetune = finetune
        new_user_input = UserInput(**user_input)
        new_instrument_specific = InstrumentSpecific(**instrument_specific)
        new_telescope_and_environment = TelescopeAndEnvironment(**telescope_and_environment)
        
        self._calculation_inputs = \
            CalculationInput(user_input=new_user_input,
                             instrument_specific=new_instrument_specific,
                             telescope_and_environment=new_telescope_and_environment)
        
        # Make a deep copy of the calculation inputs to enable the
        # calculator to be reset to its initial setup
        self._original_inputs = copy.deepcopy(self._calculation_inputs)

        # Get instrument config 
        inst_config = InstrumentConfig()
        self.loaded_instruments = inst_config.instrument_classes

    @property
    def calculation_inputs(self):
        """
        The inputs to the calculation (user input and instrument setup)
        """
        return self._calculation_inputs

    @property
    def user_input(self):
        """
        User inputs to the calculation
        """
        return self._calculation_inputs.user_input

    @property
    def instrument_specific(self):
        """
        Instrument specific parameters
        """
        return self._calculation_inputs.instrument_specific
    
    @property
    def telescope_and_environment(self):
        """
        Telescope and environment parameters
        """
        return self._calculation_inputs.telescope_and_environment

    def reset(self):
        """
        Resets the calculator configuration parameters (user input and
        instrument setup to their original values.
        """
        self._calculation_inputs = \
            self._original_inputs
        
    @staticmethod
    def _check_input_param_names(user_input):
        """
        Validates the user input parameters (just the names; value validation
        is handled by the model)

        :param user_input: Dictionary containing user-defined input parameters
        :type user_input: dict
        """

        test_model = UserInput()

        for param in user_input:
            if param not in test_model.__dict__:
                raise ValueError(f'"{param}" is not a valid input parameter')
            
    def get_chosen_instrument(self):
        """
        (ASC-76)
        Retrieve the instrument object class according to observing frequency
        and bandwidth values the user has provided. 

        :return: instrument module
        :rtype: atlast_sc.parameters.Instrument
        """
        # Look at obs_freq and bandwidth values
        user_obs_freq = self.user_input.obs_freq.value
        user_bandwidth = self.user_input.bandwidth.value
        # See which instrument those values correspond to
        chosen_inst_name = self.find_applicable_instruments(obs_freq=user_obs_freq, bandwidth=user_bandwidth)
        # Get the instrument module according to instrument name
        chosen_inst = self.loaded_instruments[chosen_inst_name]
        return chosen_inst

    def find_applicable_instruments(self, obs_freq, bandwidth):
        """
        Finds what instrument/s the observing frequency and bandwidth values
        inputted by the user correspond to and choose one to do the further
        calculations. 

        :return: applicable/chosen instrument name
        :rtype: String
        """
        # TODO: could make the finding applicable ranges more efficient by looking at general ranges first 

        instrument_obs_freqs = {} # Instrument specific observing frequency ranges
        instrument_bandw_vals = {} # Instrument specific bandwidth value ranges
        for inst_name, inst_module in self.loaded_instruments.items():
            instrument_obs_freqs[inst_name] = inst_module.obs_freq_ranges_and_unit
            instrument_bandw_vals[inst_name] = inst_module.bandwidth_ranges_and_unit

        applicable_obs_freq_instruments = []
        applicable_bandw_instruments = []

        # Get float value of each parameter to be able to make comparison
        obs_freq = float(obs_freq.value)
        bandwidth = float(bandwidth.value)

        # Check what instrument/s the observing frequency value falls in
        for instrument, obs_freqs in instrument_obs_freqs.items():
            obs_freq_ranges = obs_freqs['ranges']
            for range in obs_freq_ranges:
                range = re.findall(r"[\d.]+", range)
                min_freq = float(range[0])
                max_freq = float(range[1])
                if obs_freq >= min_freq and obs_freq <= max_freq:
                    applicable_obs_freq_instruments.append(instrument)

        # Check what instrument/s the bandwidth value falls in
        for instrument, bandw_vals in instrument_bandw_vals.items():
            bandw_val_ranges = bandw_vals['ranges']
            for range in bandw_val_ranges:
                range = re.findall(r"[\d.]+", range)
                min_bandw = float(range[0])
                max_bandw = float(range[1])
                if bandwidth >= min_bandw and bandwidth <= max_bandw:
                    applicable_bandw_instruments.append(instrument)

        # Create a set of both applicable instruments lists and take the intersection
        applicable_instruments = list(set(applicable_obs_freq_instruments) & \
                                      set(applicable_bandw_instruments))
        # NOTE: Adding this sorting functionality to keep consistency until further
        # logic on how to choose an instrument if there are multiple applicable
        # instruments
        applicable_instruments = sorted(applicable_instruments)
        # If there are more than 1 applicable instrument
        if len(applicable_instruments) > 1:
            # TODO: there might be further logic incorporated to choose which instrument 
            # will be defaulted currently we are choosing the second applicable instrument
            return applicable_instruments[1]
        if len(applicable_instruments) == 1: # If there is only 1 applicable instrument
            return applicable_instruments[0]
        else: # If there is no applicable instrument
            return "Default"