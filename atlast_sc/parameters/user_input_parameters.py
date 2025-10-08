from atlast_sc.utils import Decorators

###################################################
# Getters and setters for user input parameters   #
###################################################

class UserInputParameters:

    def __init__(self, param_setup):
        self._param_setup = param_setup

    @property
    def t_int(self):
        """
        Get the integration time that user has specified
        """
        return self._param_setup.calculation_inputs.user_input.t_int.value

    @t_int.setter
    @Decorators.validate_value
    def t_int(self, value):
        """
        Set the integration time that user has specified
        """
        # TODO: We don't technically need to update the unit here (ditto other
        #   values with units, because the value is set to a Quantity, which
        #   contains the units. It's this value that is used throughout the
        #   the application. However, not updating it feels odd, since it would
        #   result in a discrepancy between the unit property and the unit
        #   contained in the Quantity object. Think about this...
        self._param_setup.calculation_inputs.user_input.t_int.value = value
        self._param_setup.calculation_inputs.user_input.t_int.unit = value.unit

    @property
    def sensitivity(self):
        """
        Get the sensitivity that user has specified
        """
        return self._param_setup.calculation_inputs.user_input.sensitivity.value

    @sensitivity.setter
    @Decorators.validate_value
    def sensitivity(self, value):
        """
        Set the sensitivity that user has specified
        """
        self._param_setup.calculation_inputs.user_input.sensitivity.value = value
        self._param_setup.calculation_inputs.user_input.sensitivity.unit = value.unit

    @property
    def bandwidth(self):
        """
        Get the bandwidth
        """
        return self._param_setup.calculation_inputs.user_input.bandwidth.value
    
    # With the new calculation of SEFD over the whole frequency range, SEFD is now dependent
    # on bandwidth and so parameters must be updated every time bandwidth is changed.
    @bandwidth.setter
    @Decorators.validate_and_update_params
    def bandwidth(self, value):
        """
        Set the bandwidth
        """
        self._param_setup.calculation_inputs.user_input.bandwidth.value = value
        self._param_setup.calculation_inputs.user_input.bandwidth.unit = value.unit

    @property
    def obs_freq(self):
        """
        Get the sky frequency of the observations
        """
        return self._param_setup.calculation_inputs.user_input.obs_freq.value

    @obs_freq.setter
    @Decorators.validate_and_update_params
    def obs_freq(self, value):
        """
        Set the sky frequency of the observations
        """
        self._param_setup.calculation_inputs.user_input.obs_freq.value = value
        self._param_setup.calculation_inputs.user_input.obs_freq.unit = value.unit

    @property
    def n_pol(self):
        """
        Get the number of polarisations being observed
        """
        return self._param_setup.calculation_inputs.user_input.n_pol.value

    @n_pol.setter
    @Decorators.validate_value
    def n_pol(self, value):
        """
        Set the number of polarisations being observed
        """
        self._param_setup.calculation_inputs.user_input.n_pol.value = value

    @property
    def weather(self):
        """
        Get the relative humidity
        """
        return self._param_setup.calculation_inputs.user_input.weather.value

    @weather.setter
    @Decorators.validate_and_update_params
    def weather(self, value):
        """
        Set the relative humidity
        """
        self._param_setup.calculation_inputs.user_input.weather.value = value

    @property
    def elevation(self):
        """
        Get the elevation of the target for calculating air mass
        """
        return self._param_setup.calculation_inputs.user_input.elevation.value

    @elevation.setter
    @Decorators.validate_and_update_params
    def elevation(self, value):
        """
        Set the elevation of the target for calculating air mass
        """
        self._param_setup.calculation_inputs.user_input.elevation.value = value
        self._param_setup.calculation_inputs.user_input.elevation.unit = value.unit
    
    def show(self):
        for name in dir(self.__class__):
            if name == "derived_parameters": # Don't show derived_parameters
                continue
            attr = getattr(self.__class__, name)
            if isinstance(attr, property):
                value = getattr(self, name)
                print(f"{name}: {value}")