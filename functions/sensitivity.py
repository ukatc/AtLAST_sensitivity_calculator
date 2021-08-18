import astropy.units as u
import numpy as np

def calc_sensitivity(bandwidth, tau_atm, SEFD, n_pol, eta_s, t_int):
    '''
    Return sensitivity of telescope (Jansky) for a given integration time t_int
    '''
    S = SEFD/(eta_s * np.sqrt(n_pol * bandwidth * t_int))
    return S * np.exp(tau_atm)

def calc_t_integration(bandwidth, tau_atm, SEFD, n_pol, eta_s, S):
    '''
    Return integration time required for some sensitivity S (Jansky) to be reached.
    '''
    t_int = (np.exp(tau_atm) * SEFD / S * eta_s)**2 / (n_pol * bandwidth)
    return t_int