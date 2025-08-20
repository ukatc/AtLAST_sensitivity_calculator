from atlast_sc.utils import Decorators

#######################################################################
# Getters and a couple of setters for instrument specific parameters  #
#######################################################################

class InstrumentSpecificParameters:

    def __init__(self, param_setup):
        self._param_setup = param_setup

    @property
    def g(self):
        """
        Get the sideband ratio
        """
        return self._param_setup.calculation_inputs.instrument_setup.g.value

    @property
    def eta_pol(self):
        """
        Get the polarisation efficiency
        """
        return self._param_setup.calculation_inputs.instrument_setup.eta_pol.value