import astropy.units as u

class AtmosphereParams:
    ''' Class used to retrieve atmospheric parameters from a model. '''
    def __init__(self, obs_freq, pwv):
        ''' AtmosphereParams class constructor. '''
        self.obs_freq = obs_freq
        self.pwv = pwv

    def tau_atm(self):
        '''
        Return atmospheric transmittance tau_atm 

        :param obs_freq: the central observing frequency
        :type obs_freq: astropy.units.Quantity
        :param pwv: the precipitable water vapour
        :type pwv: astropy.units.Quantity
        :return: Atmospheric transmittance
        :rtype: astropy.units.Quantity
        '''
        # something that calls the atmospheric model (same as SKA - interp over grid?)

        # raise NotImplementedError
        tau_atm = 0.8
        return tau_atm
        
    def T_atm(self):
        '''
        Return atmospheric temperature T_atm 

        :param obs_freq: the central observing frequency
        :type obs_freq: astropy.units.Quantity
        :param pwv: the precipitable water vapour
        :type pwv: astropy.units.Quantity
        :return: Atmospheric temperature
        :rtype: astropy.units.Quantity
        '''
        # something that calls the atmospheric model (same as SKA - interp over grid?)

        # raise NotImplementedError
        T_atm = 255 * u.K
        return T_atm