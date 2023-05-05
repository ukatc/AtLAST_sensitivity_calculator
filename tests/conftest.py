import pytest
import numpy as np
import astropy.units as u
from atlast_sc.temperatures import Temperatures
from atlast_sc.atmosphere_params import AtmosphereParams
from atlast_sc.efficiencies import Efficiencies
from atlast_sc.data import Data
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
    return _get_param(Data.integration_time)


@pytest.fixture(scope='session')
def sensitivity():
    # Return the default sensitivity
    return _get_param(Data.sensitivity)


@pytest.fixture(scope='session')
def bandwidth():
    # Return the default bandwidth
    return _get_param(Data.bandwidth)


@pytest.fixture(scope='session')
def n_pol():
    # Return the default number of polarizations
    return _get_param(Data.n_pol)


@pytest.fixture(scope='session')
def obs_freq():
    # Return the default observing frequency
    return _get_param(Data.obs_frequency)


@pytest.fixture(scope='session')
def weather():
    # Return the default weather value
    return _get_param(Data.weather)


@pytest.fixture(scope='session')
def elevation():
    # Return the default elevation
    return _get_param(Data.elevation)


@pytest.fixture(scope='session')
def t_cmb():
    # Return the CMB temperature
    return _get_param(Data.t_cmb)


@pytest.fixture(scope='session')
def t_amb():
    # Return the default ambient temperature
    return _get_param(Data.t_amb)


@pytest.fixture(scope='session')
def g():
    # Return the default sideband ratio
    return _get_param(Data.g)


@pytest.fixture(scope='session')
def eta_eff():
    # Return the default forward efficiency
    return _get_param(Data.eta_eff)


@pytest.fixture(scope='session')
def eta_ill():
    # Return the default illumination efficiency
    return _get_param(Data.eta_ill)


@pytest.fixture(scope='session')
def eta_spill():
    # Return the default spillover efficiency
    return _get_param(Data.eta_spill)


@pytest.fixture(scope='session')
def eta_block():
    # Return the default block efficiency
    return _get_param(Data.eta_block)


@pytest.fixture(scope='session')
def eta_pol():
    # Return the default polarization efficiency
    return _get_param(Data.eta_pol)


@pytest.fixture(scope='session')
def dish_radius():
    # Return the default dish radius
    return _get_param(Data.dish_radius)


@pytest.fixture(scope='session')
def area(dish_radius):
    # Calculate and return the dish area
    return np.pi * dish_radius ** 2


@pytest.fixture(scope='session')
def surface_rms():
    # Return the default surface RMS
    return _get_param(Data.surface_rms)


@pytest.fixture(scope='session')
def temperatures(obs_freq, t_cmb, _amb, g, eta_eff):

    class TestAtmoshpereParams:
        @property
        def T_atm(self):
            return 255 * u.K

        @property
        def tau_atm(self):
            return 0.8

    return Temperatures(obs_freq, t_cmb, t_amb, g, eta_eff,
                        TestAtmoshpereParams())


@pytest.fixture(scope='session')
def atmosphere_params(obs_freq, weather, elevation):
    return AtmosphereParams(obs_freq, weather, elevation)


@pytest.fixture(scope='session')
def efficiencies(obs_freq, surface_rms, eta_ill, eta_spill, eta_block,
                 eta_pol):
    return Efficiencies(obs_freq, surface_rms, eta_ill, eta_spill,
                        eta_block, eta_pol)


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
