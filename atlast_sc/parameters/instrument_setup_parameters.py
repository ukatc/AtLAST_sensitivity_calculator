from atlast_sc.utils import Decorators

####################################################################
# Getters and a couple of setters for instrument setup parameters  #
####################################################################

class InstrumentSetupParameters:

    def __init__(self, config):
        self.config = config

    @property
    def surface_rms(self):
        """
        Get the surface smoothness of the instrument
        """
        return self.config.calculation_inputs.instrument_setup.surface_rms.value

    @property
    def dish_radius(self):
        """
        Get the radius of the primary mirror
        """
        return self.config.calculation_inputs.instrument_setup.dish_radius.value

    @dish_radius.setter
    @Decorators.validate_and_update_params
    def dish_radius(self, value):
        # TODO Flag to the user somehow that they are varying an instrument
        #   setup parameter?
        self.config.calculation_inputs.instrument_setup.dish_radius.value = value
        self.config.calculation_inputs.instrument_setup.dish_radius.unit = value.unit

    @property
    def T_amb(self):
        """
        Get the average ambient temperature
        """
        return self.config.calculation_inputs.instrument_setup.T_amb.value

    @property
    def eta_eff(self):
        """
        Get the forward efficiency
        """
        return self.config.calculation_inputs.instrument_setup.eta_eff.value

    @property
    def eta_ill(self):
        """
        Get the illumination efficiency
        """
        return self.config.calculation_inputs.instrument_setup.eta_ill.value

    @property
    def eta_spill(self):
        """
        Get the spillover efficiency
        """
        return self.config.calculation_inputs.instrument_setup.eta_spill.value

    @property
    def eta_block(self):
        """
        Get the lowered efficiency due to blocking
        """
        return self.config.calculation_inputs.instrument_setup.eta_block.value

    @property
    def eta_pol(self):
        """
        Get the polarisation efficiency
        """
        return self.config.calculation_inputs.instrument_setup.eta_pol.value

    #########################
    # Getters for constants #
    #########################

    @property
    def T_cmb(self):
        """
        Get the temperature of the CMB
        """
        return self.config.calculation_inputs.T_cmb.value
