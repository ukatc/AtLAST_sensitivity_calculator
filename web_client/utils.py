import astropy.units as u
from atlast_sc.core.utils import DataHelper
from atlast_sc.core.parameter_setup import ParameterSetup


VERSION = "1.0.0"

# Global state to store special units
special_units = ['km / s', 'm / s', 'K', 'mK']

def version_num_for_url():
    return VERSION.replace(".", "_")


def modify_user_input_with_converted_values(user_input):
    """
    Converts special unit parameters to an equivalent
    value in their respective units and replaces the old value 
    with the converted value in the user input dictionary. 
    """
    obs_freq = u.Quantity(float(user_input['obs_freq']['value']),\
               user_input['obs_freq']['unit'])
    bandwidth = u.Quantity(float(user_input['bandwidth']['value']),\
               user_input['bandwidth']['unit'])
    dish_radius = ParameterSetup().telescope_and_environment.dish_radius.value
    sensitivity = u.Quantity(float(user_input['sensitivity']['value']),\
               user_input['sensitivity']['unit'])
    
    # Convert velocity to frequency
    if user_input['bandwidth']['unit'] in special_units:
        bandw_val, bandw_unit = DataHelper.convert_velocity_to_frequency(obs_freq, bandwidth)
        user_input['bandwidth']['value'] = str(bandw_val)
        user_input['bandwidth']['unit'] = str(bandw_unit)
    if user_input['sensitivity']['unit'] in special_units:
        flux_dens_val, flux_dens_unit = DataHelper.convert_temperature_to_flux_density(
                                                        obs_freq, dish_radius, sensitivity)
        user_input['sensitivity']['value'] = str(flux_dens_val)
        user_input['sensitivity']['unit'] = str(flux_dens_unit)
    return user_input
