import astropy.units as u
from atlast_sc.instrument import Instrument

"""
MUSCAT instrument parameters
"""        
class Muscat(Instrument):
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
        # NOTE: This will be populated with instrument specific 
        # receiver temperature calculation equation.
        temp_option = float(self.receiver_temp_options_and_unit['values'][0])
        temp = temp_option * u.K
        self.T_rx = temp
        return temp

    @staticmethod
    def _set_default_receiver_temp(receiver_temp_options_and_unit):
        receiver_temp = u.Quantity(receiver_temp_options_and_unit['values'][0],
                                    u.K)
        return receiver_temp
