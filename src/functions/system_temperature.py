class SystemTemperature:
    """
    Contains all the relevant temperatures that input to the total system temperature, T_sys
    """

    def __init__(self, T_rx, T_cmb, T_atm, T_amb, T_gal, tau_atm):
        self.T_atm = T_atm
        self.T_cmb = T_cmb
        self.T_rx = T_rx
        self.T_amb = T_amb
        self.T_gal = T_gal
        self.tau_atm = tau_atm
        self.T_sky =  self.T_atm*(1 - tau_atm) + self.T_cmb + self.T_gal

    def system_temperature(self, g, eta_eff):
        '''
        Returns system temperature, following calculation in [doc]
        :param g: 
        '''
        return((1 + g) / eta_eff * self.tau_atm) * (self.T_rx + (eta_eff * self.T_sky) + ((1 - eta_eff) * self.T_amb))
