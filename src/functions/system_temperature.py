import numpy as np

class SystemTemperature:
    """
    Contains all the relevant temperatures that input to the total system temperature, T_sys
    """

    def __init__(self, T_rx, T_cmb, T_atm, T_amb, tau_atm):
        self.T_atm = T_atm
        self.T_cmb = T_cmb
        self.T_rx = T_rx
        self.T_amb = T_amb
        self.tau_atm = tau_atm
        self.transmittance = np.exp(-self.tau_atm)
        self.T_sky =  self.T_atm*(1 - self.transmittance) + self.T_cmb

    def system_temperature(self, g, eta_eff):
        '''
        Returns system temperature, following calculation in [doc]

        :param g: sideband ratio
        :type g: int
        :param eta_eff: forward efficiency
        :type eta_eff: float
        '''
        return((1 + g) / eta_eff * self.transmittance) * (self.T_rx + (eta_eff * self.T_sky) + ((1 - eta_eff) * self.T_amb))
