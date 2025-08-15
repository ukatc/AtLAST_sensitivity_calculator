from atlast_sc.utils import Decorators
from atlast_sc.config import Config

###################################################
# Getters and setters for user input parameters   #
###################################################

class UserInputParameters:

    def __init__(self, config):
        self.config = config

    # TODO t_int and sensitivity are a special can se. They can be both
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
        return self.config.calculation_inputs.user_input.t_int.value

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
        self.config.calculation_inputs.user_input.t_int.value = value
        self.config.calculation_inputs.user_input.t_int.unit = value.unit

    @property
    def sensitivity(self):
        """
        Get or set the sensitivity
        """
        return self.config.calculation_inputs.user_input.sensitivity.value

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
        self.config.calculation_inputs.user_input.sensitivity.value = value
        self.config.calculation_inputs.user_input.sensitivity.unit = value.unit

    @property
    def bandwidth(self):
        """
        Get or set the bandwidth
        """
        return self.config.calculation_inputs.user_input.bandwidth.value
    # With the new calculation of SEFD over the whole frequency range, SEFD is now dependent on bandwidth and so parameters must be updated every time bandwidth is changed.
    @bandwidth.setter
    @Decorators.validate_and_update_params
    def bandwidth(self, value):
        self.config.calculation_inputs.user_input.bandwidth.value = value
        self.config.calculation_inputs.user_input.bandwidth.unit = value.unit

    @property
    def obs_freq(self):
        """
        Get or set the sky frequency of the observations
        """
        return self.config.calculation_inputs.user_input.obs_freq.value

    @obs_freq.setter
    @Decorators.validate_and_update_params
    def obs_freq(self, value):
        self.config.calculation_inputs.user_input.obs_freq.value = value
        self.config.calculation_inputs.user_input.obs_freq.unit = value.unit

    @property
    def n_pol(self):
        """
        Get or set the number of polarisations being observed
        """
        return self.config.calculation_inputs.user_input.n_pol.value

    @n_pol.setter
    @Decorators.validate_value
    def n_pol(self, value):
        self.config.calculation_inputs.user_input.n_pol.value = value

    @property
    def weather(self):
        """
        Get or set the relative humidity
        """
        return self.config.calculation_inputs.user_input.weather.value

    @weather.setter
    @Decorators.validate_and_update_params
    def weather(self, value):
        self.config.calculation_inputs.user_input.weather.value = value

    @property
    def elevation(self):
        """
        Get or set the elevation of the target for calculating air mass
        """
        return self.config.calculation_inputs.user_input.elevation.value

    @elevation.setter
    @Decorators.validate_and_update_params
    def elevation(self, value):
        self.config.calculation_inputs.user_input.elevation.value = value
        self.config.calculation_inputs.user_input.elevation.unit = value.unit