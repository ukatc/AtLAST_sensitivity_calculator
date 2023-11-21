import warnings
import copy
import astropy.units as u
from astropy.constants import k_B
import numpy as np
from atlast_sc.derived_groups import AtmosphereParams
from atlast_sc.derived_groups import Temperatures
from atlast_sc.derived_groups import Efficiencies
from atlast_sc.models import DerivedParams
from atlast_sc.models import UserInput
from atlast_sc.models import InstrumentSetup
from atlast_sc.models import CalculationInput
from atlast_sc.utils import Decorators, DataHelper
from atlast_sc.exceptions import CalculatedValueInvalidWarning
from atlast_sc.exceptions import ValueOutOfRangeException


class Calculator:
    """
    Calculator class that provides an interface to the main
    calculator functionality and performs the core calculations
    to determine the output sensitivity or integration time.

    :param user_input: Dictionary containing user-defined input parameters
    :type user_input: dict
    :param instrument_setup: Dictionary containing instrument setup parameters.
     **NB: usage not tested, and may not be supported in future.**
    :type instrument_setup: dict
    """
    def __init__(self, user_input={}, instrument_setup={}, finetune=False):
        self._finetune = finetune

        self._derived_params = None

        # Make sure the user input doesn't contain any unexpected parameter
        # names
        Calculator._check_input_param_names(user_input)

        # Store the input parameters used to initialise the calculator
        self._config = Config(user_input, instrument_setup)

        # Calculate the derived parameters used in the calculation
        self._calculate_derived_parameters()

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
        """
        Get or set the integration time
        """
        return self.calculation_inputs.user_input.t_int.value

    @t_int.setter
    @Decorators.validate_value
    def t_int(self, value):
        # TODO: Setting this value in the on the inputs feels wrong.
        #  This may be a calculated param. Allowing the user to change it
        #  without restriction may lead to inaccurate output if they perform
        #  the sensitivity calculation, change the integration time, then
        #  store or use those stored values.
        #  Need separate "outputs" properties that are used for
        #  subsequent calculations and/or storing results?
        # TODO: We don't technically need to update the unit here (ditto other
        #   values with units, because the value is set to a Quantity, which
        #   contains the units. It's this value that is used throughout the
        #   the application. However, not updating it feels odd, since it would
        #   result in a discrepancy between the unit property and the unit
        #   contained in the Quantity object. Think about this...
        self.calculation_inputs.user_input.t_int.value = value
        self.calculation_inputs.user_input.t_int.unit = value.unit

    @property
    def sensitivity(self):
        """
        Get or set the sensitivity
        """
        return self.calculation_inputs.user_input.sensitivity.value

    @sensitivity.setter
    @Decorators.validate_value
    def sensitivity(self, value):
        # TODO: Setting this value in the on the inputs feels wrong.
        #  This may be a calculated param. Allowing the user to change it
        #  without restriction may lead to inaccurate output if they perform
        #  the sensitivity calculation, change the integration time, then
        #  store or use those stored values.
        #  Need separate "outputs" properties that are used for
        #  subsequent calculations and/or storing results?
        self.calculation_inputs.user_input.sensitivity.value = value
        self.calculation_inputs.user_input.sensitivity.unit = value.unit

    @property
    def bandwidth(self):
        """
        Get or set the bandwidth
        """
        return self.calculation_inputs.user_input.bandwidth.value

    @bandwidth.setter
    @Decorators.validate_and_update_params
    def bandwidth(self, value):
        self.calculation_inputs.user_input.bandwidth.value = value
        self.calculation_inputs.user_input.bandwidth.unit = value.unit

    @property
    def obs_freq(self):
        """
        Get or set the sky frequency of the observations
        """
        return self.calculation_inputs.user_input.obs_freq.value

    @obs_freq.setter
    @Decorators.validate_and_update_params
    def obs_freq(self, value):
        self.calculation_inputs.user_input.obs_freq.value = value
        self.calculation_inputs.user_input.obs_freq.unit = value.unit

    @property
    def n_pol(self):
        """
        Get or set the number of polarisations being observed
        """
        return self.calculation_inputs.user_input.n_pol.value

    @n_pol.setter
    @Decorators.validate_value
    def n_pol(self, value):
        self.calculation_inputs.user_input.n_pol.value = value

    @property
    def weather(self):
        """
        Get or set the relative humidity
        """
        return self.calculation_inputs.user_input.weather.value

    @weather.setter
    @Decorators.validate_and_update_params
    def weather(self, value):
        self.calculation_inputs.user_input.weather.value = value

    @property
    def elevation(self):
        """
        Get or set the elevation of the target for calculating air mass
        """
        return self.calculation_inputs.user_input.elevation.value

    @elevation.setter
    @Decorators.validate_and_update_params
    def elevation(self, value):
        self.calculation_inputs.user_input.elevation.value = value
        self.calculation_inputs.user_input.elevation.unit = value.unit

    ####################################################################
    # Getters and a couple of setters for instrument setup parameters  #
    ####################################################################

    @property
    def g(self):
        """
        Get the sideband ratio
        """
        return self.calculation_inputs.instrument_setup.g.value

    @property
    def surface_rms(self):
        """
        Get the surface smoothness of the instrument
        """
        return self.calculation_inputs.instrument_setup.surface_rms.value

    @property
    def dish_radius(self):
        """
        Get the radius of the primary mirror
        """
        return self.calculation_inputs.instrument_setup.dish_radius.value

    @dish_radius.setter
    @Decorators.validate_and_update_params
    def dish_radius(self, value):
        # TODO Flag to the user somehow that they are varying an instrument
        #   setup parameter?
        self.calculation_inputs.instrument_setup.dish_radius.value = value
        self.calculation_inputs.instrument_setup.dish_radius.unit = value.unit

    @property
    def T_amb(self):
        """
        Get the average ambient temperature
        """
        return self.calculation_inputs.instrument_setup.T_amb.value

    @property
    def eta_eff(self):
        """
        Get the forward efficiency
        """
        return self.calculation_inputs.instrument_setup.eta_eff.value

    @property
    def eta_ill(self):
        """
        Get the illumination efficiency
        """
        return self.calculation_inputs.instrument_setup.eta_ill.value

    @property
    def eta_spill(self):
        """
        Get the spillover efficiency
        """
        return self.calculation_inputs.instrument_setup.eta_spill.value

    @property
    def eta_block(self):
        """
        Get the lowered efficiency due to blocking
        """
        return self.calculation_inputs.instrument_setup.eta_block.value

    @property
    def eta_pol(self):
        """
        Get the polarisation efficiency
        """
        return self.calculation_inputs.instrument_setup.eta_pol.value

    #########################
    # Getters for constants #
    #########################

    @property
    def T_cmb(self):
        """
        Get the temperature of the CMB
        """
        return self.calculation_inputs.T_cmb.value

    ###################################
    # Getters for derived parameters  #
    ###################################

    @property
    def tau_atm(self):
        """
        Get the atmospheric transmittance
        """
        return self.derived_parameters.tau_atm

    @property
    def T_atm(self):
        """
        Get the atmospheric temperature
        """
        return self.derived_parameters.T_atm

    @property
    def T_rx(self):
        """
        Get the receiver temperature
        """
        return self.derived_parameters.T_rx

    @property
    def eta_a(self):
        """
        Get the dish efficiency
        """
        return self.derived_parameters.eta_a

    @property
    def eta_s(self):
        """
        Get the system efficiency
        """
        return self.derived_parameters.eta_s

    @property
    def T_sys(self):
        """
        Get the system temperature
        """
        return self.derived_parameters.T_sys

    @property
    def T_sky(self):
        """
        Get the system temperature
        """
        return self.derived_parameters.T_sky

    @property
    def sefd(self):
        """
        Get the system equivalent flux density
        """
        return self.derived_parameters.sefd

    @property
    def calculation_inputs(self):
        """
        The inputs to the calculation (user input and instrument setup)
        """
        return self._config.calculation_inputs

    @property
    def user_input(self):
        """
        User inputs to the calculation
        """
        return self._config.calculation_inputs.user_input

    @property
    def instrument_setup(self):
        """
        Instrument setup parameters
        """
        return self._config.calculation_inputs.instrument_setup

    @property
    def derived_parameters(self):
        """
        Parameters calculated from user input and instrument setup
        """
        return self._derived_params

    #################################################
    # Public methods for performing sensitivity and #
    # integration time calculations                 #
    #################################################

    def calculate_sensitivity(self, t_int=None, update_calculator=True):
        """
        Calculates the telescope sensitivity (mJy) for a
        given integration time `t_int`.

        :param t_int: integration time. Optional. Defaults to the internally
            stored value
        :type t_int: astropy.units.Quantity
        :param update_calculator: True if the calculator should be updated with
            the specified integration time and calculated sensitivity.
            Optional. Defaults to True
        :type update_calculator: bool
        :return: sensitivity in mJy
        :rtype: astropy.units.Quantity
        """

        if t_int is not None:
            if update_calculator:
                self.t_int = t_int
            else:
                DataHelper.validate(self, 't_int', t_int)
        else:
            t_int = self.t_int

        sensitivity = \
            self.sefd / \
            (self.eta_s * np.sqrt(self.n_pol * self.bandwidth * t_int))

        # Convert the output to the most convenient units
        sensitivityresult = sensitivity.to(u.mJy)
        if  sensitivityresult < 1*u.mJy:
            sensitivity = sensitivity.to(u.uJy)
        elif (sensitivityresult >= 1*u.mJy) & (sensitivityresult < 1000*u.mJy):
            sensitivity = sensitivity.to(u.mJy)
        elif sensitivityresult >= 1000*u.mJy:
            sensitivity = sensitivity.to(u.Jy)

        # Try to update the sensitivity stored in the calculator
        if update_calculator:
            try:
                self.sensitivity = sensitivity
            except ValueOutOfRangeException as e:
                # This point is actually unreachable, but it's sensible to
                # have the code in place in case the permitted range of
                # the sensitivity changes and becomes possible to achieve with
                # the right combination of input parameters.
                message = \
                    Calculator._calculated_value_error_msg(sensitivity, e)
                warnings.warn(message, CalculatedValueInvalidWarning)

        return sensitivity

    def calculate_t_integration(self, sensitivity=None,
                                update_calculator=True):
        """
        Calculates the integration time required for a given `sensitivity`
        to be reached.

        :param sensitivity: required sensitivity. Optional. Defaults
            to the internally stored value
        :type sensitivity: astropy.units.Quantity
        :param update_calculator: True if the calculator should be updated with
            the specified sensitivity and calculated integration time.
            Optional. Defaults to True
        :type update_calculator: bool
        :return: integration time in seconds
        :rtype: astropy.units.Quantity
        """

        if sensitivity is not None:
            if update_calculator:
                self.sensitivity = sensitivity
            else:
                DataHelper.validate(self, 'sensitivity', sensitivity)
        else:
            sensitivity = self.sensitivity

        t_int = (self.sefd / (sensitivity * self.eta_s)) ** 2 \
            / (self.n_pol * self.bandwidth)

        # Convert the output to the most convenient units
        timeresult = t_int.to(u.s)
        if  timeresult < 60*u.s:
            t_int = t_int.to(u.s)
        elif (timeresult >= 60*u.s) & (timeresult < 3600*u.s):
            t_int = t_int.to(u.min)
        elif timeresult >= 3600*u.s:
            t_int = t_int.to(u.h)

        # Try to update the integration time stored in the calculator
        if update_calculator:
            try:
                self.t_int = t_int
            except ValueOutOfRangeException as e:
                message = Calculator._calculated_value_error_msg(t_int, e)
                warnings.warn(message, CalculatedValueInvalidWarning)

        return t_int

    ###################
    # Utility methods #
    ###################

    def reset(self):
        """
        Resets all calculator parameters to their initial values.
        """
        # Reset the config calculation inputs to their original values
        self._config.reset()
        # Recalculate the derived parameters
        self._calculate_derived_parameters()

    #####################
    # Protected methods #
    #####################

    @staticmethod
    def _check_input_param_names(user_input):
        """
        Validates the user input parameters (just the names; value validation
        is handled by the model)

        :param user_input: Dictionary containing user-defined input parameters
        :type user_input: dict
        """

        test_model = UserInput()

        for param in user_input:
            if param not in test_model.__dict__:
                raise ValueError(f'"{param}" is not a valid input parameter')

    def _calculate_derived_parameters(self):
        """
        Performs the calculations required to produce the
        set of derived parameters required for the sensitivity
        calculation.
        """

        # TODO Technically, it's possible to instantiate each of the
        # classes below using a different observing frequency for each.
        # The resulting derived parameters wouldn't make sense under those
        # circumstances. Although this is an unlikely scenario, the design
        # would be cleaner if there three classes referenced the
        # same observing frequency.
        # Implement a Builder interface to construct all three objects using
        # the same observing frequency?

        # LDM
        # ------------------------------------------------------------------
        # T_atm, tau_atm, and the various temps values are not actually used
        # for computing the sefd, but I kept this part to avoid breaking the
        # build of DerivedParams below
        # ------------------------------------------------------------------

        # Perform efficiencies calculations
        eta = Efficiencies(self.obs_freq, self.surface_rms, self.eta_ill,
                           self.eta_spill, self.eta_block, self.eta_pol)

        # Perform atmospheric model calculations
        atm = AtmosphereParams()
        tau_atm = atm.calculate_tau_atm(self.obs_freq,
                                        self.weather, self.elevation)
        T_atm = atm.calculate_atmospheric_temperature(self.obs_freq,
                                                      self.weather)

        # Calculate the temperatures
        temps = Temperatures(self.obs_freq, self.T_cmb, self.T_amb, self.g,
                             self.eta_eff, T_atm, tau_atm)

        # LDM
        # ------------------------------------------------------------------
        # This is where the snippet starts. The idea is to compute an
        # effect SEFD as sefd_eff = sqrt(dnu/sum(dnu_i/sefd_i)), where dnu
        # is the total bandwidth and dnu_i the widths of the narrow channels
        # for which we compute each sefd_i. This comes from basic noise 
        # statistics consideration for computing the total RMS for a broad
        # band composed of n independent channels. 
        # Setting finetune=False will fall back on the old implementation
        # ------------------------------------------------------------------

        # define lower and upper limit of the requested band
        obs_freq_low = (self.obs_freq-0.50*self.bandwidth).to('GHz').value
        obs_freq_upp = (self.obs_freq+0.50*self.bandwidth).to('GHz').value

        # select all the frequencies in the atm tables comprised within the band edges
        obs_freq_list = atm.tau_atm_table[:, 0][np.logical_and(atm.tau_atm_table[:, 0]>obs_freq_low,
                                                               atm.tau_atm_table[:, 0]<obs_freq_upp)]
       
        # pad the frequency array to include the lower/upper band edges 
        obs_freq_list = np.concatenate(([obs_freq_low],obs_freq_list,[obs_freq_upp]))*u.GHz

        # double the frequency resolution; turned off for the moment, but
        # just wanted to keep track of this
        # if False:
        #     obs_freq_list = np.ravel([obs_freq_list[1:],0.50*(obs_freq_list[1:]+obs_freq_list[:-1])],'F')
        #     obs_freq_list = np.append(obs_freq_low,obs_freq_list)

        # check if there are enough channels for performing the sum,
        # otherwise estimate the single-frequency SEFD
        if self._finetune and len(obs_freq_list)>1:
            
            _sefd = []
            
            obs_band_list = (obs_freq_list[1:]-obs_freq_list[:-1])
            obs_freq_list = (obs_freq_list[1:]+obs_freq_list[:-1])*0.50

            # compute SEFD for each narrow spectral element
            for freq in obs_freq_list:
                _tau_atm = atm.calculate_tau_atm(freq,self.weather,self.elevation)

                _T_atm = atm.calculate_atmospheric_temperature(freq,self.weather)
                _temps = Temperatures(freq, self.T_cmb, self.T_amb, self.g,
                                      self.eta_eff, _T_atm, _tau_atm)

                _sefd.append(self._calculate_sefd(_temps.T_sys,eta.eta_a).to('J/m2').value)
            _sefd = np.asarray(_sefd)*(u.J/u.m**2)

            # obtain the effective SEFD for the input band
            sefd = np.sqrt(self.bandwidth/np.sum(obs_band_list/_sefd**2))
        else:
            sefd = self._calculate_sefd(temps.T_sys, eta.eta_a)

        self._derived_params = \
            DerivedParams(tau_atm=tau_atm, T_atm=T_atm, T_rx=temps.T_rx,
                          eta_a=eta.eta_a, eta_s=eta.eta_s, T_sys=temps.T_sys, T_sky=temps.T_sky,
                          sefd=sefd)

    def _calculate_sefd(self, T_sys, eta_a):
        """
        Calculates the source equivalent flux density, SEFD, from the system
        temperature, T_sys, the dish efficiency eta_A, and the dish area.

        :param T_sys: system temperature
        :type T_sys: astropy.units.Quantity
        :param eta_a: the dish efficiency factor
        :type eta_a: float
        :return: source equivalent flux density
        :rtype: astropy.units.Quantity
        """

        dish_area = np.pi * self.dish_radius ** 2
        sefd = (2 * k_B * T_sys) / (eta_a * dish_area)

        return sefd

    @staticmethod
    def _calculated_value_error_msg(calculated_value, validation_error):
        """
        The message displayed when a calculated value (t_int or sensitivity) is
        outside the permitted range.

        :param calculated_value: the calculated value of the target parameter
        :type calculated_value: astropy.units.Quantity
        :param validation_error: the error raised when validating the
            calculated parameter value
        :type validation_error: atlast_sc.exceptions.ValueOutOfRangeException
        """

        message = f"The calculated value {calculated_value.round(4)} " \
                  f"is outside of the permitted range " \
                  f"for parameter '{validation_error.parameter}'. " \
                  f"{validation_error.message} " \
                  f"The Calculator will not be updated with the new value. " \
                  f"Please adjust the input parameters and recalculate."

        return message


