import pytest
import numpy as np
import astropy.units as u
from atlast_sc.temperatures import Temperatures
from atlast_sc.atmosphere_params import AtmosphereParams
from atlast_sc.efficiencies import Efficiencies
from atlast_sc.sefd import SEFD
import atlast_sc.data as data


@pytest.fixture(scope='session')
def tmp_output_dir(tmp_path_factory):
    """
    Temporary directory where output files should be stored
    """
    return tmp_path_factory.mktemp('output')


@pytest.fixture(scope='session')
def t_int():
    # Return the default integration time
    return _get_param(data.integration_time)


@pytest.fixture(scope='session')
def sensitivity():
    # Return the default sensitivity
    return _get_param(data.sensitivity)


@pytest.fixture(scope='session')
def bandwidth():
    # Return the default bandwidth
    return _get_param(data.bandwidth)


@pytest.fixture(scope='session')
def n_pol():
    # Return the default number of polarizations
    return _get_param(data.n_pol)


@pytest.fixture(scope='session')
def obs_freq():
    # Return the default observing frequency
    return _get_param(data.obs_frequency)


@pytest.fixture(scope='session')
def weather():
    # Return the default weather value
    return _get_param(data.weather)


@pytest.fixture(scope='session')
def elevation():
    # Return the default elevation
    return _get_param(data.elevation)


@pytest.fixture(scope='session')
def t_cmb():
    # Return the CMB temperature
    return _get_param(data.t_cmb)


@pytest.fixture(scope='session')
def t_amb():
    # Return the default ambient temperature
    return _get_param(data.t_amb)


@pytest.fixture(scope='session')
def g():
    # Return the default sideband ratio
    return _get_param(data.g)


@pytest.fixture(scope='session')
def eta_eff():
    # Return the default forward efficiency
    return _get_param(data.eta_eff)


@pytest.fixture(scope='session')
def eta_ill():
    # Return the default illumination efficiency
    return _get_param(data.eta_ill)


@pytest.fixture(scope='session')
def eta_spill():
    # Return the default spillover efficiency
    return _get_param(data.eta_spill)


@pytest.fixture(scope='session')
def eta_block():
    # Return the default block efficiency
    return _get_param(data.eta_block)


@pytest.fixture(scope='session')
def eta_pol():
    # Return the default polarization efficiency
    return _get_param(data.eta_pol)


@pytest.fixture(scope='session')
def eta_r():
    # Return the default ?? efficiency
    # TODO: What is this efficiency?
    return _get_param(data.eta_r)


@pytest.fixture(scope='session')
def dish_radius():
    # Return the default dish radius
    return _get_param(data.dish_radius)


@pytest.fixture(scope='session')
def area(dish_radius):
    # Calculate and return the dish area
    return np.pi * dish_radius ** 2


@pytest.fixture(scope='session')
def surface_rms():
    # Return the default surface RMS
    return _get_param(data.surface_rms)


@pytest.fixture(scope='session')
def temperatures(obs_freq, t_cmb, t_amb):

    T_atm = 255 * u.K
    tau_atm = 0.8

    return Temperatures(obs_freq, t_cmb, T_atm, t_amb, tau_atm)


@pytest.fixture(scope='session')
def atmosphere_params(obs_freq, weather, elevation):
    return AtmosphereParams(obs_freq, weather, elevation)


@pytest.fixture(scope='session')
def efficiencies(eta_ill, eta_spill, eta_block, eta_pol, eta_r):
    return Efficiencies(eta_ill, eta_spill, eta_block, eta_pol, eta_r)


@pytest.fixture(scope='session')
def sefd(temperatures, efficiencies, g, eta_eff, area, obs_freq, surface_rms):
    eta_a = efficiencies.eta_a(obs_freq, surface_rms)
    T_sys = temperatures.system_temperature(g, eta_eff)

    return SEFD.calculate(T_sys, area, eta_a)


@pytest.fixture(scope='session')
def user_input_params(t_int, sensitivity, bandwidth, obs_freq, n_pol,
                      weather, elevation):

    input_params = {
        't_int': {'value': t_int.value, 'unit': str(t_int.unit)},
        'sensitivity': {'value': sensitivity.value,
                        'unit': str(sensitivity.unit)},
        'bandwidth': {'value': bandwidth.value, 'unit': str(bandwidth.unit)},
        'obs_freq': {'value': obs_freq.value, 'unit': str(obs_freq.unit)},
        'n_pol': {'value': n_pol},
        'weather': {'value': weather},
        'elevation': {'value': elevation.value, 'unit': str(elevation.unit)}
    }

    return input_params


def _get_param(param):
    if param.default_unit is not None:
        return param.default_value * u.Unit(param.default_unit)

    return param.default_value
