import astropy.units as u

from run import T_gal

class SkyParams:
    def __init__(self):
        pass

    def get_T_gal(self, obs_freq, coords):
        '''
        Return T_gal for a given sky position.

        :param obs_freq: the observing frequency
        :type obs_freq: astropy.units.Quantity
        :param coords: target coordinates
        :type coords: astrpy.coordinates.SkyCoord
        :return: T galaxy
        :rtype: astropy.units.Quantity
        '''
        # raise NotImplementedError

        self.T_gal = T_gal
    
