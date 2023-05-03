import numpy as np
from astropy.constants import k_B
from astropy.constants import h
from astropy import units as u


class Temperatures:
    """
    Calculates temperature terms
    """

    def __init__(self, obs_freq, T_cmb, T_amb, g, eta_eff, atmosphere_params):
        self._T_cmb = T_cmb
        self._obs_freq = obs_freq
        self._g = g
        self._eta_eff = eta_eff
        self._T_amb = T_amb
        self._T_atm = atmosphere_params.T_atm
        self._tau_atm = atmosphere_params.tau_atm
        self._T_rx = self._calculate_receiver_temperature()
        self._transmittance = self._calculate_transmittance()
        self._T_sys = self._calculate_system_temperature()

    @property
    def T_rx(self):
        """
        Get the receiver temperature
        """
        return self._T_rx

    @property
    def T_sys(self):
        """
        Get the system temperature
        """
        return self._T_sys

    def _calculate_system_temperature(self):
        """
        Returns system temperature, following calculation in [doc]

        :return: system temperature in Kelvin
        :rtype: astropy.units.Quantity
        """

        sky_temp = self._calculate_sky_temperature()

        return (1 + self._g) / (self._eta_eff * self._transmittance) * \
               (self.T_rx
                + (self._eta_eff * sky_temp)
                + ((1 - self._eta_eff) * self._T_amb)
                )

    def _calculate_receiver_temperature(self):
        """
        Calculate the receiver temperature
        """
        return (5 * h * self._obs_freq.to(u.Hz) / k_B).to(u.K)

    def _calculate_transmittance(self):
        """
        Calculate the transmittance
        """
        return np.exp(-self._tau_atm)

    def _calculate_sky_temperature(self):
        """
        Calculate the sky temperature
        """
        return self._T_atm * (1 - self._transmittance) + self._T_cmb
