import re
import astropy.units as u
from atlast_sc.instrument import Instrument

"""
FINER instrument parameters
"""        
class Finer(Instrument):
    def __init__(self, data):
        super().__init__(data)
        self._T_rx = self._set_default_receiver_temp(self.receiver_temp_options_and_unit)

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
        temp_options = re.findall(r"[\d.]+", 
                           self.receiver_temp_options_and_unit['values'][0])
        temp_options = [float(temp) for temp in temp_options]

        obs_freq = obs_freq.value 
        if obs_freq >= 120.0 and obs_freq <= 210.0:
            temp = temp_options[0] * u.K
        elif obs_freq > 210.0 and obs_freq <= 360.0:
            temp = temp_options[1] * u.K
        self.T_rx = temp
        return temp
    
    @staticmethod
    def _set_default_receiver_temp(receiver_temp_options_and_unit):
        temp_options = re.findall(r"[\d.]+", 
                           receiver_temp_options_and_unit['values'][0])
        temp_options = [float(temp) for temp in temp_options]
        # NOTE: Currently chooses first receiver temp option as default
        temp = temp_options[0]
        temp = u.Quantity(temp, receiver_temp_options_and_unit['unit'])
        return temp
