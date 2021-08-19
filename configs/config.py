import yaml
from yaml import Loader, Dumper
import astropy.units as u


class Config:
    ''' A class that reads in values from the input files, and if they do not exist fills with defaults. '''
    def __init__(self, user_input, setup_input, fixed_input, default_input):
        self.user_input = self.get_inputs(user_input)
        self.setup_input = self.get_inputs(setup_input)
        self.fixed_input = self.get_inputs(fixed_input)
        self.default = self.get_inputs(default_input)
        self.obs_freq = self.user_input.get('obs_freq', self.default.get('obs_freq')) 
        self.n_pol = self.user_input.get('n_pol', self.default.get('n_pol')) 
        # etc for all the input attributes
        # self.pwv =
        # self.RA =
        # self.Dec =
        # self.bandwidth =

    def get_inputs(self, file):
        '''
        Read input from a .yaml file and return a dictionary
        Check for units and convert value into astropy.unit.Quantity if units given
        
        :param file: the .yaml file with parameters described as param_name: {value:param_value, unit:param_unit}
        :type file: str (file path)
        :retunr: a dictionary of astropy.unit.Quantities, if units given
        :rtype: dict
        '''
        dict = {}
        file = open(file, "r")
        inputs = yaml.load(file, Loader=Loader)
        for key in inputs.keys():
            if inputs[key]['unit'] == "none":
                dict[key] = inputs[key]['value']
            else:
                unit = getattr(u, inputs[key]['unit'])
                dict[key] = inputs[key]['value'] * unit
        return dict

