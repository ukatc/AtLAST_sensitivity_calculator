###############################################
# Getters for instrument specific parameters  #
###############################################

class InstrumentSpecificParameters:

    def __init__(self, param_setup):
        self._param_setup = param_setup

    @property
    def eta_pol(self):
        """
        Get the polarisation efficiency
        """
        return self._param_setup.calculation_inputs.instrument_specific.eta_pol.value
    
        
    def show(self):
        for name in dir(self.__class__):
            attr = getattr(self.__class__, name)
            if isinstance(attr, property):
                value = getattr(self, name)
                print(f"{name}: {value}")
