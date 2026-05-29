import astropy.units as u
from astropy import constants
from atlast_sc.instrument import Instrument
from atlast_sc.derived_groups import noise_temperature

"""
Default instrument parameters
"""        
class Default(Instrument):
    def __init__(self, data):
        super().__init__(data)
        self._T_rx = None
        self.prefactor = data.prefactor['value']

    ##################################
    # Instrument specific parameters #
    ##################################
        
    @property 
    def T_rx(self):
        return self._T_rx
    
    @T_rx.setter
    def T_rx(self, value):
        self._T_rx = value

    @property 
    def T_sys(self):
        return self._T_sys
    
    @T_sys.setter
    def T_sys(self, value):
        self._T_sys = value

    ################################################
    # Additional instrument specific methods below #
    ################################################

    def calculate_system_temperature(self, obs_freq, bandwidth, eta_eff, 
                                     T_amb, T_sky, transmittance, n_pol):
        """
        Returns system temperature, following calculation in [doc]

        :return: system temperature in Kelvin
        :rtype: astropy.units.Quantity
        """
        self.T_rx = self.calculate_receiver_temp(obs_freq)
        system_temp = 1 / (eta_eff * transmittance) * \
            (self.T_rx
            + (eta_eff * T_sky)
            + ((1 - eta_eff) * noise_temperature(T_amb, obs_freq))
            )
        self.T_sys = system_temp
        return system_temp

    def calculate_receiver_temp(self, obs_freq):
        """
        Returns receiver temperature, following calculation in [doc]

        :return: receiver temperature in Kelvin
        :rtype: astropy.units.Quantity
        """

        # h*f/k is the quantum limit 
        # scaling prefactor defines how close to that we expect to get
        temp = (self.prefactor * constants.h * obs_freq / constants.k_B).to(u.K)
        self.T_rx = temp
        return temp