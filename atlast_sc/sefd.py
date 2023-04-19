from astropy.constants import k_B
import numpy as np

class SEFD:
    """
    Class that calculates the source equivalent flux density, SEFD
    TODO: do we really need this class. A method in the calculatr class is
    probably enough
    """

    @staticmethod
    def calculate(T_sys, dish_radius, eta_A):
        """
        Calculate SEFD from the system temperature T_sys, the dish area and
        the efficiency eta_A

        :param T_sys: system temperature
        :type T_sys: astropy.units.Quantity
        :param dish_radius: the dish radius
        :type dish_radius: astropy.units.Quantity
        :param eta_A: the dish efficiency factor
        :type eta_A: float
        :return: source equivalent flux density
        :rtype: astropy.units.Quantity
        """

        dish_area = np.pi * dish_radius ** 2
        return (2 * k_B * T_sys) / (eta_A * dish_area)
