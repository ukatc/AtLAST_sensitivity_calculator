import yaml
from yaml import Loader, Dumper
import astropy.units as u


class Config:
    def __init__(self, user_input, setup_input, fixed_input, default_input):
        self.user_input = self.get_inputs(user_input)
        self.setup_input = self.get_inputs(setup_input)
        self.fixed_input = self.get_inputs(fixed_input)
        self.obs_freq = self.user_input.get('obs_freq', self.get_inputs(default_input).get('obs_freq')) 
        self.n_pol = self.user_input.get('n_pol', self.get_inputs(default_input).get('n_pol')) 
        # etc for all the input attributes

    def get_inputs(self, file):
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

        # self.pwv =
        # self.RA =
        # self.Dec =
        # self.bandwidth =