# Just the SEFD calculation in here. Will need input from system_temperature and efficiencies (some other calculation?)

from astropy import constants


class SEFD:
    ''' Class that calculates the source equivalent flux density, SEFD'''
    def __init__(self) -> None:
        """
        Constructor
        """
        pass

    def calculate(T_sys, area, eta_A):
        """
        Calculate SEFD from the system temperature T_sys, the dish area and the efficiency eta_A
        
        :param T_sys: system temperature
        :type T_sys: astropy.units.Quantity
        :param area: the dish area 
        :type area: astropy.units.Quantity
        :param eta_A: the dish efficiency factor
        :type eta_A: float
        :return: source equivalent flux density
        :rtype: astropy.units.Quantity
        """

        return (2 * constants.k_B * T_sys) / (eta_A * area)
