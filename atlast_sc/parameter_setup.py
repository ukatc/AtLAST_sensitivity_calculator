import copy, re
from atlast_sc.models import UserInput
from atlast_sc.models import InstrumentSpecific
from atlast_sc.models import CalculationInput
from atlast_sc.models import TelescopeAndEnvironment
from atlast_sc.utils import FileHelper
from atlast_sc.parameters.Instrument import GLTCam, Tifuun, Muscat, Finer, Chai, Sepia345, Default

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

        self.loaded_instruments = self.load_instrument_modules()

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
            
    
    def load_instrument_modules(self):
        """
        (ASC-76)
        Reads all instrument YAML files and creates their respective object
        class. These instrument object classes get assigned as value to a 
        dictionary where the corresponding instrument class will be pulled 
        according to the name. 
        """
        # TODO: Currently uses observing frequency in a few 
        # instrument modules according to guidelines provided by
        # instrument teams. Observing frequency might be used in
        # other instrument modules when guidelines are clearer.
        obs_freq = self.user_input.obs_freq.value
        inst_modules = {
            "GLTCam": GLTCam(data=FileHelper.read_instrument_file("gltcam")),
            "Tifuun": Tifuun(data=FileHelper.read_instrument_file("tifuun")),
            "Muscat": Muscat(data=FileHelper.read_instrument_file("muscat")),
            "Finer": Finer(data=FileHelper.read_instrument_file("finer")),
            "Chai": Chai(data=FileHelper.read_instrument_file("chai")),
            "Sepia345": Sepia345(data=FileHelper.read_instrument_file("sepia")),
            "Default": Default(data=FileHelper.read_instrument_file("default"),
                               obs_freq=obs_freq)
        }
        return inst_modules
    
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
        chosen_inst = self.get_inst_spec_params_module(inst_name=chosen_inst_name)
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
    
    def get_inst_spec_params_module(self, inst_name):
        """
        Returns the instrument module according to instrument 
        name and observing frequency value supplied. 

        :param inst_name: instrument name
        :type inst_name: String
        :return: instrument module
        :rtype: atlast_sc.parameters.Instrument
        """
        if inst_name is not None:
            match inst_name:
                case "GLTCam":
                    return self.loaded_instruments["GLTCam"]

                case "Tifuun":
                    return self.loaded_instruments["Tifuun"]

                case "Muscat":
                    return self.loaded_instruments["Muscat"]

                case "Finer":
                    return self.loaded_instruments["Finer"]

                case "Chai":
                    return self.loaded_instruments["Chai"]

                case "Sepia345":
                    return self.loaded_instruments["Sepia345"]
                
                case "Default":
                    return self.loaded_instruments["Default"]
        else:
           # TODO: Throw an error 
            return None
