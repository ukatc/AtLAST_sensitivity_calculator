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
        self.npix = self.data.npix["value"]
        self.detector_yield = self.data.detector_yield["value"]

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

        fit = np.array([27.92229463,  0.17222585]) * 1e-3 # from mK to K
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
        #print("Tau =", tau)
        NET = self.tau_to_net(tau) 
        #print("MISTRAL NET=", NET)
        
        #NEP = 2 * constants.k_B.value * (obs_freq.to(u.Hz).value)**2 / constants.c.value**2 * NET * bandwidth.to(u.Hz).value * (3.3e-3)**2
        NEP = 2 * constants.k_B.value * bandwidth.to(u.Hz).value * NET
        #print("MISTRAL NEP=", NEP)
        Tsys = NEP / constants.k_B.value / 1 / 1 / np.sqrt(2 * 1 * bandwidth.to(u.Hz).value)  * u.K
        #print("Tsys=", Tsys)

        self.T_sys = Tsys
        return Tsys
    
    '''
    def calculate_system_temperature(self, obs_freq, bandwidth, eta_eff, 
                                     T_amb, T_sky, transmittance, n_pol):
        """
        Returns system temperature, following calculation in [doc]

        :return: system temperature in Kelvin
        :rtype: astropy.units.Quantity
        """
        # calculate power spectral density
        psdkid = constants.k_B * (self.eta_chip * (1 - self.eta_co) * noise_temperature(self.T_co, obs_freq) +
                self.eta_chip * self.eta_co * (1 - eta_eff) * noise_temperature(T_amb, obs_freq) +
                self.eta_chip * self.eta_co * eta_eff * T_sky
                )

        # calculate power absorbed by instrument
        pkid = (psdkid * n_pol * bandwidth) # assuming small bandwidth

        # calculate noise equivalent power
        nep = (sqrt(2 * pkid * constants.h * obs_freq +
                    2 * pkid**2 / (n_pol * bandwidth) +
                    4 * self.delta_g * pkid / self.eta_pb))

        system_temp = (nep / (constants.k_B * eta_eff * transmittance * \
               self.eta_chip * self.eta_co * \
               sqrt(2 * n_pol * bandwidth))).to(u.K)
        
        self.T_sys = system_temp
        return system_temp
    '''