import yaml
from yaml import Loader
import astropy.units as u
from pathlib import Path
import json

CONFIG_PATH = Path(__file__).resolve().parents[0]

class Config:
    """ A class that reads in values from the input dictionaries, and if they do not exist fills with defaults. """
    def __init__(self, user_input, setup = "setup_inputs.yaml", fixed = "fixed_inputs.yaml", default = "default_inputs.yaml"):
        '''
        Initialises all the required parameters from various input sources
        setup_input, fixed_input and the default can be found in .yaml files in the configs directory
        User input is here read as dict but class methods allow reading various file types.

        :param user_input: a dictionary of user inputs of structure {'param_name':{'value': , 'unit': }}
        :type user_input: dict
        '''
        self.user_input = self.enforce_units(user_input)
        self.setup_input = self.enforce_units(self._dict_from_yaml(CONFIG_PATH / setup))
        self.fixed_input = self.enforce_units(self._dict_from_yaml(CONFIG_PATH / fixed))
        self.default = self.enforce_units(self._dict_from_yaml(CONFIG_PATH / default))

        self.t_int        = self.user_input.get('t_int', self.default.get('t_int')) 
        self.sensitivity  = self.user_input.get('sensitivity', self.default.get('sensitivity')) 
        self.bandwidth    = self.user_input.get('bandwidth', self.default.get('bandwidth'))
        self.obs_freq     = self.user_input.get('obs_freq', self.default.get('obs_freq'))
        self.n_pol        = self.user_input.get('n_pol', self.default.get('n_pol'))
        self.weather      = self.user_input.get('weather', self.default.get('weather'))
        self.elevation    = self.user_input.get('elevation', self.default.get('elevation'))
        self.g            = self.setup_input.get('g', self.default.get('g'))
        self.surface_rms  = self.setup_input.get('surface_rms', self.default.get('surface_rms'))
        self.dish_radius  = self.setup_input.get('dish_radius', self.default.get('dish_radius'))
        self.T_amb        = self.setup_input.get('T_amb', self.default.get('T_amb'))
        self.T_rx         = self.setup_input.get('T_rx', self.default.get('T_rx'))
        self.eta_eff      = self.setup_input.get('eta_eff', self.default.get('eta_eff'))
        self.eta_ill      = self.setup_input.get('eta_ill', self.default.get('eta_ill'))
        self.eta_q        = self.setup_input.get('eta_q', self.default.get('eta_q'))
        self.T_cmb        = self.fixed_input.get('T_cmb')

    @classmethod
    def _dict_from_yaml(self, path):
        '''
        Read input from a .yaml file and return a dictionary

        :param path: the .yaml file with parameters described as param_name: {value:param_value, unit:param_unit}
        :type path: str (file path)

        '''
        with open(path, "r") as yaml_file:
            inputs = yaml.load(yaml_file, Loader=Loader)
        return inputs

    @classmethod
    def from_yaml(self, path):
        '''
        Takes a .yaml input file of user inputs and returns an instance of ``Config``

        :param path: the path of the input .yaml file
        :type path: str
        '''
        inputs = Config._dict_from_yaml(path)
        return Config(inputs)

    @classmethod
    def from_json(self, path):
        '''
        Takes a .json input file of user inputs and returns an instance of Config

        :param path: the path of the input json file
        :type path: str
        '''
        with open(path, "r") as json_file:
            inputs = json.load(json_file)
        return Config(inputs)

    def enforce_units(self, inputs):
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
                unit = u.Unit(inputs[key]["unit"])
                params[key] = inputs[key]["value"] * unit
        return params

    def to_file(self, path):
        '''
        Write config parameters to file
        
        :param path: the path of the output log file
        :type path: str
        '''
        with open(path, "w") as f:
            for attr in vars(self):
                if type(getattr(self, attr)) == dict:
                    pass
                else:
                    f.write("{} = {} \n".format(attr, getattr(self, attr)))

    def to_yaml(self, path):
        import astropy
        with open(path, "w") as f:
            for attr in vars(self):
                if type(getattr(self, attr)) == dict:
                    pass
                else:
                    if type(getattr(self, attr)) == astropy.units.quantity.Quantity and not getattr(self, attr).unit == ' ':
                        f.write("{0: <16}: {{value: {1: >10}, unit: {2}}} \n".format(attr, getattr(self, attr).value, getattr(self, attr).unit))
                    else:
                        f.write("{0: <16}: {{value: {1: >10}, unit: none}} \n".format(attr, getattr(self, attr)))