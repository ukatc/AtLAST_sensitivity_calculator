import numpy as np
from astropy.constants import k_B
from astropy.constants import h
from astropy import units as u


class Temperature:
    """
    Contains all the relevant temperatures that input to the total system
    temperature, T_sys
    """

    def __init__(self, obs_freq, T_cmb, T_atm, T_amb, tau_atm):
        self._T_cmb = T_cmb
        self._T_rx = Temperature._calculate_receiver_temperature(obs_freq)
        self._T_amb = T_amb
        self._T_atm = T_atm
        self._tau_atm = tau_atm
        self._transmittance = Temperature._calculate_transmittance(tau_atm)
        self._T_sky = self._calculate_sky_temperature()

    @property
    def T_cmb(self):
        return self._T_cmb

    @property
    def T_rx(self):
        return self._T_rx

    @property
    def T_amb(self):
        return self._T_amb

    @property
    def T_atm(self):
        return self._T_atm

    @property
    def tau_atm(self):
        return self._tau_atm

    @property
    def transmittance(self):
        return self._transmittance

    @property
    def T_sky(self):
        return self._T_sky

    def system_temperature(self, g, eta_eff):
        """
        Returns system temperature, following calculation in [doc]

        :param g: sideband ratio
        :type g: int
        :param eta_eff: forward efficiency
        :type eta_eff: float
        :return: system temperature in Kelvin
        :rtype: astropy.units.Quantity
        """
        return ((1 + g) / eta_eff * self.transmittance) \
            * self.T_rx \
            + (eta_eff * self.T_sky) + \
            ((1 - eta_eff) * self.T_amb)

    @staticmethod
    def _calculate_receiver_temperature(obs_freq):
        return (5 * h * obs_freq.to(u.Hz) / k_B).to(u.K)

    @staticmethod
    def _calculate_transmittance(tau_atm):
        return np.exp(-tau_atm)

    def _calculate_sky_temperature(self):
        return self.T_atm * (1 - self.transmittance) + self.T_cmb
