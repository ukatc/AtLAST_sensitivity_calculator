import warnings
import astropy.units as u
from astropy.constants import k_B
import numpy as np
from atlast_sc.derived_groups import AtmosphereParams
from atlast_sc.derived_groups import Temperatures
from atlast_sc.derived_groups import Efficiencies
from atlast_sc.models import DerivedParams
from atlast_sc.parameters.derived_parameters import DerivedParameters
from atlast_sc.utils import DataHelper
from atlast_sc.exceptions import CalculatedValueInvalidWarning
from atlast_sc.exceptions import ValueOutOfRangeException
from astropy.units import Quantity


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
    def __init__(self, config, user_input_params, inst_setup_params, finetune=False):
        
        self.config = config
        self.finetune = finetune
        self._uip = user_input_params
        self._isp = inst_setup_params
        # self.derived_params =  self._uip._calculate_derived_parameters(user_input_params, inst_setup_params, self.finetune)
        self.derived_params =  self._uip._calculate_derived_parameters()
        self._dp = DerivedParameters(self.derived_params, config)
        self.sensitivity = user_input_params.sensitivity
        self.t_int = None
        
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
                self._uip.t_int = t_int
            else:
                DataHelper.validate(self._uip, 't_int', t_int)
        else:
            t_int = self.config.calculation_inputs.user_input.t_int.value
        
        if user_input is not None:
            if 'bandwidth' in user_input:
                # Retrieve bandwidth value from user inputs and convert to Quantity object
                bandwidth = Quantity(value = float(user_input['bandwidth']['value']),
                                                unit = (user_input['bandwidth']['unit']))
            else:
                 bandwidth = self.config.calculation_inputs.user_input.bandwidth.value
            if 'n_pol' in user_input:
                n_pol = Quantity(value = int(user_input['n_pol']['value']))
            else:
                n_pol = self.config.calculation_inputs.user_input.n_pol.value
        else:
            bandwidth = self.config.calculation_inputs.user_input.bandwidth.value
            # Retrieve n_pol value from user inputs and convert to Quantity object
            n_pol = self.config.calculation_inputs.user_input.n_pol.value

        sensitivity = \
            self._uip.derived_parameters.sefd / \
            (self._uip.derived_parameters.eta_s * np.sqrt(n_pol * bandwidth * t_int))

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
                self._uip.sensitivity = sensitivity
            else:
                DataHelper.validate(self, 'sensitivity', sensitivity)
        else:
            sensitivity = self.config.calculation_inputs.user_input.sensitivity.value

        if user_input is not None:
            if 'bandwidth' in user_input:
                # Retrieve bandwidth value from user inputs and convert to Quantity object
                bandwidth = Quantity(value = float(user_input['bandwidth']['value']),
                                                unit = (user_input['bandwidth']['unit']))
            else:
                 bandwidth = self.config.calculation_inputs.user_input.bandwidth.value
            if 'n_pol' in user_input:
                n_pol = Quantity(value = int(user_input['n_pol']['value']))
            else:
                n_pol = self.config.calculation_inputs.user_input.n_pol.value
        else:
            bandwidth = self.config.calculation_inputs.user_input.bandwidth.value
            # Retrieve n_pol value from user inputs and convert to Quantity object
            n_pol = self.config.calculation_inputs.user_input.n_pol.value
        
        t_int = (self._uip.derived_parameters.sefd / (sensitivity * self._uip.derived_parameters.eta_s)) ** 2 \
                / (n_pol * bandwidth)

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
        self.config.reset()
        # Recalculate the derived parameters
        self._uip._calculate_derived_parameters()

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

