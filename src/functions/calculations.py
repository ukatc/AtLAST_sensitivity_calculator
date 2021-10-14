# Will need to get to the parameters required for the sensitivity calculation: bandwidth, tau_atm, SEFD, n_pol, eta_s, and either t_int or S.
# Bandwidth comes from config
# tau_atm comes from atm_model

from astropy import constants

class SEFD:
    def __init__(self) -> None:
        pass

    def calculate(T_sys, area, eta_A):
        '''
        Calculate SEFD from the system temperature T_sys, the dish area and the efficiency eta_A
        :param T_sys: system temperature
        :type T_sys: astropy.units.Quantity
        :param area: the dish area 
        :type area: astropy.units.Quantity
        :param eta_A: the efficiency factor
        :type eta_A: float
        '''
        return (2 * constants.k_B * T_sys)/(eta_A * area)
