from pathlib import Path
import astropy.units as u
from scipy.interpolate import interp2d 
import numpy as np

# Plan is to use the AM model to produce a grid of T_atm and tau_atm
# This code can then interpolate over that grid to get correct values
# Using AM as described in /am-code/README.md

STATIC_DATA_PATH = Path(__file__).resolve().parents[0] / "static"

WEATHER = [5, 25, 50, 75, 95]
T_ATM_PATH = STATIC_DATA_PATH / "lookups" / "am_ACT_T_annual.txt"
TAU_ATM_PATH = STATIC_DATA_PATH / "lookups" / "am_ACT_tau_annual.txt"


class AtmosphereParams:
    """ Class used to retrieve atmospheric parameters from a model. """

    def __init__(self, obs_freq, weather, elevation):
        """ AtmosphereParams class constructor. 
        
        :param obs_freq: the central observing frequency
        :type obs_freq: astropy.units.Quantity
        :param weather: the precipitable water vapour
        :type weather: astropy.units.Quantity
        """
        self.obs_freq = obs_freq
        self.weather = weather
        self.elevation = elevation
        self.T_atm_table = np.genfromtxt(T_ATM_PATH)
        self.tau_atm_table = np.genfromtxt(TAU_ATM_PATH)
        self.interp_T_atm = interp2d(self.T_atm_table[:, 0], WEATHER, self.T_atm_table[:, 1:].T)
        self.interp_tau_atm = interp2d(self.tau_atm_table[:, 0], WEATHER, self.tau_atm_table[:, 1:].T)

    def tau_atm(self):
        """
        Return atmospheric transmittance tau_atm 

        :return: Atmospheric transmittance
        :rtype: astropy.units.Quantity
        """
        tau_z = self.interp_tau_atm(self.obs_freq, self.weather)
        zenith = 90.0 * u.deg - self.elevation
        tau_atm = tau_z / np.cos(zenith)
        tau_atm[self.elevation <= 0.0 * u.deg] = -1.0
        return tau_atm[0]

    def T_atm(self):
        """
        Return atmospheric temperature T_atm 

        :return: Atmospheric temperature
        :rtype: astropy.units.Quantity
        """
        return self.interp_T_atm(self.obs_freq, self.weather)[0] * u.K
