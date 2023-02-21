import astropy.units as u
import numpy as np
from atlast_sc.atmosphere_params import AtmosphereParams
from atlast_sc.sefd import SEFD
from atlast_sc.system_temperature import SystemTemperature
from atlast_sc.efficiencies import Efficiencies
from atlast_sc.models import CalculatedParams
from atlast_sc.models import SensitivityCalculatorParameters
from atlast_sc.config import Config
from atlast_sc.utils import update_input_param


class Calculator:
    """
    Calculator class that provides an interface to the main
    calculator functionality and performs the core calculations
    to determine the output sensitivity or integration time.
    """

    def __init__(self, inputs=None, setup='standard', file_path=None,
                 setup_inputs_file=None, default_inputs_file=None):
        # TODO: provide accessor methods for properties
        # TODO: get a list of properties that are editable and provide setters

        self._calculation_params = None

        # Store the input parameters used to initialise the calculator
        self._config = Config(inputs, setup, file_path, setup_inputs_file,
                              default_inputs_file)

        # Calculate and store the remaining parameters used in the
        # calculation
        self.generate_calculation_params(self._config.calculation_inputs)

    #################################################
    # Public methods for performing sensitivity and #
    # integration time calculations                 #
    #################################################

    def calculate_sensitivity(self, t_int):
        """
        Return sensitivity of telescope (Jansky) for a
        given integration time t_int

        :param t_int: integration time
        :type t_int: astropy.units.Quantity
        :return: sensitivity in Janksy
        :rtype: astropy.units.Quantity
        """
        sensitivity = (
                self.calculation_params['sefd']
                / (self.calculation_params['eta_s']
                   * np.sqrt(
                    self.calculation_params['n_pol']
                    * self.calculation_params['bandwidth']
                    * t_int
                ))
                * np.exp(self.calculation_params['tau_atm'])
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

        t_int = ((self.calculation_params['sefd']
                  * np.exp(self.calculation_params['tau_atm']))
                 / (sensitivity * self.calculation_params['eta_s'])) ** 2 \
            / (self.calculation_params['n_pol']
                * self.calculation_params['bandwidth'])

        return t_int.to(u.s)

    def generate_calculation_params(self, calculation_inputs=None):

        # Default to the stored calculation inputs if none are supplied
        calculation_inputs = calculation_inputs \
            if calculation_inputs\
            else self._calculation_params.calculation_inputs
        # Use the input values to calculate the remaining parameters
        # used in the calculation
        calculated_params = \
            self._calculate_parameters(calculation_inputs)

        # Store all the inputs and calculated params used
        # in the sensitivity and integration time calculations
        self._calculation_params = \
            SensitivityCalculatorParameters(
                calculation_inputs=calculation_inputs,
                calculated_params=calculated_params)

    def reset_calculator(self):
        # Reset the config calculation inputs to their original values
        self._config.calculation_inputs = self._config.original_inputs
        # Regenerate the calculation parameters from the original inputs
        self.generate_calculation_params(self._config.original_inputs)

    ###################################################
    # Getters and setters for user input parameters   #
    ###################################################
    # TODO: move these getters and setters to Config object?

    @property
    def t_int(self):
        return self._calculation_params.calculation_inputs.t_int

    @t_int.setter
    def t_int(self, value):
        # TODO: Setting this value in the on the inputs feels wrong.
        #  This may be a calculated param. Allowing the user to change it
        #  without restriction may lead to inaccurate output if they perform
        #  the sensitivity calculation, change the integration time, then
        #  store or use those stored values.
        #  Need separate "outputs" properties that are used for
        #  subsequent calculations and/or storing results?
        self._calculation_params.calculation_inputs.t_int = value

    @property
    def sensitivity(self):
        return self._calculation_params.calculation_inputs.sensitivity

    @sensitivity.setter
    def sensitivity(self, value):
        # TODO: Setting this value in the on the inputs feels wrong.
        #  This may be a calculated param. Allowing the user to change it
        #  without restriction may lead to inaccurate output if they perform
        #  the sensitivity calculation, change the integration time, then
        #  store or use those stored values.
        #  Need separate "outputs" properties that are used for
        #  subsequent calculations and/or storing results?
        self._calculation_params.calculation_inputs.sensitivity = value

    @property
    def bandwidth(self):
        return self._calculation_params.calculation_inputs.bandwidth

    @bandwidth.setter
    @update_input_param
    def bandwidth(self, value):
        self._calculation_params.calculation_inputs.bandwidth = value

    @property
    def obs_frequency(self):
        return self._calculation_params.calculation_inputs.obs_freq

    @obs_frequency.setter
    @update_input_param
    def obs_frequency(self, value):
        self._calculation_params.calculation_inputs.obs_freq = value

    @property
    def n_pol(self):
        return self._calculation_params.calculation_inputs.n_pol

    @n_pol.setter
    @update_input_param
    def n_pol(self, value):
        self._calculation_params.calculation_inputs.n_pol = value

    @property
    def weather(self):
        return self._calculation_params.calculation_inputs.weather

    @weather.setter
    @update_input_param
    def weather(self, value):
        self._calculation_params.calculation_inputs.weather = value

    @property
    def elevation(self):
        return self._calculation_params.calculation_inputs.elevation

    @elevation.setter
    @update_input_param
    def elevation(self, value):
        self._calculation_params.calculation_inputs.elevation = value

    @property
    def calculation_params(self):
        """
        Parameters used to perform the calculation
        (input params and calculated params)
        """
        return self._calculation_params.calculator_params()

    @staticmethod
    def _calculate_parameters(calculation_inputs):
        """
        Performs the calculations required to produce the
        final set of parameters required for the sensitivity
        calculation, and outputs the sensitivity or integration
        time as required.

        :return:
        """

        # TODO: can do better with this...

        # Perform atmospheric model calculation
        atm = AtmosphereParams(
            calculation_inputs.obs_freq,
            calculation_inputs.weather,
            calculation_inputs.elevation
        )

        T_atm = atm.T_atm()
        tau_atm = atm.tau_atm()

        # Perform efficiencies calculation
        eta = Efficiencies(
            calculation_inputs.eta_ill,
            calculation_inputs.eta_q,
            calculation_inputs.eta_spill,
            calculation_inputs.eta_block,
            calculation_inputs.eta_pol,
            calculation_inputs.eta_r
        )

        eta_a = eta.eta_a(calculation_inputs.obs_freq,
                          calculation_inputs.surface_rms)
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
