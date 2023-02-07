import os
from pathlib import Path
import json
from yaml import load, Loader
from astropy.units import Unit
from astropy.units.quantity import Quantity

from atlast_sc import inputs

PARENT_PATH = Path(__file__).resolve().parents[0]

STANDARD_CONFIG_PATH = os.path.join(PARENT_PATH, "configs", "standard")
BENCHMARKING_CONFIGS_PATH = os.path.join(PARENT_PATH, "configs", "benchmarking")
BENCHMARKING_JCMT_PATH = os.path.join(BENCHMARKING_CONFIGS_PATH, "JCMT")
BENCHMARKING_APEX_PATH = os.path.join(BENCHMARKING_CONFIGS_PATH, "APEX")

STANDARD_SETUP = 'standard'
CUSTOM_SETUP = 'custom'
# TODO: are these benchmarking setups still required?
BENCHMARKING_APEX = 'apex'
BENCHMARKING_JCMT = 'jcmt'


class Config:
    """
    Sets up the configuration used to perform the sensitivity calculations.

    Attributes
    ----------

    Methods
    -------
    """
    # def __init__(self, user_input, setup="setup_inputs.yaml", fixed="fixed_inputs.yaml",
    #              default="default_inputs.yaml"):
    def __init__(self, user_input, setup='standard', file_path=None, setup_inputs_file="setup_inputs.yaml",
                 fixed_inputs_file="fixed_inputs.yaml", default_inputs_file="default_inputs.yaml"):
        """
        Initialises all the required parameters from various input sources
        setup_input, fixed_input and the default can be found in .yaml files in the configs directory
        User input is here read as dict but class methods allow reading various file types.

        :param user_input: A dictionary of user inputs of structure {'param_name':{'value': , 'unit': }}
        :type user_input: dict
        :param setup: The required telescope setup. Default value 'standard'
        """

        # TODO: do we want to keep this and make it part of the object?
        calculation_input = inputs.CalculationInput(**user_input)

        if setup == STANDARD_SETUP:
            config_path = STANDARD_CONFIG_PATH
        elif setup == BENCHMARKING_JCMT:
            config_path = BENCHMARKING_JCMT_PATH
        elif setup == BENCHMARKING_JCMT:
            config_path = BENCHMARKING_APEX_PATH
        elif setup == CUSTOM_SETUP:
            # User is expected to provide the path
            # TODO: figure out how to make this easy for the user
            # TODO: report an error if the file path is not provided
            config_path = file_path
        else:
            # TODO need some error handling/data validation
            pass

        self._setup_input = self.enforce_units(self._dict_from_yaml(config_path, setup_inputs_file))
        self._fixed_input = self.enforce_units(self._dict_from_yaml(config_path, fixed_inputs_file))
        self._default = self.enforce_units(self._dict_from_yaml(config_path, default_inputs_file))

        # TODO provide input to the get_params method
        user_defined_params = \
            self.get_params([])
        setup_params = self.get_params([])
        # TODO get rid of this and put fixed params in a constants file
        fixed_params = self.get_params([], False)


        # TODO: provide accessor methods for all of these properties (and make them properties!)
        # TODO: store initial input in an object (should always be possible to recover the initial
        #       state and/or restrict the values that the user can manipulate)

        # User defined input parameters
        self.t_int = self._user_input.get('t_int', self._default.get('t_int'))
        self.sensitivity = self._user_input.get('sensitivity', self._default.get('sensitivity'))
        self.bandwidth = self._user_input.get('bandwidth', self._default.get('bandwidth'))
        self.obs_freq = self._user_input.get('obs_freq', self._default.get('obs_freq'))
        self.n_pol = self._user_input.get('n_pol', self._default.get('n_pol'))
        self.weather = self._user_input.get('weather', self._default.get('weather'))
        self.elevation = self._user_input.get('elevation', self._default.get('elevation'))

        # Instrument-specific input parameters
        self.g = self._setup_input.get('g', self._default.get('g'))
        self.surface_rms = self._setup_input.get('surface_rms', self._default.get('surface_rms'))
        self.dish_radius = self._setup_input.get('dish_radius', self._default.get('dish_radius'))
        self.T_amb = self._setup_input.get('T_amb', self._default.get('T_amb'))
        self.T_rx= self._setup_input.get('T_rx', self._default.get('T_rx'))
        self.eta_eff = self._setup_input.get('eta_eff', self._default.get('eta_eff'))
        self.eta_ill = self._setup_input.get('eta_ill', self._default.get('eta_ill'))
        self.eta_spill = self._setup_input.get('eta_spill', self._default.get('eta_spill'))
        self.eta_block = self._setup_input.get('eta_block', self._default.get('eta_block'))
        self.eta_pol = self._setup_input.get('eta_pol', self._default.get('eta_pol'))
        self.eta_r = self._setup_input.get('eta_r', self._default.get('eta_r'))
        self.eta_q = self._setup_input.get('eta_q', self._default.get('eta_q'))

        # Fixed parameters
        # TODO: this should be configured as a constant. No point reading a single, fixed value from a file
        self.T_cmb = self._fixed_input.get('T_cmb')

    def get_params(self, param_names, have_defaults=True):
        return {param_name: self._user_input.get(param_name, self._default.get(param_name))
                for param_name in param_names}

    @classmethod
    def from_yaml(cls, path, file_name):
        """
        Takes a .yaml input file of user inputs and returns an instance of ``Config``

        :param path: the path to the input .yaml file
        :type path: str
        :param file_name: the name of input file
        :type path: str
        """
        inputs = cls._dict_from_yaml(path, file_name)
        return Config(inputs)

    @classmethod
    def from_json(cls, path):
        """
        Takes a .json input file of user inputs and returns an instance of Config

        :param path: the path of the input json file
        :type path: str
        """
        with open(path, "r") as json_file:
            inputs = json.load(json_file)
        return Config(inputs)

    @classmethod
    def enforce_units(cls, inputs):
        """
        Read dict of inputs. 
        Check for units and convert value into ``astropy.unit.Quantity`` if units given.
        
        :param inputs: a dictionary of inputs
        :type inputs: dict
        :return: a dictionary of ``astropy.unit.Quantity`, if units given
        :rtype: dict
        """
        params = {}
        for key in inputs.keys():
            if inputs[key]["unit"] == "none":
                params[key] = inputs[key]["value"]
            else:
                unit = Unit(inputs[key]["unit"])
                params[key] = inputs[key]["value"] * unit
        return params

    def to_file(self, path):
        """
        Write config parameters to file
        
        :param path: the path of the output log file
        :type path: str
        """
        with open(path, "w") as f:
            for attr in vars(self):
                if type(getattr(self, attr)) == dict:
                    pass
                else:
                    f.write("{} = {} \n".format(attr, getattr(self, attr)))

    def to_yaml(self, path):
        with open(path, "w") as f:
            # TODO: be explicit about the variables that are written to file.
            #       Should not be iterating over every instance member
            for attr in vars(self):
                if type(getattr(self, attr)) == dict:
                    pass
                else:
                    if type(getattr(self, attr)) == Quantity and not getattr(self, attr).unit == ' ':
                        f.write("{0: <16}: {{value: {1: >10}, unit: {2}}} \n".format(attr, getattr(self, attr).value, getattr(self, attr).unit))
                    else:
                        f.write("{0: <16}: {{value: {1: >10}, unit: none}} \n".format(attr, getattr(self, attr)))

    @classmethod
    def _dict_from_yaml(cls, path, file_name):
        """
        Read input from a .yaml file and return a dictionary

        :param path: the .yaml file with parameters described as param_name: {value:param_value, unit:param_unit}
        :type path: str (file path)
        """

        file_path = os.path.join(path, file_name)
        with open(file_path, "r") as yaml_file:
            inputs = load(yaml_file, Loader=Loader)
        return inputs

    @property
    def input_params(self):
        return self._input_params

    @input_params.setter
    def input_params(self, input_params):
        if input_params:
            return

        else:
            self._input_params = input_params
