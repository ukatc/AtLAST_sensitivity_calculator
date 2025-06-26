from atlast_sc.utils import Decorators

####################################################################
# Getters and a couple of setters for instrument setup parameters  #
####################################################################

class InstrumentSetupParameters:

    def __init__(self, config):
        self.config = config

    @property
    def eta_pol(self):
        """
        Get the polarisation efficiency
        """
        return self.config.calculation_inputs.instrument_setup.eta_pol.value