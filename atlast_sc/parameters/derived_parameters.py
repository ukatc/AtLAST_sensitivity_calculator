###################################
# Getters for derived parameters  #
###################################

class DerivedParameters:
    def __init__(self, param_setup):
        self._param_setup = param_setup

    @property
    def tau_atm(self):
        """
        Get the atmospheric transmittance
        """
        return self._param_setup.derived_parameters_model.tau_atm

    @property
    def T_atm(self):
        """
        Get the atmospheric temperature
        """
        return self._param_setup.derived_parameters_model.T_atm

    @property
    def T_rx(self):
        """
        Get the receiver temperature
        """
        return self._param_setup.derived_parameters_model.T_rx

    @property
    def eta_a(self):
        """
        Get the dish efficiency
        """
        return self._param_setup.derived_parameters_model.eta_a

    @property
    def eta_s(self):
        """
        Get the system efficiency
        """
        return self._param_setup.derived_parameters_model.eta_s

    @property
    def T_sys(self):
        """
        Get the system temperature
        """
        return self._param_setup.derived_parameters_model.T_sys

    @property
    def T_sky(self):
        """
        Get the system temperature
        """
        return self._param_setup.derived_parameters_model.T_sky

    @property
    def sefd(self):
        """
        Get the system equivalent flux density
        """
        return self._param_setup.derived_parameters_model.sefd
        
    def show(self):
        for name in dir(self.__class__):
            attr = getattr(self.__class__, name)
            if isinstance(attr, property):
                value = getattr(self, name)
                print(f"{name}: {value}")

    def __eq__(self, other):
        """
        Method to compare each derived parameter
        """
        eq = True
        for name in dir(self.__class__):
            attr = getattr(self.__class__, name)
            other_attr = getattr(other.__class__, name)
            if isinstance(attr, property) and isinstance (other_attr, property):
                value = getattr(self, name)
                other_value = getattr(other, name)
                if (value != other_value):
                    eq = False
                    break
                else:
                    eq = True
        return eq