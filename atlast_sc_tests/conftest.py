import os
import pytest
from dataclasses import dataclass
import astropy.units as u
from pydantic import BaseModel
from atlast_sc.derived_groups import Temperatures
from atlast_sc.derived_groups import AtmosphereParams
from atlast_sc.derived_groups import Efficiencies
from atlast_sc.data import Data, DataHelper
from atlast_sc.calculator import Calculator
from atlast_sc.models import ValueWithoutUnits, ValueWithUnits


@pytest.fixture(scope='session')
def test_files_path():
    return os.path.join(os.path.dirname(__file__), 'test_files')


@pytest.fixture(scope='session')
def tmp_output_dir(tmp_path_factory):
    """
    Temporary directory where output files should be stored
    """
    return tmp_path_factory.mktemp('output')


@pytest.fixture()
def calculator():
    # Return a calculator with default parameters
    return Calculator()


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
def surface_rms():
    # Return the default surface RMS
    return _get_param(Data.surface_rms)


@pytest.fixture(scope='session')
def t_sys(temperatures):
    # Return the system temperature
    return temperatures.T_sys


@pytest.fixture(scope='session')
def t_rx(temperatures):
    # Return the receiver temperature
    return temperatures.T_rx


@pytest.fixture(scope='session')
def t_atm(obs_freq, weather, atmosphere_params):
    return atmosphere_params.calculate_atmospheric_temperature(obs_freq,
                                                               weather)


@pytest.fixture(scope='session')
def tau_atm(obs_freq, weather, elevation, atmosphere_params):
    return atmosphere_params.calculate_tau_atm(obs_freq, weather, elevation)


@pytest.fixture(scope='session')
def eta_a(efficiencies):
    return efficiencies.eta_a


@pytest.fixture(scope='session')
def eta_s(efficiencies):
    return efficiencies.eta_s


@pytest.fixture()
def sefd(calculator, t_sys, eta_a):
    return calculator._calculate_sefd(t_sys, eta_a)


@pytest.fixture(scope='session')
def temperatures(obs_freq, t_cmb, t_amb, g, eta_eff, t_atm, tau_atm):
    return Temperatures(obs_freq, t_cmb, t_amb, g, eta_eff, t_atm, tau_atm)


@pytest.fixture(scope='session')
def atmosphere_params():
    return AtmosphereParams()


@pytest.fixture(scope='session')
def efficiencies(obs_freq, surface_rms, eta_ill, eta_spill, eta_block,
                 eta_pol):
    return Efficiencies(obs_freq, surface_rms, eta_ill, eta_spill,
                        eta_block, eta_pol)


@pytest.fixture(scope='session')
def user_input_dict(t_int, sensitivity, bandwidth, obs_freq, n_pol,
                    weather, elevation):

    input_params = {
        't_int': t_int,
        'sensitivity': sensitivity,
        'bandwidth': bandwidth,
        'obs_freq': obs_freq,
        'n_pol': n_pol,
        'weather': weather,
        'elevation': elevation
    }

    return input_params


@pytest.fixture(scope='session')
def instrument_setup_dict(g, surface_rms, dish_radius, t_amb, eta_eff, eta_ill,
                          eta_spill, eta_block, eta_pol):

    instrument_setup_parms = {
        'g': g,
        'surface_rms': surface_rms,
        'dish_radius': dish_radius,
        'T_amb': t_amb,
        'eta_eff': eta_eff,
        'eta_ill': eta_ill,
        'eta_spill': eta_spill,
        'eta_block': eta_block,
        'eta_pol': eta_pol
    }

    return instrument_setup_parms


@pytest.fixture(scope='session')
def test_model_with_values():
    class TestModel(BaseModel):
        value1: ValueWithUnits = ValueWithUnits(value=1, unit='GHz')
        value2: ValueWithUnits = ValueWithUnits(value=2.12345678e10, unit='s')
        value3: ValueWithoutUnits = ValueWithoutUnits(value=1)
        value4: ValueWithoutUnits = ValueWithoutUnits(value=1.12345678)

    return TestModel()


@pytest.fixture(scope='session')
def test_model_with_literals():
    class TestModel(BaseModel):
        value1: float = 1.3
        value2: bool = True
        value3: str = "hello"
        value4: list = [1, 2, 3]

    return TestModel()


@pytest.fixture()
def test_data_types(mocker):
    # Use this fixture to unit test Validator functions, etc., so they are
    # decoupled from the allowed values, units, etc., of the real
    # Calculator params.

    @dataclass
    class DataType:
        default_value: float = None
        default_unit: str = None
        lower_value: float = None
        lower_value_is_floor: bool = False
        upper_value: float = None
        upper_value_is_ceil: bool = False
        allowed_values: list = None
        units: list[str] = None

        def __post_init__(self):
            if self.units:
                self.data_conversion = \
                    DataHelper.data_conversion_factors(self.default_unit,
                                                       self.units)

    t_int = DataType(
        default_value=100,
        default_unit=str(u.s),
        lower_value=1,
        upper_value=float('inf'),
        upper_value_is_ceil=True,
        units=[str(u.s), str(u.min), str(u.h)],
    )

    sensitivity = DataType(
        default_value=3.0,
        default_unit=str(u.mJy),
        lower_value=0,
        lower_value_is_floor=True,
        upper_value=1e10,
        upper_value_is_ceil=True,
        units=[str(u.uJy), str(u.mJy), str(u.Jy)],
    )

    n_pol = DataType(
        default_value=2,
        allowed_values=[1, 2]
    )

    obs_freq = DataType(
        default_value=100,
        default_unit=str(u.GHz),
        lower_value=35,
        upper_value=950,
        units=[str(u.GHz)]
    )

    allowed_values_with_units = DataType(
        default_value=100,
        default_unit=str(u.s),
        allowed_values=[1, 60],
        units=[str(u.s), str(u.min), str(u.h)],
    )

    param_data_type_dicts = {
        't_int': t_int,
        'sensitivity': sensitivity,
        'n_pol': n_pol,
        'obs_freq': obs_freq,
        'allowed_values_with_units': allowed_values_with_units,
    }

    mocker.patch(__name__ + '.Data.param_data_type_dicts',
                 return_value=param_data_type_dicts,
                 new_callable=mocker.PropertyMock)

    return param_data_type_dicts


def _get_param(param):
    if param.default_unit is not None:
        return param.default_value * u.Unit(param.default_unit)

    return float(param.default_value)
