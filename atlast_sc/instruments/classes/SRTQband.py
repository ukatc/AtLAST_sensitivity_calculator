import re
import astropy.units as u
from atlast_sc.instrument import Instrument
from atlast_sc.derived_groups import noise_temperature
import numpy as np


"""
SRTQband instrument parameters
"""        


_NUMBER_RE = re.compile(r"\d+(?:\.\d+)?")

def _parse_ranges(range_strings):
    """Parse ['(33.0-50.0)', ...] into [(33.0, 50.0), ...]."""
    ranges = []
    for s in range_strings:
        values = [float(v) for v in _NUMBER_RE.findall(str(s))]
        if len(values) != 2:
            raise ValueError(f"Cannot parse frequency range {s!r}")
        lo, hi = sorted(values)
        ranges.append((lo, hi))
    return ranges


class SRTQband(Instrument):
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





    def calculate_system_temperature(self, obs_freq, bandwidth, eta_eff, 
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
                + ((1 - eta_eff) * noise_temperature(T_amb, obs_freq))
                )
            self.T_sys = system_temp
            return system_temp

    def calculate_receiver_temp(self, obs_freq):
        """
        Returns receiver temperature, following calculation in [doc].

        The last frequency range carries the T_rx law:

        - one value in the YAML      -> constant T_rx
        - two values (low, high)     -> linear from low at the range minimum
                                        to high at the range maximum
        - frequencies in earlier ranges get the low value (SEPIA-like case)

        :param obs_freq: observing frequency
        :type obs_freq: astropy.units.Quantity
        :return: receiver temperature
        :rtype: astropy.units.Quantity
        :raises ValueError: if obs_freq is outside all ranges
        """
        temps = [float(t) for t in self.receiver_temp_options_and_unit['values']]
        temp_unit = u.Unit(self.receiver_temp_options_and_unit.get('unit', 'K'))
        freq_unit = u.Unit(self.obs_freq_ranges_and_unit.get('unit', 'GHz'))
        ranges = _parse_ranges(self.obs_freq_ranges_and_unit['ranges'])

        nu = obs_freq.to_value(freq_unit)

        if not any(lo <= nu <= hi for lo, hi in ranges):
            raise ValueError(
                f"Observing frequency {obs_freq} outside instrument ranges {ranges} {freq_unit}"
            )

        # np.interp clamps outside [lo, hi] -> earlier ranges get temps[0]
        lo, hi = ranges[-1]
        t_rx = np.interp(nu, [lo, hi], [temps[0], temps[-1]])

        self.T_rx = t_rx * temp_unit
        return self.T_rx