class Config:
    """
    Class that holds the user input and instrument setup parameters
    used to perform the sensitivity calculations.
    """
    def __init__(self, user_input={}, instrument_setup={}):
        """
        Initialises all the required parameters from user_input and
        instrument_setup.

        :param user_input: A dictionary of user inputs of structure
        {'param_name':{'value': <value>, 'unit': <unit>}}
        :type user_input: dict
        :param instrument_setup: A dictionary of instrument setup parameters
        of structure
        {'param_name':{'value': <value>, 'unit': <unit>}}
        :type instrument_setup: dict
        """

        new_user_input = UserInput(**user_input)
        new_instrument_setup = InstrumentSetup(**instrument_setup)
        self._calculation_inputs = \
            CalculationInput(user_input=new_user_input,
                             instrument_setup=new_instrument_setup)

        # Make a deep copy of the calculation inputs to enable the
        # calculator to be reset to its initial setup
        self._original_inputs = copy.deepcopy(self._calculation_inputs)

    @property
    def calculation_inputs(self):
        """
        Get the calculation inputs (user input and instrument setup)
        """
        return self._calculation_inputs

    def reset(self):
        """
        Resets the calculator configuration parameters (user input and
        instrument setup to their original values.
        """
        self._calculation_inputs = \
            self._original_inputs
