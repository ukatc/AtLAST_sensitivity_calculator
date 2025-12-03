from pathlib import Path
from scipy.interpolate import RegularGridInterpolator
import numpy as np
import astropy.units as u
from astropy import constants
from atlast_sc.parameters.instrument_specific_parameters import InstrumentSpecificParameters


class AtmosphereParams:
    """
    Class used to retrieve atmospheric parameters from a model.

    The AM model was used to produce a grid of T_atm and tau_atm.
    (Use of AM model described in am_code/REAME.md.)
    The code interpolates over the grids to get the correct values for tau_atm
    and T_atm.
    """

    _STATIC_DATA_PATH = Path(__file__).resolve().parents[0] / "static"

    _WEATHER = [5, 25, 50, 75, 95]
    _T_ATM_PATH = _STATIC_DATA_PATH / "lookups" / "am_ACT_T_ext_annual.txt"
    _TAU_ATM_PATH = _STATIC_DATA_PATH / "lookups" / "am_ACT_tau_ext_annual.txt"

    def __init__(self):

        self.T_atm_table = np.genfromtxt(AtmosphereParams._T_ATM_PATH)
        self.tau_atm_table = np.genfromtxt(AtmosphereParams._TAU_ATM_PATH)
        # the temperature values obtained by interpolating over the ATM tables are rescaled by the opacity at zenith to obtain T_atm (see the discussion around Eq. 7-9 in the ALMA Memo 602 (https://library.nrao.edu/public/memos/alma/main/memo602.pdf))
        self.T_atm_table[:,1:] = self.T_atm_table[:,1:] / (1.00 - np.exp(-self.tau_atm_table[:,1:]))

        self._interp_T_atm = RegularGridInterpolator((self.T_atm_table[:, 0],
                                                      AtmosphereParams._WEATHER),
                                                      self.T_atm_table[:, 1:])

        self._interp_tau_atm = RegularGridInterpolator((self.tau_atm_table[:, 0],
                                                        AtmosphereParams._WEATHER),
                                                        self.tau_atm_table[:, 1:])

    def calculate_atmospheric_temperature(self, obs_freq, weather):
        """
        Calculate the atmospheric temperature T_atm

        :param obs_freq: the central observing frequency
        :type obs_freq: astropy.units.Quantity
        :param weather: the precipitable water vapour
        :type weather: float
        :return: Atmospheric temperature
        :rtype: astropy.units.Quantity
        """
        return float(self._interp_T_atm((obs_freq, weather))) * u.K
    
    def calculate_transmittance(self, obs_freq, weather, elevation):
        """
        Calculate the atmospheric transmittance

        :param obs_freq: the central observing frequency
        :type obs_freq: astropy.units.Quantity
        :param weather: the precipitable water vapour
        :type weather: float
        :param elevation: elevation of the target
        :type elevation: astropy.units.Quantity
        :return: Atmospheric transmittance
        :rtype: astropy.units.Quantity
        """
        tau_z = self._interp_tau_atm((obs_freq, weather))
        zenith = 90.0 * u.deg - elevation
        tau_atm = tau_z / np.cos(zenith)
        transmittance = np.exp(-tau_atm)
        
        return float(transmittance)


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

        self._eta_a = \
            Efficiencies._calculate_eta_a(obs_freq, surface_rms, eta_ill,
                                          eta_spill, eta_block, eta_pol)

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

    @staticmethod
    def _calculate_eta_a(obs_freq, surface_rms, eta_ill, eta_spill,
                         eta_block, eta_pol):
        """
        Calculate the dish efficiency, used in the SEFD
        calculation using Ruze formula.

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
        :return: dish efficiency
        :rtype: float
        """

        wavelength = (constants.c / obs_freq).to(u.m)

        eta_a_quantity = eta_ill * eta_spill * eta_pol * \
            eta_block * \
            np.exp(-(4 * np.pi * surface_rms / wavelength)**2)

        return eta_a_quantity.value


class Temperatures:
    """
    Calculates temperature terms
    """

    def __init__(self, inst_module, obs_freq, T_cmb, T_amb, eta_eff, T_atm, transmittance):
        self._T_rx = inst_module.calculate_receiver_temp(obs_freq=obs_freq)
        self._T_sky = T_atm * (1 - transmittance) + T_cmb
        self._T_sys = inst_module.calculate_system_temperature(eta_eff, T_amb, self.T_sky,
                                     transmittance)

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

    @property
    def T_sky(self):
        """
        Get the sky temperature
        """
        return self._T_sky