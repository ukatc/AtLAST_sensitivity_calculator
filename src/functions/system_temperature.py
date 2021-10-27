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
        self.T_sky = self.sky_temperature(tau_atm)

    def sky_temperature(self, tau_atm):
        return self.T_atm * (1 - tau_atm) + self.T_cmb + self.T_gal

    def calculate(self, g, eta_eff, tau_atm):
        """
        Returns """
        return ((1 + g) / eta_eff * tau_atm) * (
            self.T_rx + (eta_eff * self.T_sky) + ((1 - eta_eff) * self.T_amb)
        )
