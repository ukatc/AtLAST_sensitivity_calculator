import pytest
from astropy.units import Unit
from atlast_sc.data import ObsFrequency, TCmb, TAmb, G, EtaEff


@pytest.fixture(scope='session')
def tmp_output_dir(tmp_path_factory):
    """
    Temporary directory where output files should be stored
    """
    return tmp_path_factory.mktemp('output')


@pytest.fixture(scope='session')
def obs_freq():
    # Return the default observing frequency
    return ObsFrequency.DEFAULT_VALUE.value * Unit(ObsFrequency.DEFAULT_UNIT.value)


@pytest.fixture(scope='session')
def t_cmb():
    # Return the CMB temperature
    return TCmb.DEFAULT_VALUE.value * Unit(TCmb.DEFAULT_UNIT.value)


@pytest.fixture(scope='session')
def t_amb():
    # Return the default ambient temperature
    return TAmb.DEFAULT_VALUE.value * Unit(TAmb.DEFAULT_UNIT.value)


@pytest.fixture(scope='session')
def g():
    # Return the default sideband ratio
    return G.DEFAULT_VALUE.value


@pytest.fixture(scope='session')
def eta_eff():
    # Return the default forward efficiency
    return EtaEff.DEFAULT_VALUE.value


@pytest.fixture(scope='session')
def user_input():
    pass

