from atlast_sc.utils import Decorators

###################################
# Getters for derived parameters  #
###################################

class DerivedParameters:
    def __init__(self, derived_params, config):
        self._derived_parameters = derived_params
        
        self.config = config

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
        return self.config.calculation_inputs

    @property
    def user_input(self):
        """
        User inputs to the calculation
        """
        return self.config.calculation_inputs.user_input

    @property
    def instrument_setup(self):
        """
        Instrument setup parameters
        """
        return self.config.calculation_inputs.instrument_setup

    @property
    def derived_parameters(self):
        """
        Parameters calculated from user input and instrument setup
        """
        return self._derived_parameters

    @derived_parameters.setter
    @Decorators.validate_and_update_params
    def derived_parameters(self, value):
        self._derived_parameters = value
