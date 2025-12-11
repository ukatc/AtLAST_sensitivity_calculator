import re
import astropy.units as u
from atlast_sc.instrument import Instrument

import bisect
from typing import List

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

    @property 
    def T_sys(self):
        return self._T_sys
    
    @T_sys.setter
    def T_sys(self, value):
        self._T_sys = value

    ################################################
    # Additional instrument specific methods below #
    ################################################

    def calculate_system_temperature(self, eta_eff, T_amb, T_sky,
                                     transmittance):
        """
        Returns system temperature, following calculation in [doc]

        :return: system temperature in Kelvin
        :rtype: astropy.units.Quantity
        """
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
        temp = None
        temp_index_count = 0
        for range in freq_ranges:
            if obs_freq >= range[0] and obs_freq <= range[1]:
                if temp == None: # If there is not an assigned temp already
                    # NOTE: This allows us to do open range assignments to temperatures
                    temp = temp_options[temp_index_count] * u.K
            # Only increase the temperature option index if the next increment
            # is within the total amount of temperature options
            if temp_index_count+1 < len(temp_options):
                temp_index_count += 1
        self.T_rx = temp
        
        return temp
    
    @staticmethod
    def _set_default_receiver_temp(receiver_temp_options_and_unit):
        """
        Sets default receiver temperature, currently chooses first receiver
        temp option as default.

        :return: receiver temperature in Kelvin
        :rtype: astropy.units.Quantity
        """
        temp_options = receiver_temp_options_and_unit['values']
        temp = temp_options[0] # first receiver temp option
        temp = u.Quantity(temp, receiver_temp_options_and_unit['unit'])
        return temp