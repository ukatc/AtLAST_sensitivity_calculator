import warnings
import astropy.units as u
import numpy as np
from atlast_sc.utils import DataHelper
from atlast_sc.exceptions import CalculatedValueInvalidWarning
from atlast_sc.exceptions import ValueOutOfRangeException
from astropy.units import Quantity
from atlast_sc.models import UserInput
from atlast_sc.utils import Decorators

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
    def __init__(self, param_setup, user_input_params, inst_spec_params, tel_and_env_params, derived_params):
        
        # Default classes
        self._param_setup = param_setup
        self.user_input = user_input_params
        self.instrument_specific = inst_spec_params
        self.telescope_and_environment = tel_and_env_params

        self.calculated_sensitivity = None
        self.calculated_t_int = None

        # Make sure the user input doesn't contain any unexpected parameter
        # names
        # self._check_input_param_names(self.user_input)

    @property
    def derived_parameters(self):
        # We need to retrieve the derived parameters from user input class as with every 
        # parameter that gets used in the calculation of other parameters change, the 
        # derived parameters also change. It is only the user input parameters that prompts
        # the derived parameters to change ( TODO: dish radius also prompts derived parameters to
        # change, however, this might be consciously overlooked). Validation of the user inputs 
        # are done on the user input level, therefore, the derived parameters belong to the current
        # version of the user input parameters at that point.
        return self.user_input.derived_parameters
    
    @derived_parameters.setter
    @Decorators.validate_and_update_derived_params
    def derived_parameters(self, new_values):
        self.derived_parameters = new_values

    
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
        
    #################################################
    # Public methods for performing sensitivity and #
    # integration time calculations                 #
    #################################################

    def calculate_sensitivity(self, user_input=None, t_int=None, update_calculator=True):
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

        # TODO: If update calculator is true then update dp manually with uip derived parameters
        n_pol = None
        bandwidth = None
        if t_int is not None:
            if update_calculator:
                self.user_input.t_int = t_int
            else:
                DataHelper.validate(self.user_input, 't_int', t_int)
        else:
            t_int = self.user_input.t_int
        
        if user_input is not None:
            if 'bandwidth' in user_input:
                # Retrieve bandwidth value from user inputs and convert to Quantity object
                bandwidth = Quantity(value = float(user_input['bandwidth']['value']),
                                                unit = (user_input['bandwidth']['unit']))
            else:
                 bandwidth = self.user_input.bandwidth
            if 'n_pol' in user_input:
                n_pol = Quantity(value = int(user_input['n_pol']['value']))
            else:
                n_pol = self.user_input.n_pol
        else:
            bandwidth = self.user_input.bandwidth
            # Retrieve n_pol value from user inputs and convert to Quantity object
            n_pol = self.user_input.n_pol

        sensitivity_result = \
            self.derived_parameters.sefd / \
            (self.derived_parameters.eta_s * np.sqrt(n_pol * bandwidth * t_int))

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

    def calculate_t_integration(self, user_input=None, sensitivity=None,
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

        if user_input is not None:
            if 'bandwidth' in user_input:
                # Retrieve bandwidth value from user inputs and convert to Quantity object
                bandwidth = Quantity(value = float(user_input['bandwidth']['value']),
                                                unit = (user_input['bandwidth']['unit']))
            else:
                 bandwidth = self.user_input.bandwidth
            if 'n_pol' in user_input:
                n_pol = Quantity(value = int(user_input['n_pol']['value']))
            else:
                n_pol = self.user_input.n_pol
        else:
            bandwidth = self.user_input.bandwidth
            # Retrieve n_pol value from user inputs and convert to Quantity object
            n_pol = self.user_input.n_pol
        
        t_int_result = (self.derived_parameters.sefd / (sensitivity * self.derived_parameters.eta_s)) ** 2 \
                / (n_pol * bandwidth)

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
        self.user_input._calculate_derived_parameters()

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