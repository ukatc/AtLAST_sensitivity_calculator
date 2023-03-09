import astropy.units as u
import numpy as np
from atlast_sc.atmosphere_params import AtmosphereParams
from atlast_sc.sefd import SEFD
from atlast_sc.temperatures import Temperatures
from atlast_sc.efficiencies import Efficiencies
from atlast_sc.models import DerivedParams
from atlast_sc.models import UserInput
from atlast_sc.models import InstrumentSetup
from atlast_sc.config import Config
from atlast_sc.utils import params_updater
from atlast_sc.utils import FileHelper


class Calculator:
    """
    Calculator class that provides an interface to the main
    calculator functionality and performs the core calculations
    to determine the output sensitivity or integration time.

    :param user_input: Dictionary containing user-defined input parameters
    :type user_input: dict
    :param instrument_setup: Dictionary containing instrument setup parameters. **NB: usage not tested, and may not be supported in future.**
    :type instrument_setup: dict
    """
    def __init__(self, user_input={}, instrument_setup={}):
        # TODO: provide accessor methods for properties
        # TODO: get a list of properties that are editable and provide setters

        self._derived_params = None

        # Store the input parameters used to initialise the calculator
        self._config = Config(user_input, instrument_setup)

        # Calculate and derived parameters used in the calculation
        self._calculate_derived_parameters()

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
        return self._calculation_inputs.user_input.t_int.value

    @t_int.setter
    @params_updater
    def t_int(self, value):
        # TODO: Setting this value in the on the inputs feels wrong.
        #  This may be a calculated param. Allowing the user to change it
        #  without restriction may lead to inaccurate output if they perform
        #  the sensitivity calculation, change the integration time, then
        #  store or use those stored values.
        #  Need separate "outputs" properties that are used for
        #  subsequent calculations and/or storing results?
        self._calculation_inputs.user_input.t_int.value = value

    @property
    def sensitivity(self):
        return self._calculation_inputs.user_input.sensitivity.value

    @sensitivity.setter
    @params_updater
    def sensitivity(self, value):
        # TODO: Setting this value in the on the inputs feels wrong.
        #  This may be a calculated param. Allowing the user to change it
        #  without restriction may lead to inaccurate output if they perform
        #  the sensitivity calculation, change the integration time, then
        #  store or use those stored values.
        #  Need separate "outputs" properties that are used for
        #  subsequent calculations and/or storing results?
        self._calculation_inputs.user_input.sensitivity.value = value
        self._calculation_inputs.user_input.sensitivity.unit = value.unit

    @property
    def bandwidth(self):
        return self._calculation_inputs.user_input.bandwidth.value

    @bandwidth.setter
    @params_updater
    def bandwidth(self, value):
        self._calculation_inputs.user_input.bandwidth.value = value
        self._calculation_inputs.user_input.bandwidth.unit = value.unit

    @property
    def obs_frequency(self):
        return self._calculation_inputs.user_input.obs_freq.value

    @obs_frequency.setter
    @params_updater
    def obs_frequency(self, value):
        self._calculation_inputs.user_input.obs_freq.value = value
        self._calculation_inputs.user_input.obs_freq.unit = value.unit

    @property
    def n_pol(self):
        return self._calculation_inputs.user_input.n_pol.value

    @n_pol.setter
    @params_updater
    def n_pol(self, value):
        self._calculation_inputs.user_input.n_pol.value = value

    @property
    def weather(self):
        return self._calculation_inputs.user_input.weather.value

    @weather.setter
    @params_updater
    def weather(self, value):
        self._calculation_inputs.user_input.weather.value = value

    @property
    def elevation(self):
        return self._calculation_inputs.user_input.elevation.value

    @elevation.setter
    @params_updater
    def elevation(self, value):
        self._calculation_inputs.user_input.elevation.value = value
        self._calculation_inputs.user_input.elevation.unit = value.unit

    ####################################################################
    # Getters and a couple of setters for instrument setup parameters  #
    ####################################################################

    @property
    def g(self):
        return self._calculation_inputs.instrument_setup.g.value

    @property
    def surface_rms(self):
        return self._calculation_inputs.instrument_setup.surface_rms.value

    @property
    def dish_radius(self):
        return self._calculation_inputs.instrument_setup.dish_radius.value

    @dish_radius.setter
    @params_updater
    def dish_radius(self, value):
        # TODO Flag to the user somehow that they are varying an instrument
        #   setup parameter
        self._calculation_inputs.instrument_setup.dish_radius.value = value
        self._calculation_inputs.instrument_setup.dish_radius.unit = value.unit

    @property
    def T_amb(self):
        return self._calculation_inputs.instrument_setup.T_amb.value

    # @property
    # def T_rx(self):
    #     return self._calculation_inputs.instrument_setup.T_rx.value

    @property
    def eta_eff(self):
        return self._calculation_inputs.instrument_setup.eta_eff.value

    @property
    def eta_ill(self):
        return self._calculation_inputs.instrument_setup.eta_ill.value

    @property
    def eta_q(self):
        return self._calculation_inputs.instrument_setup.eta_q.value

    @property
    def eta_spill(self):
        return self._calculation_inputs.instrument_setup.eta_spill.value

    @property
    def eta_block(self):
        return self._calculation_inputs.instrument_setup.eta_block.value

    @property
    def eta_pol(self):
        return self._calculation_inputs.instrument_setup.eta_pol.value

    @property
    def eta_r(self):
        return self._calculation_inputs.instrument_setup.eta_r.value

    #########################
    # Getters for constants #
    #########################

    @property
    def T_cmb(self):
        return self._calculation_inputs.T_cmb.value

    ###################################
    # Getters for derived parameters  #
    ###################################

    @property
    def tau_atm(self):
        return self._derived_params.tau_atm

    @property
    def T_atm(self):
        return self._derived_params.T_atm

    @property
    def eta_a(self):
        return self._derived_params.eta_a

    @property
    def eta_s(self):
        return self._derived_params.eta_s

    @property
    def T_sys(self):
        return self._derived_params.T_sys

    @property
    def sefd(self):
        return self._derived_params.sefd

    @property
    def area(self):
        return self._derived_params.area

    @property
    def calculation_parameters_as_dict(self):
        """
        TODO: might remove this. Not sure it's useful, and may cause some confusion.
        Returns the parameters used in the calculation (user input, instrument
        setup, and derived parameters).

        :return: Dictionary of parameters used in the calculation
        :rtype: dict
        """
        return self._calculation_params_as_dict()

    @property
    def _calculation_inputs(self):
        """
        The inputs to the calculation (user input and instrument setup)
        """
        return self._config.calculation_inputs

    #################################################
    # Public methods for performing sensitivity and #
    # integration time calculations                 #
    #################################################

    def calculate_sensitivity(self, t_int=None):
        """
        Calculates the telescope sensitivity (Jansky) for a
        given integration time `t_int`.

        :param t_int: integration time. Optional. Defaults to the internally
            stored value
        :type t_int: astropy.units.Quantity
        :return: sensitivity in Janksy
        :rtype: astropy.units.Quantity
        """

        # Use the internally stored integration time if t_int is not
        #   supplied
        t_int = t_int if t_int is None else self.t_int

        sensitivity = \
            (self.sefd /
                (self.eta_s *
                    np.sqrt(self.n_pol *
                            self.bandwidth *
                            t_int)
                 ) * np.exp(self.tau_atm)
             )

        return sensitivity.to(u.Jy)

    def calculate_t_integration(self, sensitivity=None):
        """
        Calculates the integration time required for a given `sensitivity`
        to be reached.

        :param sensitivity: required sensitivity in Jansky. Optional. Defaults
            to the internally stored value
        :type sensitivity: astropy.units.Quantity
        :return: integration time in seconds
        :rtype: astropy.units.Quantity
        """

        # Use the internally stored sensitivity if this value is not
        #   supplied.
        sensitivity = sensitivity if sensitivity is None else self.sensitivity

        t_int = ((self.sefd
                  * np.exp(self.tau_atm))
                 / (sensitivity *
                    self.eta_s)) ** 2 \
            / (self.n_pol
                * self.bandwidth)

        return t_int.to(u.s)

    def reset_calculator(self):
        """
        Resets all calculators parameters to their initial values.
        """
        # Reset the config calculation inputs to their original values
        self._config.calculation_inputs = \
            self._config.original_calculation_inputs
        # Recalculate the derived parameters
        self._calculate_derived_parameters()

    def output_to_file(self, path, file_name="output_parameters",
                       file_type="yml"):
        """
        Writes the calculator parameters to a file. An existing file
        with the same name path, file_name and file_type will be overwritten.

        :param path: The directory where the file is written
        :type path: str
        :param file_name: The name of the file (excluding the file extension)
        :type file_name: str
        :param file_type: The file format
        :type file_type: str
        """
        output_as_dict = self._calculation_params_as_dict()

        FileHelper.write_to_file(output_as_dict, path, file_name, file_type)

    def _calculate_derived_parameters(self):
        """
        Performs the calculations required to produce the
        final set of parameters required for the sensitivity
        calculation.
        """

        # Perform atmospheric model calculation
        atm = AtmosphereParams(self.obs_frequency, self.weather,
                               self.elevation)

        T_atm = atm.T_atm()
        tau_atm = atm.tau_atm()

        # Perform efficiencies calculation
        eta = Efficiencies(self.eta_ill, self.eta_q, self.eta_spill,
                           self.eta_block, self.eta_pol, self.eta_r)

        eta_a = eta.eta_a(self.obs_frequency, self.surface_rms)
        eta_s = eta.eta_s()

        # Calculate the temperatures
        temps = Temperatures(self.obs_frequency, self.T_cmb, T_atm, self.T_amb,
                            tau_atm)
        T_sys = temps.system_temperature(self.g, self.eta_eff)

        # Calculate the dish area
        area = np.pi * self.dish_radius ** 2
        # Calculate source equivalent flux density
        sefd = SEFD.calculate(T_sys, area, eta_a)

        self._derived_params = \
            DerivedParams(tau_atm=tau_atm, T_atm=T_atm, T_rx=temps.T_rx,
                          eta_a=eta_a, eta_s=eta_s, T_sys=T_sys, sefd=sefd,
                          area=area)

    def _calculation_params_as_dict(self):
        """
        Convert the calculation inputs (user inputs and instrument setup)
        and derived parameters to a dictionary
        """

        # Convert the calculation inputs to a dictionary
        output_dict = {}
        for field in self._calculation_inputs:
            if isinstance(field[1], UserInput) \
                    or isinstance(field[1], InstrumentSetup):
                for values in field[1]:
                    output_dict[values[0]] = values[1].value
            else:
                output_dict[field[0]] = field[1].value

        # Append the derived parameters to the dictionary
        for field in self._derived_params:
            output_dict[field[0]] = field[1]

        return output_dict
