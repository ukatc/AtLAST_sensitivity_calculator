from numpy import expm1, sqrt
import numpy as np
import astropy.units as u
from astropy import constants
from atlast_sc.instrument import Instrument
from atlast_sc.derived_groups import noise_temperature

"""
MISTRAL instrument parameters
"""        
class Mistral(Instrument):
    def __init__(self, data):
        super().__init__(data)
        self.atm_fit_slope = float(self.data.tau_to_net["fit_slope"]["value"])
        self.atm_fit_intercept = float(self.data.tau_to_net["fit_intercept"]["value"])
        self.chip_efficiency = self.data.chip_efficiency["value"]
        self.cold_optics_efficiency = self.data.cold_optics_efficiency["value"]
        

    ##################################
    # Instrument specific parameters #
    ##################################

    @property 
    def T_sys(self):
        return self._T_sys
    
    @T_sys.setter
    def T_sys(self, value):
        self._T_sys = value


    ################################################
    # Additional instrument specific methods below #
    ################################################


    @staticmethod
    def create_Quantity(inst_spec_param):
        """
        Create an Astropy Quantity object from a parameter 
        retrieved from the instrument YAML. 

        Note: Only used on the instrument specific parameters 
        that have a unit accompanying the value. As some of the 
        instrument specific equations need to be working with 
        Astropy Quantity objects.
        """
        value = inst_spec_param['value']
        unit = inst_spec_param['unit']
        quantity = u.Quantity(value=value, unit=unit)
        return quantity

    def tau_to_net(self,tau):

        fit = np.array([self.atm_fit_slope, self.atm_fit_intercept]) # from mK to K
        poly = np.poly1d(fit)

        return poly(tau)
    
    def calculate_system_temperature(self, obs_freq, bandwidth, eta_eff, 
                                     T_amb, T_sky, transmittance, n_pol):
        """
        Returns system temperature, following calculation in [doc]

        :return: system temperature in Kelvin
        :rtype: astropy.units.Quantity
        """

        tau = -np.log(transmittance)
        NET = self.tau_to_net(tau)      
        NEP = 2 * constants.k_B.value * bandwidth.to(u.Hz).value * NET
        Tsys = NEP / constants.k_B.value / self.chip_efficiency / self.cold_optics_efficiency / np.sqrt(2 *n_pol * bandwidth.to(u.Hz).value)  * u.K

        self.T_sys = Tsys
        return Tsys
