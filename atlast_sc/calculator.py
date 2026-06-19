import warnings, yaml, re
import astropy.units as u
import numpy as np
from atlast_sc.utils import DataHelper, Decorators
from atlast_sc.exceptions import CalculatedValueInvalidWarning
from atlast_sc.exceptions import ValueOutOfRangeException
from atlast_sc.exceptions import InstrumentNotApplicableException

from atlast_sc.parameter_setup import ParameterSetup
from atlast_sc.parameters.user_input_parameters import UserInputParameters
from atlast_sc.parameters.telescope_and_environment_parameters import TelescopeAndEnvironmentParameters
from atlast_sc.parameters.derived_parameters import DerivedParameters

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
    def __init__(self, user_input={}, telescope_and_environment={}, finetune=False):

        kwargs = {}
        if user_input:
            kwargs["user_input"] = user_input
        if telescope_and_environment:
            kwargs["telescope_and_environment"] = telescope_and_environment
        if finetune:
            kwargs["finetune"] = finetune
        
        # Parameter setup class that contains models with default values if not specified
        self._param_setup = ParameterSetup(**kwargs)
        # Special classes for customisation of models
        self._user_input = UserInputParameters(self._param_setup)
        self._telescope_and_environment = TelescopeAndEnvironmentParameters(self._param_setup)
        self._derived_parameters = DerivedParameters(self._param_setup)
        # Calculated value variables of calculation result model
        self._calculated_sensitivity = self._param_setup.calculation_results.calculated_sensitivity
        self._calculated_t_int = self._param_setup.calculation_results.calculated_t_int

    @property
    def user_input(self):
        """
        User inputs to the calculation
        """
        return self._user_input
    
    @property
    def telescope_and_environment(self):
        """
        Telescope and environment parameters
        """
        return self._telescope_and_environment
    
    @property
    def derived_parameters(self):
        """
        Derived parameters
        """
        return self._derived_parameters
    
    @property
    def calculated_sensitivity(self):
        """
        Calculated sensitivity value
        """
        return self._calculated_sensitivity.value

    @calculated_sensitivity.setter
    @Decorators.validate_value
    def calculated_sensitivity(self, value):
        self._calculated_sensitivity.value = value

    @property
    def calculated_t_int(self):
        """
        Calculated integration time value
        """
        return self._calculated_t_int.value

    @calculated_t_int.setter
    @Decorators.validate_value
    def calculated_t_int(self, value):
        self._calculated_t_int.value = value

    @property
    def chosen_instrument(self):
        """
        Name of chosen instrument
        """
        return self._param_setup.chosen_instrument.name
    
    @chosen_instrument.setter
    def chosen_instrument(self, instrument_name):
        old_inst_name = self._param_setup.chosen_instrument.name
        instrument_name = instrument_name.capitalize()
        try:
            requested_inst_name = \
                self._param_setup.loaded_instruments[instrument_name].name
            
            # Check if the requested instrument can be selected given the 
            # existing user input parameters
            requested_inst_is_applicable = \
                self.requested_inst_is_applicable(requested_inst_name)

            try:
                # User inputted obs_freq and bandwidth are in range
                if requested_inst_is_applicable:
                    self._param_setup.chosen_instrument = (
                        self._param_setup.loaded_instruments[requested_inst_name]
                    )
                    # Recalculate derived parameters because new
                    # instrument has been chosen
                    self._param_setup._calculate_derived_parameters()
                    new_inst_name = self._param_setup.chosen_instrument.name
                    if old_inst_name != new_inst_name:
                        print("Instrument has been changed from " + old_inst_name + " to " + \
                          new_inst_name + ".")
                else:
                    # User inputted obs_freq and bandwidth are not 
                    # in range of the requested instrument
                    raise InstrumentNotApplicableException(
                        requested_inst_name,
                        self.chosen_instrument
                    )
            except InstrumentNotApplicableException as e:
                raise
        except KeyError as e:
            print('Instrument name provided is not available. '\
                  'Proceeding with an applicable instrument from '\
                  'the list of instruments.')
        

    @property
    def loaded_instruments(self):
        """
        Dictionary of each loaded instrument with its respective
        specified observing frequency and bandwidth ranges
        """
        loaded_instrument_dict = {}
        loaded_instrument_modules = self._param_setup.loaded_instruments
        for inst_name, inst_module in loaded_instrument_modules.items():
            inst_obs_freq_list = inst_module.obs_freq_ranges_and_unit
            inst_bandwidth_list = inst_module.bandwidth_ranges_and_unit
            loaded_instrument_dict[inst_name] = {
                'obs_freq': inst_obs_freq_list,
                'bandwidth': inst_bandwidth_list}

        return loaded_instrument_dict
        
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
                self.user_input.t_int = t_int
            else:
                DataHelper.validate(self.user_input, 't_int', t_int)
        else:
            t_int = self.user_input.t_int

        sensitivity_result = \
            self.derived_parameters.sefd / \
            (self.derived_parameters.eta_s * np.sqrt(self.user_input.n_pol * self.user_input.bandwidth * t_int))

        # Convert the output to the most convenient units
        sensitivity_result = sensitivity_result.to(u.mJy)
        if  sensitivity_result < 1*u.mJy:
            sensitivity_result = sensitivity_result.to(u.uJy)
        elif (sensitivity_result >= 1*u.mJy) & (sensitivity_result < 1000*u.mJy):
            sensitivity_result = sensitivity_result.to(u.mJy)
        elif sensitivity_result >= 1000*u.mJy:
            sensitivity_result = sensitivity_result.to(u.Jy)

        # Try to update the sensitivity stored in the calculator
        if update_calculator:
            try:
                self.calculated_sensitivity = sensitivity_result
            except ValueOutOfRangeException as e:
                # This point is actually unreachable, but it's sensible to
                # have the code in place in case the permitted range of
                # the sensitivity changes and becomes possible to achieve with
                # the right combination of input parameters.
                message = \
                    Calculator._calculated_value_error_msg(sensitivity_result, e)
                warnings.warn(message, CalculatedValueInvalidWarning)

        return sensitivity_result

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
                self.user_input.sensitivity = sensitivity
            else:
                DataHelper.validate(self, 'calculated_sensitivity', sensitivity)
        else:
            sensitivity = self.user_input.sensitivity
        
        t_int_result = (self.derived_parameters.sefd / (sensitivity * self.derived_parameters.eta_s)) ** 2 \
                / (self.user_input.n_pol * self.user_input.bandwidth)

        # Convert the output to the most convenient units
        t_int_result = t_int_result.to(u.s)
        if  t_int_result < 60*u.s:
            t_int_result = t_int_result.to(u.s)
        elif (t_int_result >= 60*u.s) & (t_int_result < 3600*u.s):
            t_int_result = t_int_result.to(u.min)
        elif t_int_result >= 3600*u.s:
            t_int_result = t_int_result.to(u.h)
        # Try to update the integration time stored in the calculator
        if update_calculator:
            try:
                self.calculated_t_int = t_int_result
            except ValueOutOfRangeException as e:
                message = Calculator._calculated_value_error_msg(t_int_result, e)
                warnings.warn(message, CalculatedValueInvalidWarning)
        return t_int_result

    ###################
    # Utility methods #
    ###################

    def reset(self):
        """
        Resets all calculator parameters to their initial values.
        """
        # Reset the _param_setup calculation inputs to their original values
        self._param_setup.reset()
        # Recalculate the derived parameters
        self._param_setup._calculate_derived_parameters()

    def requested_inst_is_applicable(self, requested_inst_name):
        """
        Check if the requested instrument can be selected to be used in the
        calculations. The already existing user input parameters will be 
        cross checked with the applicable ranges of the requested instrument.

        :param requested_inst_name: name of the requested instrument
        :type requested_inst_name: String
        :return: applicability of requested instrument
        :rtype: boolean
        """
        inst_applicable = False
        obs_freq_applicable = False
        bandwidth_applicable = False

        # See if the requested instrument fits the existent user input values
        user_obs_freq = self.user_input.obs_freq
        # Check if obs_freq units are the same 
        user_obs_freq_unit = str(self.user_input.obs_freq.unit)
        requested_inst_obs_freq_unit = self.loaded_instruments[requested_inst_name]['obs_freq']['unit']
        # If the units are not the same, convert user input obs_freq to the unit
        # of the requested instrument obs_freq ranges
        if user_obs_freq_unit != requested_inst_obs_freq_unit:
            user_obs_freq = user_obs_freq.to(u.Unit(requested_inst_obs_freq_unit))
        user_obs_freq = user_obs_freq.value
            
        # Convert bandwidth value to Hz
        user_bandwidth = self.user_input.bandwidth
        user_bandwidth = user_bandwidth.to(u.Hz)
        user_bandwidth = user_bandwidth.value

        # Requested instrument ranges
        instrument_obs_freqs = \
            self.loaded_instruments[requested_inst_name]['obs_freq']['ranges']
        instrument_bandw_vals = \
            self.loaded_instruments[requested_inst_name]['bandwidth']['ranges']
        
        # Check if user inputted observing frequency value falls in 
        # the range of the requested instrument ranges
        for range in instrument_obs_freqs:
            range = re.findall(r"[\d.]+", range)
            min_freq = float(range[0])
            max_freq = float(range[1])
            if user_obs_freq >= min_freq and user_obs_freq <= max_freq:
                obs_freq_applicable = True

        # Check if user inputted bandwidth value falls in the range of 
        # the requested instrument ranges
        if requested_inst_name != 'Default':
            for range in instrument_bandw_vals:
                range = re.findall(r"[\d.]+", range)
                min_bandw = float(range[0])
                max_bandw = float(range[1])
                if user_bandwidth >= min_bandw and user_bandwidth <= max_bandw:
                    bandwidth_applicable = True
        else: # If the requested instrument is Default
            bandwidth_applicable = True

        # If both user inputted parameters fall in the requested
        # instrument range
        if obs_freq_applicable and bandwidth_applicable:
            inst_applicable = True
        return inst_applicable

    def list_instruments(self):
        """
        Show loaded instruments and their observing frequency and bandwidth ranges
        in a pretty format.
        """
        output = "\n" + "="*70 + "\n"
        output += "AVAILABLE INSTRUMENTS\n"
        output += "="*70 + "\n\n"
        
        for inst_name, inst_info in self.loaded_instruments.items():
            output += f"* {inst_name}\n"
            obs_freq_ranges = inst_info['obs_freq']['ranges']
            obs_freq_unit = inst_info['obs_freq']['unit']
            output += f"   Observing Frequency: {obs_freq_ranges} {obs_freq_unit}\n"
            
            bandwidth_ranges = inst_info['bandwidth']['ranges']
            bandwidth_unit = inst_info['bandwidth']['unit']
            
            if inst_name == 'Default':
                bandwidth_ranges = "[Any positive value]"
            else:
                # Convert bandwidth ranges to easily readible units if needed
                bandwidth_ranges, bandwidth_unit = \
                    self._format_bandwidth_ranges(bandwidth_ranges, bandwidth_unit)
            
            output += f"   Bandwidth: {bandwidth_ranges} {bandwidth_unit}\n\n"
        
        output += "-"*70 + "\n"
        output += "To select an instrument:\n"
        output += '   calculator.chosen_instrument = "Finer"\n'
        output += "-"*70 + "\n"
        
        print(output)

    def _format_bandwidth_ranges(self, bandwidth_ranges, bandwidth_unit):
        """
        Format bandwidth ranges, converting to MHz or kHz if the values are too
        large to be easily read in Hz.

        :param bandwidth_ranges: list or string of bandwidth range(s)
        :type bandwidth_ranges: list or str
        :param bandwidth_unit: the unit of the bandwidth ranges
        :type bandwidth_unit: str
        :return: formatted ranges and appropriate unit
        :rtype: tuple(str, str)
        """
        if bandwidth_unit.lower() != 'hz':
            # If not in Hz, return as-is
            return bandwidth_ranges, bandwidth_unit
        
        # Determine the appropriate unit based on max values
        max_val = 0
        if isinstance(bandwidth_ranges, list):
            for range_str in bandwidth_ranges:
                matches = re.findall(r"[\d.]+", range_str)
                if len(matches) >= 2:
                    val = float(matches[1])
                    max_val = max(max_val, val)
        else:
            matches = re.findall(r"[\d.]+", str(bandwidth_ranges))
            if len(matches) >= 2:
                max_val = float(matches[1])
        
        # Determine display unit
        if max_val >= 1e6:
            display_unit = "MHz"
            divisor = 1e6
        elif max_val >= 1e3:
            display_unit = "kHz"
            divisor = 1e3
        else:
            display_unit = "Hz"
            divisor = 1
        
        # Convert ranges if needed
        if divisor != 1:
            formatted_ranges = []
            if isinstance(bandwidth_ranges, list):
                for range_str in bandwidth_ranges:
                    matches = re.findall(r"[\d.]+", range_str)
                    if len(matches) >= 2:
                        min_val = float(matches[0]) / divisor
                        max_val = float(matches[1]) / divisor
                        formatted_ranges.append(f"({min_val}-{max_val})")
                    else:
                        formatted_ranges.append(range_str)
                return formatted_ranges, display_unit
            else:
                matches = re.findall(r"[\d.]+", str(bandwidth_ranges))
                if len(matches) >= 2:
                    min_val = float(matches[0]) / divisor
                    max_val = float(matches[1]) / divisor
                    return f"({min_val}-{max_val})", display_unit
        
        return bandwidth_ranges, bandwidth_unit

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
    
    
    ###################################################
    # Methods to throw an error for old functionality #
    ###################################################

    def __getattr__(self, name):
        """
        Handle deprecated way of accessing parameters.
        """
        deprecated_params = {
            # user input parameters
            'obs_freq': 'user_input.obs_freq',
            'bandwidth': 'user_input.bandwidth',
            'sensitivity': 'user_input.sensitivity',
            't_int': 'user_input.t_int',
            'n_pol': 'user_input.n_pol',
            'weather': 'user_input.weather',
            'elevation': 'user_input.elevation',
            # telescope and environment parameters
            'surface_rms': 'telescope_and_environment.surface_rms',
            'dish_radius': 'telescope_and_environment.dish_radius',
            'eta_eff': 'telescope_and_environment.eta_eff',
            'eta_ill': 'telescope_and_environment.eta_ill',
            'eta_spill': 'telescope_and_environment.eta_spill',
            'eta_block': 'telescope_and_environment.eta_block',
            'eta_pol': 'telescope_and_environment.eta_pol',
            'T_cmb': 'telescope_and_environment.T_cmb',
            'T_amb': 'telescope_and_environment.T_amb',
            'T_amb': 'telescope_and_environment.T_amb'
        }
        
        if name in deprecated_params:
            raise RuntimeError(
                f"calculator.{name} is not a valid input. "
                f"Use calculator.{deprecated_params[name]} instead."
            )
        
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        """
        Handle deprecated way of setting parameters.
        """
        deprecated_params = {
            # user input parameters
            'obs_freq': 'user_input.obs_freq',
            'bandwidth': 'user_input.bandwidth',
            'sensitivity': 'user_input.sensitivity',
            't_int': 'user_input.t_int',
            'n_pol': 'user_input.n_pol',
            'weather': 'user_input.weather',
            'elevation': 'user_input.elevation',
            # telescope and environment parameters
            'surface_rms': 'telescope_and_environment.surface_rms',
            'dish_radius': 'telescope_and_environment.dish_radius',
            'eta_eff': 'telescope_and_environment.eta_eff',
            'eta_ill': 'telescope_and_environment.eta_ill',
            'eta_spill': 'telescope_and_environment.eta_spill',
            'eta_block': 'telescope_and_environment.eta_block',
            'eta_pol': 'telescope_and_environment.eta_pol',
            'T_cmb': 'telescope_and_environment.T_cmb',
            'T_amb': 'telescope_and_environment.T_amb',
            'T_amb': 'telescope_and_environment.T_amb'
        }
        
        if name in deprecated_params:
            raise RuntimeError(
                f"calculator.{name} is not a valid input. "
                f"Use calculator.{deprecated_params[name]} instead."
            )
        
        super().__setattr__(name, value)