import astropy.units as u
import numpy as np
from atlast_sc.atmosphere_params import AtmosphereParams
from atlast_sc.sefd import SEFD
from atlast_sc.system_temperature import SystemTemperature
from atlast_sc.efficiencies import Efficiencies


class Calculator:
    """ Calculator class that does the core calculation to get the output sensitivity or integration time. """
    def __init__(self, config):
        # TODO: the calculator should instantiate the Config object and accept inputs
        #       to the calculation as arguments
        self._calculation_inputs = config.calculation_inputs
        print('the calculation inputs are', self._calculation_inputs)
        self._calculation_params = self.calculate_parameters()
        print('the calculation params are', self._calculation_params)
        self.config = self.calculate_parameters(config)
        print('the config is', config)

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


    def calculate_parameters(self):
        """
        Performs the calculations required to produce the final set of parameters
        required for the sensitivity calculation,
        and outputs the sensitivity / integration time as required.

        :param calculation_inputs:
        :type calculation_inputs:
        :return: 
        """

        calculation_params = {}
        # Calculate area of dish & add to parameters
        calculation_params.area = np.pi * self._calculation_inputs.dish_radius.value ** 2

        atm = AtmosphereParams( 
            self._calculation_inputs.obs_freq,
            self._calculation_inputs.weather,
            self._calculation_inputs.elevation)
        # Perform atmospheric model calculation and add
        # opacity and temperature to config parameters
        calculation_params.tau_atm = atm.tau_atm()
        calculation_params.T_atm = atm.T_atm()

        eta = Efficiencies(
            self._calculation_inputs.eta_ill,
            self._calculation_inputs.eta_q,
            self._calculation_inputs.eta_spill,
            self._calculation_inputs.eta_block,
            self._calculation_inputs.eta_pol,
            self._calculation_inputs.eta_r)
        # Perform efficiency calculations
        # TODO eta_s() currently not implemented, placeholder value only
        calculation_params.eta_a = eta.eta_a(self._calculation_inputs.obs_freq, self._calculation_inputs.surface_rms)
        calculation_params.eta_s = eta.eta_s()

        # Calculate the system temperature
        T_sys = SystemTemperature(
            self._calculation_inputs.T_rx,
            self._calculation_inputs.T_cmb,
            self._calculation_inputs.T_atm,
            self._calculation_inputs.T_amb,
            self._calculation_inputs.tau_atm
            ).system_temperature(
                self._calculation_inputs.g,
                self._calculation_inputs.eta_eff)

        # Calculate source equivalent flux density
        sefd = SEFD.calculate(
            T_sys, 
            self._calculation_inputs.area,
            self._calculation_inputs.eta_a)
        calculation_params.sefd = sefd

        return calculation_params


