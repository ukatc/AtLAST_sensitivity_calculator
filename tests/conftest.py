import pytest
import numpy as np
import astropy.units as u
from pydantic import BaseModel
from atlast_sc.derived_groups import Temperatures
from atlast_sc.derived_groups import AtmosphereParams
from atlast_sc.derived_groups import Efficiencies
from atlast_sc.data import Data
from atlast_sc.calculator import Calculator
from atlast_sc.models import ValueWithoutUnits, ValueWithUnits


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
def area(dish_radius):
    # Calculate and return the dish area
    return np.pi * dish_radius ** 2


@pytest.fixture(scope='session')
def surface_rms():
    # Return the default surface RMS
    return _get_param(Data.surface_rms)


@pytest.fixture(scope='session')
def temperatures(obs_freq, t_cmb, t_amb, g, eta_eff, weather, elevation,
                 atmosphere_params):
    t_atm = \
        atmosphere_params.calculate_atmospheric_temperature(obs_freq, weather)
    tau_atm = \
        atmosphere_params.calculate_tau_atm(obs_freq, weather, elevation)
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
def mock_calculator():
    class MockCalculator:

        def __init__(self):
            self._calculation_inputs = MockCalculator.MockCalculationInputs()

        class MockCalculationInputs:

            def validate_update(self, param, value):
                print('\n**********************************************')
                print(f'doing validation of {param} with value {value}')
                print('\n**********************************************')
                if value == "invalid":
                    raise ValueError

                return self

        @property
        def prop1(self):
            return 1

        @property
        def prop2(self):
            return 2.0

        @property
        def prop3(self):
            return '3'

        @property
        def calculation_inputs(self):
            return self._calculation_inputs

    return MockCalculator()


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


def _get_param(param):
    if param.default_unit is not None:
        return param.default_value * u.Unit(param.default_unit)

    return float(param.default_value)
