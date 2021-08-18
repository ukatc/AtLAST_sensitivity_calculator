def tau_atm(obs_freq, pwv):
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

    raise NotImplementedError
    return(tau_atm)
    
def T_atm(obs_freq, pwv):
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

    raise NotImplementedError
    return(T_atm)