import astropy.units as u
import numpy as np

class Calculator:
    ''' Calculator class that does the core calculation to get the output sensitivity or integration time. '''
    def __init__(self, bandwidth, tau_atm, sefd, n_pol, eta_s):
        self.bandwidth = bandwidth
        self.tau_atm = tau_atm
        self.sefd = sefd
        self.n_pol = n_pol
        self.eta_s = eta_s
        
    def sensitivity(self, t_int):
        '''
        Return sensitivity of telescope (Jansky) for a given integration time t_int

        :param t_int: integration time 
        :type t_int: astropy.units.Quantity
        :return: sensitivity in Janksy
        :rtype: astropy.units.Quantity
        '''
        sensitivity = self.sefd/(self.eta_s * np.sqrt(self.n_pol * self.bandwidth * t_int)) * np.exp(self.tau_atm)
        return sensitivity.to(u.Jy)

    def t_integration(self, sensitivity):
        '''
        Return integration time required for some sensitivity to be reached.

        :param sensitivity: required sensitivity in Jansky
        :type sensitivity: astropy.units.Quantity
        :return: integration time in seconds
        :rtype: astropy.units.Quantity
        '''
        t_int = (self.sefd / sensitivity * np.exp(self.tau_atm) * self.eta_s)**2 / (self.n_pol * self.bandwidth)
        return t_int.to(u.s)