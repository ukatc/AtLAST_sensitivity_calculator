from pathlib import Path
from scipy.interpolate import interp2d
import numpy as np
import astropy.units as u

# Plan is to use the AM model to produce a grid of T_atm and tau_atm
# This code can then interpolate over that grid to get correct values
# Using AM as described in /am-code/README.md

STATIC_DATA_PATH = Path(__file__).resolve().parents[0] / "static"

WEATHER = [5, 25, 50, 75, 95]
T_ATM_PATH = STATIC_DATA_PATH / "lookups" / "am_ACT_T_annual.txt"
TAU_ATM_PATH = STATIC_DATA_PATH / "lookups" / "am_ACT_tau_annual.txt"


class AtmosphereParams:
    """
    Class used to retrieve atmospheric parameters from a model.

    The AM model was used to produce a grid of T_atm and tau_atm.
    (Use of AM model described in am_code/REAME.md.)
    The code  interpolates over the grids to get the correct values for tau_atm
    and T_atm.
    """

    def __init__(self, obs_freq, weather, elevation):
        """ AtmosphereParams class constructor.

        :param obs_freq: the central observing frequency
        :type obs_freq: astropy.units.Quantity
        :param weather: the precipitable water vapour
        :type weather: astropy.units.Quantity
        """
        self._obs_freq = obs_freq
        self._weather = weather
        self._elevation = elevation

        T_atm_table = np.genfromtxt(T_ATM_PATH)
        tau_atm_table = np.genfromtxt(TAU_ATM_PATH)
        # TODO: interp2d is deprecated:
        #   see https://docs.scipy.org/doc/scipy/reference/generated
        #       /scipy.interpolate.interp2d.html
        self._interp_T_atm = interp2d(T_atm_table[:, 0],
                                      WEATHER, T_atm_table[:, 1:].T)
        self._interp_tau_atm = interp2d(tau_atm_table[:, 0],
                                        WEATHER, tau_atm_table[:, 1:].T)

        self._tau_atm = self._calculate_transmittance()
        self._T_atm = self._calculate_temperature()

    @property
    def tau_atm(self):
        """
        Get the atmospheric transmittance
        """
        return self._tau_atm

    @property
    def T_atm(self):
        """
        Get the atmospheric temperature
        """
        return self._T_atm

    def _calculate_transmittance(self):
        """
        Calculate the atmospheric transmittance tau_atm

        :return: Atmospheric transmittance
        :rtype: astropy.units.Quantity
        """
        tau_z = self._interp_tau_atm(self._obs_freq, self._weather)
        zenith = 90.0 * u.deg - self._elevation
        tau_atm = tau_z / np.cos(zenith)
        return tau_atm[0]

    def _calculate_temperature(self):
        """
        Calculate the atmospheric temperature T_atm

        :return: Atmospheric temperature
        :rtype: astropy.units.Quantity
        """
        return self._interp_T_atm(self._obs_freq, self._weather)[0] * u.K
