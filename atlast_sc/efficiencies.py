from astropy import constants
import numpy as np

class Efficiencies:
    '''
    All of the efficiency factors need to come in here...
    '''
    def __init__(self, eta_ill):
        '''
        At present, a placeholder method just to hold some efficiencies.

        :param eta_ill: the illumination factor
        :type eta_ill: float
        '''
        self.eta_ill = eta_ill

    def eta_a(self, obs_freq, surface_rms):
        '''
        Return the dish efficiency eta_a that needs to go into the SEFD calculation
        Using Ruze formula.

        :param obs_freq: the observing frequency in GHz
        :type obs_freq: astropy.units.Quantity
        :param surface_rms: the surface accuracy in micron
        :type surface_rms: astropy.units.Quantity
        :return: dish efficiency
        :rtype: astropy.units quantity
        '''
        wavelength = constants.c / obs_freq
        eta_a = self.eta_ill * np.exp((4* np.pi * surface_rms / wavelength)**2)
        return eta_a

    def eta_s(self):
        '''
        Return the system efficiency eta_s that goes into the sensitivity calculation
        PLACEHOLDER

        :return: system efficiency
        :rtype: astropy.units quantity
        '''
        eta_s = 0.9
        return eta_s
