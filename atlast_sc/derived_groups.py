from pathlib import Path
from scipy.interpolate import interp2d
import numpy as np
import astropy.units as u
from astropy import constants


class AtmosphereParams:
    """
    Class used to retrieve atmospheric parameters from a model.

    The AM model was used to produce a grid of T_atm and tau_atm.
    (Use of AM model described in am_code/REAME.md.)
    The code  interpolates over the grids to get the correct values for tau_atm
    and T_atm.
    """

    _STATIC_DATA_PATH = Path(__file__).resolve().parents[0] / "static"

    _WEATHER = [5, 25, 50, 75, 95]
    _T_ATM_PATH = _STATIC_DATA_PATH / "lookups" / "am_ACT_T_annual.txt"
    _TAU_ATM_PATH = _STATIC_DATA_PATH / "lookups" / "am_ACT_tau_annual.txt"

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

        T_atm_table = np.genfromtxt(AtmosphereParams._T_ATM_PATH)
        tau_atm_table = np.genfromtxt(AtmosphereParams._TAU_ATM_PATH)
        # TODO: interp2d is deprecated:
        #   see https://docs.scipy.org/doc/scipy/reference/generated
        #       /scipy.interpolate.interp2d.html
        self._interp_T_atm = interp2d(T_atm_table[:, 0],
                                      AtmosphereParams._WEATHER,
                                      T_atm_table[:, 1:].T)
        self._interp_tau_atm = interp2d(tau_atm_table[:, 0],
                                        AtmosphereParams._WEATHER,
                                        tau_atm_table[:, 1:].T)

        self._tau_atm = self._calculate_atmospheric_tau_factor()
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

    def _calculate_atmospheric_tau_factor(self):
        """
        Calculate the atmospheric tau factor tau_atm

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
        return (5 * constants.h * self._obs_freq.to(u.Hz)
                / constants.k_B).to(u.K)

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
