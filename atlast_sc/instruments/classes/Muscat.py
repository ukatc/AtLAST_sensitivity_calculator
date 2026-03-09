from numpy import expm1, sqrt
import astropy.units as u
from astropy import constants
from atlast_sc.instrument import Instrument
from atlast_sc.derived_groups import noise_temperature

"""
MUSCAT instrument parameters
"""        
class Muscat(Instrument):
    def __init__(self, data):
        super().__init__(data)
        self.eta_chip_co = self.data.chip_and_cold_optics_efficiency['value']
        # self.T_co = self.create_Quantity(self.data.cold_optics_temperature) # not currently used
        self.delta_g = self.create_Quantity(self.data.band_gap)
        self.eta_pb = self.data.pair_breaking_efficiency['value']
    
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

    def calculate_system_temperature(self, obs_freq, bandwidth,eta_eff, 
                                     T_amb, T_sky, transmittance, n_pol):
        """
        Returns system temperature, following calculation in [doc]

        :return: system temperature in Kelvin
        :rtype: astropy.units.Quantity
        """
        # calculate power spectral density
        psdkid = constants.k_B * (self.eta_chip_co * (1 - eta_eff) * noise_temperature(T_amb, obs_freq) +
                self.eta_chip_co * eta_eff * T_sky
                )
        
        # calculate power absorbed by instrument
        pkid = (psdkid * bandwidth) # assuming small bandwidth

        # calculate noise equivalent power
        nep = (sqrt(2 * pkid * constants.h * obs_freq +
                    2 * pkid**2 / (n_pol * bandwidth) +
                    4 * self.delta_g * pkid / self.eta_pb))

        system_temp = (nep / (constants.k_B * eta_eff * transmittance *
               self.eta_chip_co *
               sqrt(2 * n_pol * bandwidth))).to(u.K)
        
        self.T_sys = system_temp
        return system_temp