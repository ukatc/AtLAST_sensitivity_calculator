import astropy.units as u
from atlast_sc.core.utils import DataHelper

VERSION = "1.0.0"


def version_num_for_url():
    return VERSION.replace(".", "_")


def modify_user_input_with_converted_values(user_input):
    """
    Converts given bandwith velocity value to an equivalent
    frequency in Hz and replaces the old bandwidth value 
    with the converted value in the user input dictionary. 
    """
    obs_freq = u.Quantity(float(user_input['obs_freq']['value']),\
               user_input['obs_freq']['unit'])
    bandwidth = u.Quantity(float(user_input['bandwidth']['value']),\
               user_input['bandwidth']['unit'])
    
    # Convert velocity to frequency
    bandw_val, bandw_unit = DataHelper.convert_velocity_to_frequency(obs_freq, bandwidth)
    user_input['bandwidth']['value'] = str(bandw_val)
    user_input['bandwidth']['unit'] = str(bandw_unit)
    return user_input
