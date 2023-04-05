from astropy import constants
import astropy.units as u
import numpy as np


class Efficiencies:
    """
    All of the efficiency factors need to come in here...
    """
    def __init__(self, eta_ill, eta_spill, eta_block, eta_pol, eta_r):
        """
        At present, a placeholder method just to hold some efficiencies.

        :param eta_ill: the illumination factor
        :type eta_ill: float
        :param eta_spill: spill-over factor
        :type eta_spill: float
        :param eta_block: blocking factor
        :type eta_block: float

        """
        self.eta_ill = eta_ill
        self.eta_spill = eta_spill
        self.eta_block = eta_block
        self.eta_pol = eta_pol
        self.eta_r = eta_r

    def eta_a(self, obs_freq, surface_rms):
        """
        Return the dish efficiency eta_a that needs to go into the SEFD
        calculation Using Ruze formula.

        :param obs_freq: the observing frequency in GHz
        :type obs_freq: astropy.units.Quantity
        :param surface_rms: the surface accuracy in micron
        :type surface_rms: astropy.units.Quantity
        :return: dish efficiency
        :rtype: astropy.units quantity
        """
        wavelength = (constants.c / obs_freq).to(u.m)
        return self.eta_ill * self.eta_spill * self.eta_r * self.eta_pol * \
            self.eta_block * \
            np.exp(-(4 * np.pi * surface_rms / wavelength)**2)

    @classmethod
    def eta_s(cls):
        """
        Return the system efficiency eta_s that goes into the sensitivity
        calculation
        PLACEHOLDER - more/different efficiencies may need to be added

        :return: system efficiency
        :rtype: astropy.units quantity
        """
        return 0.99
