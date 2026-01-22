from atlast_sc.utils import Decorators

############################################################
# Getters and a couple of setters for telescope parameters #
############################################################

class TelescopeAndEnvironmentParameters:

    def __init__(self, param_setup):
        self._param_setup = param_setup
    
    @property
    def surface_rms(self):
        """
        Get the surface smoothness of the instrument
        """
        return self._param_setup.calculation_inputs.telescope_and_environment.surface_rms.value
    
    @property
    def dish_radius(self):
        """
        Get the radius of the primary mirror
        """
        return self._param_setup.calculation_inputs.telescope_and_environment.dish_radius.value
    
    @dish_radius.setter
    @Decorators.validate_and_update_params
    def dish_radius(self, value):
        """
        Set the radius of the primary mirror
        """
        self._param_setup.calculation_inputs.telescope_and_environment.dish_radius.value = value
        self._param_setup.calculation_inputs.telescope_and_environment.dish_radius.unit = value.unit
    
    @property
    def eta_eff(self):
        """
        Get the forward efficiency
        """
        return self._param_setup.calculation_inputs.telescope_and_environment.eta_eff.value
    
    @property
    def eta_ill(self):
        """
        Get the illumination efficiency
        """
        return self._param_setup.calculation_inputs.telescope_and_environment.eta_ill.value
    
    @property
    def eta_spill(self):
        """
        Get the spillover efficiency
        """
        return self._param_setup.calculation_inputs.telescope_and_environment.eta_spill.value
    
    @property
    def eta_block(self):
        """
        Get the lowered efficiency due to blocking
        """
        return self._param_setup.calculation_inputs.telescope_and_environment.eta_block.value
    
    @property
    def eta_pol(self):
        """
        Get the polarisation efficiency
        """
        return self._param_setup.calculation_inputs.telescope_and_environment.eta_pol.value
    
    ##############################################################
    # Getters for environment parameters #
    ##############################################################

    @property
    def T_cmb(self):
        """
        Get the temperature of the CMB
        """
        return self._param_setup.calculation_inputs.telescope_and_environment.T_cmb.value

    @property
    def T_amb(self):
        """
        Get the average ambient temperature
        """
        return self._param_setup.calculation_inputs.telescope_and_environment.T_amb.value
        
    def show(self):
        for name in dir(self.__class__):
            attr = getattr(self.__class__, name)
            if isinstance(attr, property):
                value = getattr(self, name)
                print(f"{name}: {value}")
