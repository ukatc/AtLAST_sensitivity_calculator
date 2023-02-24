import astropy.units as u
import numpy as np
from atlast_sc.atmosphere_params import AtmosphereParams
from atlast_sc.sefd import SEFD
from atlast_sc.system_temperature import SystemTemperature
from atlast_sc.efficiencies import Efficiencies
from atlast_sc.models import DerivedParams
from atlast_sc.models import SensitivityCalculatorParameters
from atlast_sc.config import Config
from atlast_sc.utils import update_input_param


class Calculator:
    """
    Calculator class that provides an interface to the main
    calculator functionality and performs the core calculations
    to determine the output sensitivity or integration time.
    """

    # def __init__(self, inputs=None, setup='standard', file_path=None,
    #              setup_inputs_file=None, default_inputs_file=None):
    def __init__(self, user_input={}, instrument_setup={}):
        # TODO: provide accessor methods for properties
        # TODO: get a list of properties that are editable and provide setters

        self._calculation_params = None

        # Store the input parameters used to initialise the calculator
        self._config = Config(user_input, instrument_setup)
        self._calculation_inputs = self._config.calculation_inputs
        # self._calculation_inputs.user_input.sensitivity = 0.1

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
                self.sefd
                / (self.eta_s
                   * np.sqrt(
                    self.n_pol
                    * self.bandwidth
                    * t_int
                ))
                * np.exp(self.tau_atm)
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

        t_int = ((self.sefd
                  * np.exp(self.tau_atm))
                 / (sensitivity *
                    self.eta_s)) ** 2 \
            / (self.n_pol
                * self.bandwidth)

        return t_int.to(u.s)

    def generate_calculation_params(self, calculation_inputs=None):

        # Default to the stored calculation inputs if none are supplied
        calculation_inputs = calculation_inputs \
            if calculation_inputs\
            else self._calculation_params.calculation_inputs
        # Use the input values to calculate the derived parameters
        # used in the calculation
        derived_params = \
            self._calculate_parameters(calculation_inputs)

        # Store all the inputs and calculated params used
        # in the sensitivity and integration time calculations
        self._calculation_params = \
            SensitivityCalculatorParameters(
                calculation_inputs=calculation_inputs,
                derived_params=derived_params)

    def reset_calculator(self):
        # Reset the config calculation inputs to their original values
        self._config.calculation_inputs = self._config.original_inputs
        # Regenerate the calculation parameters from the original inputs
        self.generate_calculation_params(self._config.original_inputs)

    # TODO: move these getters and setters to Config object?

    ###################################################
    # Getters and setters for user input parameters   #
    ###################################################

    # TODO t_int and sensitivity are a special case. They can be both
    #   set and calculated. Special care needs to be taken on setting them:
    #   they will have to be validated if they're set, but not calculated.
    #   Also, if they're set, the user needs to be warned if they then try
    #   to use Calculator values with redoing the senstivity/integration time
    #   calculation
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
        self._calculation_params.t_int = value

    @property
    def sensitivity(self):
        return self._calculation_params.calculation_inputs.sensitivity

    @sensitivity.setter
    @update_input_param
    def sensitivity(self, value):
        # TODO: Setting this value in the on the inputs feels wrong.
        #  This may be a calculated param. Allowing the user to change it
        #  without restriction may lead to inaccurate output if they perform
        #  the sensitivity calculation, change the integration time, then
        #  store or use those stored values.
        #  Need separate "outputs" properties that are used for
        #  subsequent calculations and/or storing results?

        print(hasattr(self._calculation_params.calculation_inputs,
                      'sensitivity'))
        # TODO: pick up from here. The line below is failing
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

    ####################################################################
    # Getters and a couple of setters for instrument setup parameters  #
    ####################################################################

    @property
    def g(self):
        return self._calculation_params.calculation_inputs.g

    @property
    def surface_rms(self):
        return self._calculation_params.calculation_inputs.surface_rms

    @property
    def dish_radius(self):
        return self._calculation_params.calculation_inputs.dish_radius

    @dish_radius.setter
    @update_input_param
    def dish_radius(self, value):
        # TODO Flag to the user somehow that they are varying an instrument
        #   setup parameter
        # TODO: the update function will fail because the InstrumetSetup
        #       model doesn't contain the field validator
        self._calculation_params.calculation_inputs.dish_radius = value

    @property
    def T_amb(self):
        return self._calculation_params.calculation_inputs.T_amb

    @property
    def T_rx(self):
        return self._calculation_params.calculation_inputs.T_rx

    @property
    def eta_eff(self):
        return self._calculation_params.calculation_inputs.eta_eff

    @property
    def eta_ill(self):
        return self._calculation_params.calculation_inputs.eta_ill

    @property
    def eta_q(self):
        return self._calculation_params.calculation_inputs.eta_q

    @property
    def eta_spill(self):
        return self._calculation_params.calculation_inputs.eta_spill

    @property
    def eta_block(self):
        return self._calculation_params.calculation_inputs.eta_block

    @property
    def eta_pol(self):
        return self._calculation_params.calculation_inputs.eta_pol

    @property
    def eta_r(self):
        return self._calculation_params.calculation_inputs.eta_r

    ###################################
    # Getters for derived parameters  #
    ###################################

    @property
    def tau_atm(self):
        return self._calculation_params.derived_params.tau_atm

    @property
    def T_atm(self):
        return self._calculation_params.derived_params.T_atm

    @property
    def eta_a(self):
        return self._calculation_params.derived_params.eta_a

    @property
    def eta_s(self):
        return self._calculation_params.derived_params.eta_s

    @property
    def T_sys(self):
        return self._calculation_params.derived_params.T_sys

    @property
    def sefd(self):
        return self._calculation_params.derived_params.sefd

    @property
    def area(self):
        return self._calculation_params.area

    @property
    def calculation_params(self):
        """
        Parameters used to perform the calculation
        (input params and calculated params)
        This function returns the parameters as a
        flattened dictionary for convenience
        """
        return self._calculation_params.calculator_params_as_dict()

    @property
    def calculation_inputs(self):
        """
        The inputs to the calculation
        """
        return self._calculation_params.calculation_inputs

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

        return DerivedParams(tau_atm=tau_atm, T_atm=T_atm, eta_a=eta_a,
                             eta_s=eta_s, T_sys=T_sys, sefd=sefd, area=area)
