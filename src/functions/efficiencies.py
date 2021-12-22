from astropy import constants
import numpy as np
from scipy.interpolate.dfitpack import regrid_smth_spher

class Efficiencies:
    '''
    All of the efficiency factors need to come in here...
    '''
    def __init__(self, eta_ill):
        '''
        At present, a placeholder method just to hold some efficiencies.
        :param eta1: efficiency 1
        :type eta1: float
        etc.
        '''
        self.eta_ill = eta_ill

    def eta_a(self, obs_freq, surface_rms):
        '''
        Return the dish efficiency eta_a that needs to go into the SEFD calculation
        Using Ruze formula 
        '''
        wavelength = constants.c /obs_freq
        eta_a = self.eta_ill * np.exp((4* np.pi * surface_rms / wavelength)**2)
        return eta_a

    def eta_s(self):
        '''
        Return the system efficiency eta_s that goes into the sensitivity calculation
        PLACEHOLDER
        '''
        eta_s = 0.9
        return eta_s
