import re
import astropy.units as u
from atlast_sc.instrument import Instrument

"""
SEPIA instrument parameters
"""        
class Sepia(Instrument):
    def __init__(self, data):
        super().__init__(data)
        self._T_rx = None

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

    def calculate_system_temperature(self, obs_freq, bandwidth, T_cmb, eta_eff, T_atm, 
                                     T_amb, T_sky, transmittance, n_pol):
        """
        Returns system temperature, following calculation in [doc]

        :return: system temperature in Kelvin
        :rtype: astropy.units.Quantity
        """
        self.T_rx = self.calculate_receiver_temp(obs_freq)
        system_temp = 1 / (eta_eff * transmittance) * \
            (self.T_rx
            + (eta_eff * T_sky)
            + ((1 - eta_eff) * T_amb)
            )
        self.T_sys = system_temp
        return system_temp

    def calculate_receiver_temp(self, obs_freq):
        """
        Returns receiver temperature, following calculation in [doc]

        :return: receiver temperature in Kelvin
        :rtype: astropy.units.Quantity
        """
        # Extract instrument receiver temperature options
        temp_options = self.receiver_temp_options_and_unit['values']
        temp_options = [float(temp) for temp in temp_options]
        # Extract instrument observing frequency ranges
        freq_options = self.obs_freq_ranges_and_unit['ranges']
        freq_ranges = []
        for freq_range in freq_options:
            range = re.findall(r"[\d.]+", freq_range)
            range = [float(val) for val in range] # convert to float ranges
            freq_ranges.append(range) 

        obs_freq = obs_freq.value
        t_rx_low = temp_options[0] # low receiver temp specified in the YAML
        t_rx_high = temp_options[1] # high receiver temp specified in the YAML
        freq_high_min = freq_ranges[1][0] # min freq of second obs_freq range
        freq_high_max = freq_ranges[1][1] # max freq of second obs_freq range

        temp = None
        # If the observing frequency is in the first range 
        if obs_freq >= freq_ranges[0][0] and obs_freq <= freq_ranges[0][1]:
            temp = t_rx_low * u.K
        # If the observing frequency is in the second range
        elif obs_freq > freq_ranges[1][0] and obs_freq <= freq_ranges[1][1]:
            temp = ( t_rx_low + (t_rx_high - t_rx_low) * (obs_freq - freq_high_min) \
            / (freq_high_max - freq_high_min) ) * u.K
        self.T_rx = temp
        return temp