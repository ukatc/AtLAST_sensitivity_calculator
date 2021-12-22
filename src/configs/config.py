import yaml
from yaml import Loader, Dumper
import astropy.units as u


class Config:
    """ A class that reads in values from the input files, and if they do not exist fills with defaults. """

    def __init__(self, user_input, setup_input, fixed_input, default_input):
        self.user_input = self.get_inputs(user_input)
        self.setup_input = self.get_inputs(setup_input)
        self.fixed_input = self.get_inputs(fixed_input)
        self.default = self.get_inputs(default_input)

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
        self.eta_transp   = self.setup_input.get('eta_transp', self.default.get('eta_transp'))
        self.eta_eff      = self.setup_input.get('eta_eff', self.default.get('eta_eff'))
        # self.eta_radf     = self.setup_input.get('eta_radf', self.default.get('eta_radf'))
        # self.eta_block    = self.setup_input.get('eta_block', self.default.get('eta_block'))
        # self.eta_surface  = self.setup_input.get('eta_surface', self.default.get('eta_surface'))
        self.eta_ill      = self.setup_input.get('eta_ill', self.default.get('eta_ill'))
        self.eta_q        = self.setup_input.get('eta_q', self.default.get('eta_q'))
        # self.eta_point    = self.setup_input.get('eta_point', self.default.get('eta_point'))
        self.T_cmb        = self.fixed_input.get('T_cmb')

    def get_inputs(self, file):
        """
        Read input from a .yaml file and return a dictionary
        Check for units and convert value into astropy.unit.Quantity if units given
        
        :param file: the .yaml file with parameters described as param_name: {value:param_value, unit:param_unit}
        :type file: str (file path)
        :retunr: a dictionary of astropy.unit.Quantities, if units given
        :rtype: dict
        """
        params = {}
        file = open(file, "r")
        inputs = yaml.load(file, Loader=Loader)
        for key in inputs.keys():
            if inputs[key]["unit"] == "none":
                params[key] = inputs[key]["value"]
            else:
                unit = getattr(u, inputs[key]["unit"])
                params[key] = inputs[key]["value"] * unit
        return params
