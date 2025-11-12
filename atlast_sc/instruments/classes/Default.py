import astropy.units as u
from astropy import constants
from atlast_sc.instrument import Instrument
from atlast_sc.data import Data

"""
Default instrument parameters
"""        
class Default(Instrument):
    def __init__(self, data):
        super().__init__(data)
        self._T_rx = self._set_default_receiver_temp()

    ##################################
    # Instrument specific parameters #
    ##################################
        
    @property 
    def T_rx(self):
        return self._T_rx
    
    @T_rx.setter
    def T_rx(self, value):
        self._T_rx = value

    ################################################
    # Additional instrument specific methods below #
    ################################################

    def calculate_receiver_temp(self, obs_freq):
        temp = (5 * constants.h * obs_freq / constants.k_B).to(u.K)
        self.T_rx = temp
        return temp

    @staticmethod
    def _set_default_receiver_temp():
        default_obs_freq = u.Quantity(Data.obs_frequency.default_value,
                                        Data.obs_frequency.default_unit)
        return (5 * constants.h * default_obs_freq / constants.k_B).to(u.K)