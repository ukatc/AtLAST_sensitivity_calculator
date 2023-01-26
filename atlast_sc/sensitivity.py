import astropy.units as u
import numpy as np
from atlast_sc.atmosphere_params import AtmosphereParams
from atlast_sc.sefd import SEFD
from atlast_sc.system_temperature import SystemTemperature
from atlast_sc.efficiencies import Efficiencies


class Sensitivity:
    """ Calculator class that does the core calculation to get the output sensitivity or integration time. """
    def __init__(self, config):
        self.config = self.resolve_config(config)

    def sensitivity(self, t_int):
        """
        Return sensitivity of telescope (Jansky) for a given integration time t_int

        :param t_int: integration time 
        :type t_int: astropy.units.Quantity
        :return: sensitivity in Janksy
        :rtype: astropy.units.Quantity
        """
        sensitivity = (
            self.config.sefd
            / (self.config.eta_s * np.sqrt(self.config.n_pol * self.config.bandwidth * t_int))
            * np.exp(self.config.tau_atm)
        )
        return sensitivity.to(u.Jy)

    def t_integration(self, sensitivity):
        """
        Return integration time required for some sensitivity to be reached.

        :param sensitivity: required sensitivity in Jansky
        :type sensitivity: astropy.units.Quantity
        :return: integration time in seconds
        :rtype: astropy.units.Quantity
        """
        t_int = ((self.config.sefd * np.exp(self.config.tau_atm))/ (sensitivity * self.config.eta_s)) ** 2 / (
            self.config.n_pol * self.config.bandwidth
        )
        return t_int.to(u.s)

    @classmethod
    def resolve_config(cls, config):
        """
        Performs the calculations required to produce the final set of parameters
        required for the sensitivity calculation,
        and outputs the sensitivity / integration time as required.

        :param config: a ``Config`` instance
        :type config: ``configs.config.Config`` object
        :return: 
        """

        # Calculate area of dish & add to parameters
        config.area = np.pi * config.dish_radius**2

        atm = AtmosphereParams( 
            config.obs_freq, 
            config.weather,
            config.elevation)
        # Perform atmospheric model calculation and add
        # opacity and temperature to config parameters
        config.tau_atm = atm.tau_atm()
        config.T_atm = atm.T_atm()

        eta = Efficiencies(
            config.eta_ill, 
            config.eta_q, 
            config.eta_spill, 
            config.eta_block, 
            config.eta_pol, 
            config.eta_r)
        # Perform efficiency calculations
        # TODO eta_s() currently not implemented, placeholder value only
        config.eta_a = eta.eta_a(config.obs_freq, config.surface_rms)
        config.eta_s = eta.eta_s()

        # Calculate the system temperature
        T_sys = SystemTemperature(
            config.T_rx, 
            config.T_cmb, 
            config.T_atm, 
            config.T_amb, 
            config.tau_atm
            ).system_temperature(
                config.g, 
                config.eta_eff)

        # Calculate source equivalent flux density
        sefd = SEFD.calculate(
            T_sys, 
            config.area, 
            config.eta_a)
        config.sefd = sefd

        return config


