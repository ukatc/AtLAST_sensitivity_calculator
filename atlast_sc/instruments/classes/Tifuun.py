import astropy.units as u
from atlast_sc.instrument import Instrument

"""
TIFUUN instrument parameters
"""        
class Tifuun(Instrument):
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

    @property 
    def T_sys(self):
        return self._T_sys
    
    @T_sys.setter
    def T_sys(self, value):
        self._T_sys = value


    ################################################
    # Additional instrument specific methods below #
    ################################################

    # TODO: Adding the default system temp calculation in to test
    # Default instrument calculations in CLI
    def calculate_system_temperature(self, g, eta_eff, T_amb, T_sky,
                                     transmittance):
        """
        Returns system temperature, following calculation in [doc]

        :return: system temperature in Kelvin
        :rtype: astropy.units.Quantity
        """
        system_temp = (1 + g) / (eta_eff * transmittance) * \
            (self.T_rx
            + (eta_eff * T_sky)
            + ((1 - eta_eff) * T_amb)
            )
        self.T_sys = system_temp
        return system_temp

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
