from astropy import constants
import astropy.units as u
import numpy as np


class Efficiencies:
    """
    Calculates efficiency terms
    """

    def __init__(self, obs_freq, surface_rms, eta_ill, eta_spill, eta_block,
                 eta_pol):
        """
        :param obs_freq: observing frequency
        :type obs_freq: astropy.units.Quantity
        :param surface_rms: surface smoothness
        :type surface_rms: astropy.units.Quantity
        :param eta_ill: illumination efficiency
        :type eta_ill: float
        :param eta_spill: spillover efficiency
        :type eta_spill: float
        :param eta_block: lowered efficiency due to blocking
        :type eta_block: float
        :param eta_pol: polarisation efficiency
        :type eta_pol: float
        """
        self._obs_freq = obs_freq
        self._surface_rms = surface_rms
        self._eta_ill = eta_ill
        self._eta_spill = eta_spill
        self._eta_block = eta_block
        self._eta_pol = eta_pol
        self._eta_a = self._calculate_eta_a()

    @property
    def eta_a(self):
        """
        Get the dish efficiency
        """
        return self._eta_a

    @property
    def eta_s(self):
        """
        Get the system efficiency
        """

        # PLACEHOLDER - more/different efficiencies may need to be added
        return 0.99

    def _calculate_eta_a(self):
        """
        Calculate the dish efficiency, used in the SEFD
        calculation using Ruze formula.

        :return: dish efficiency
        :rtype: float
        """
        wavelength = (constants.c / self._obs_freq).to(u.m)

        eta_a_quantity = self._eta_ill * self._eta_spill * self._eta_pol * \
            self._eta_block * \
            np.exp(-(4 * np.pi * self._surface_rms / wavelength)**2)

        return eta_a_quantity.value
