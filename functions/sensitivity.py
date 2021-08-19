import astropy.units as u
import numpy as np

class Calculator:
    def __init__(self, bandwidth, tau_atm, sefd, n_pol, eta_s, sensitivity=0, t_int=0):
        self.bandwidth = bandwidth
        self.tau_atm = tau_atm
        self.sefd = sefd
        self.n_pol = n_pol
        self.eta_s = eta_s
        self.sensitivity = sensitivity
        self.t_int = t_int
        
    def calc_sensitivity(self):
        '''
        Return sensitivity of telescope (Jansky) for a given integration time t_int
        '''
        sensitivity = self.sefd/(self.eta_s * np.sqrt(self.n_pol * self.bandwidth * self.t_int))
        return sensitivity * np.exp(self.tau_atm)

    def calc_t_integration(self):
        '''
        Return integration time required for some sensitivity S (Jansky) to be reached.
        '''
        t_int = (np.exp(self.tau_atm) * self.sefd / self.sensitivity * self.eta_s)**2 / (self.n_pol * self.bandwidth)
        return t_int