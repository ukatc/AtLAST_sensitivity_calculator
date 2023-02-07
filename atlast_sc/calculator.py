import astropy.units as u
import numpy as np
from atlast_sc.atmosphere_params import AtmosphereParams
from atlast_sc.sefd import SEFD
from atlast_sc.system_temperature import SystemTemperature
from atlast_sc.efficiencies import Efficiencies
from atlast_sc.inputs import CalculatedParams, SensitivityCalculatorParameters


class Calculator:
    """ Calculator class that does the core calculation to get the output sensitivity or integration time. """
    def __init__(self, config):
        # TODO: the calculator should instantiate the Config object and accept inputs
        #       to the calculation as arguments

        calculation_inputs = config.calculation_inputs
        calculated_params = self.calculate_parameters(calculation_inputs)

        # Store all the input and calculated param used for the sensitivity calculater
        self._sensitivity_calc_params = \
            SensitivityCalculatorParameters(calculation_inputs=calculation_inputs,
                                            calculated_params=calculated_params)

    def calculate_sensitivity(self, t_int):
        """
        Return sensitivity of telescope (Jansky) for a given integration time t_int

        :param t_int: integration time 
        :type t_int: astropy.units.Quantity
        :return: sensitivity in Janksy
        :rtype: astropy.units.Quantity
        """
        sensitivity = (
            self._sensitivity_calc_params.sefd
            / (self._sensitivity_calc_params.eta_s
               * np.sqrt(self._sensitivity_calc_params.n_pol
                         * self._sensitivity_calc_params.bandwidth * t_int))
            * np.exp(self._sensitivity_calc_params.tau_atm)
        )
        return sensitivity.to(u.Jy)

    def calculate_t_integration(self, sensitivity):
        """
        Return integration time required for some sensitivity to be reached.

        :param sensitivity: required sensitivity in Jansky
        :type sensitivity: astropy.units.Quantity
        :return: integration time in seconds
        :rtype: astropy.units.Quantity
        """
        t_int = ((self._sensitivity_calc_params.sefd
                  * np.exp(self._sensitivity_calc_params.tau_atm))
                 / (sensitivity * self._sensitivity_calc_params.eta_s)) ** 2 / \
                (self._sensitivity_calc_params.n_pol
                 * self._sensitivity_calc_params.bandwidth)

        return t_int.to(u.s)

    @property
    def t_int(self):
        return self._sensitivity_calc_params.t_int

    @property
    def sensitivity(self):
        return self._sensitivity_calc_params.sensitivity

    @property
    def sensitivity_calc_params(self):
        return self._sensitivity_calc_params

    @classmethod
    def calculate_parameters(cls, calculation_inputs):
        """
        Performs the calculations required to produce the final set of parameters
        required for the sensitivity calculation,
        and outputs the sensitivity / integration time as required.

        :return: 
        """

        # TODO: can do better with this...

        # Perform atmospheric model calculation
        atm = AtmosphereParams( 
            calculation_inputs.obs_freq,
            calculation_inputs.weather,
            calculation_inputs.elevation)

        T_atm = atm.T_atm()
        tau_atm = atm.tau_atm()

        # Perform efficiencies calculation
        eta = Efficiencies(
            calculation_inputs.eta_ill,
            calculation_inputs.eta_q,
            calculation_inputs.eta_spill,
            calculation_inputs.eta_block,
            calculation_inputs.eta_pol,
            calculation_inputs.eta_r)

        eta_a = eta.eta_a(calculation_inputs.obs_freq, calculation_inputs.surface_rms)
        eta_s = eta.eta_s()

        # Calculate the system temperature
        T_sys = SystemTemperature(
            calculation_inputs.T_rx,
            calculation_inputs.T_cmb,
            T_atm,
            calculation_inputs.T_amb,
            tau_atm
            ).system_temperature(
                calculation_inputs.g,
                calculation_inputs.eta_eff)

        # Calculate the dish area
        area = np.pi * calculation_inputs.dish_radius ** 2
        # Calculate source equivalent flux density
        sefd = SEFD.calculate(T_sys, area, eta_a)

        return CalculatedParams(tau_atm=tau_atm, T_atm=T_atm, eta_a=eta_a,
                                eta_s=eta_s, T_sys=T_sys, sefd=sefd, area=area)
