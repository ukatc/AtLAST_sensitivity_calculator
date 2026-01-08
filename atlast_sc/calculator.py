import warnings
import yaml
import astropy.units as u
import numpy as np
from atlast_sc.utils import DataHelper, Decorators
from atlast_sc.exceptions import CalculatedValueInvalidWarning
from atlast_sc.exceptions import ValueOutOfRangeException

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
    def __init__(self, param_setup):
        
        # Parameter setup class that contains models with default values
        self._param_setup = param_setup
        # Special classes for customisation of models
        self._user_input = UserInputParameters(param_setup)
        self._telescope_and_environment = TelescopeAndEnvironmentParameters(param_setup)
        self._derived_parameters = DerivedParameters(param_setup)
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
    def loaded_instruments(self):
        """
        List of names of the loaded instruments with their respective
        specified observing frequency and bandwidth ranges
        """
        loaded_instrument_list = []
        loaded_instrument_modules = self._param_setup.loaded_instruments
        for inst_name, inst_module in loaded_instrument_modules.items():
            inst_obs_freq_list = inst_module.obs_freq_ranges_and_unit
            inst_bandwidth_list = inst_module.bandwidth_ranges_and_unit
            loaded_instrument_list.append({inst_name: {
                                           'obs_freq': inst_obs_freq_list,
                                           'bandwidth': inst_bandwidth_list}
                                           })
        return yaml.dump(loaded_instrument_list, default_flow_style=False)

    @property
    def chosen_instrument(self):
        """
        Name of chosen instrument
        """
        return self._param_setup.chosen_instrument.name
    
    @chosen_instrument.setter
    def chosen_instrument(self, instrument_name):
        try:
            self._param_setup.chosen_instrument = \
                self._param_setup.loaded_instruments[instrument_name]
        except KeyError as e:
            print('Instrument provided is not available. Check '\
                  'the list of loaded instrument names again.')
        
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