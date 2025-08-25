###################################
# Getters for derived parameters  #
###################################

class DerivedParameters:
    def __init__(self, derived_params):
        self._derived_parameters = derived_params

    @property
    def tau_atm(self):
        """
        Get the atmospheric transmittance
        """
        return self._derived_parameters.tau_atm

    @property
    def T_atm(self):
        """
        Get the atmospheric temperature
        """
        return self._derived_parameters.T_atm

    @property
    def T_rx(self):
        """
        Get the receiver temperature
        """
        return self._derived_parameters.T_rx

    @property
    def eta_a(self):
        """
        Get the dish efficiency
        """
        return self._derived_parameters.eta_a

    @property
    def eta_s(self):
        """
        Get the system efficiency
        """
        return self._derived_parameters.eta_s

    @property
    def T_sys(self):
        """
        Get the system temperature
        """
        return self._derived_parameters.T_sys

    @property
    def T_sky(self):
        """
        Get the system temperature
        """
        return self._derived_parameters.T_sky

    @property
    def sefd(self):
        """
        Get the system equivalent flux density
        """
        return self._derived_parameters.sefd
        
    def show(self):
        for name in dir(self.__class__):
            attr = getattr(self.__class__, name)
            if isinstance(attr, property):
                value = getattr(self, name)
                print(f"  {name}: {value}")
