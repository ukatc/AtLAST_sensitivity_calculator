# Will need to get to the parameters required for the sensitivity calculation: bandwidth, tau_atm, SEFD, n_pol, eta_s, and either t_int or S.
# Bandwidth comes from config
# tau_atm comes from atm_model

from astropy import constants

def get_SEFD(T_sys, area, eta_A):
    return (2 * constants.k_B * T_sys)/(eta_A * area)
