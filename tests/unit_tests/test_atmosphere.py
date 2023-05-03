import pytest
import astropy.units as u
from atlast_sc.atmosphere_params import AtmosphereParams


test_data = [
    (35, "band 1"),
    (60, "opaque"),
    (125, "band 3"),
    (150, "band 4"),
    (200, "band 5"),
    (250, "band 6"),
    (350, "band 7"),
    (380, "opaque"),
    (420, "band 8"),
    (550, "opaque"),
    (650, "band 9"),
    (750, "opaque"),
    (850, "band 10"),
]


@pytest.mark.parametrize('obs_freq,band',test_data)
def test__calculate_atmospheric_tau_factor(obs_freq, band, weather):

    elevations = [5, 45]

    tau_factors = []
    atms = []
    obs_freq = obs_freq * u.GHz
    for elevation in elevations:
        elevation = elevation * u.deg
        atmosphere_params = AtmosphereParams(obs_freq, weather, elevation)
        tau_factors.append(atmosphere_params._calculate_atmospheric_tau_factor())
        atms.append(atmosphere_params)

    # Check that the tau factor for the lower elevation is greater than the
    #   tau factor for the higher elevation
    assert tau_factors[0] > tau_factors[1]

    # Check the tau factors have been correctly assigned to the tau_atm
    # property
    assert tau_factors == [atm.tau_atm for atm in atms]

    # Check that the tau factor is "high" for frequencies between bands
    for tau_factor in tau_factors:
        if band == "opaque":
            assert tau_factor > 10
        else:
            assert tau_factor < 10


@pytest.mark.parametrize('obs_freq,band', test_data)
def test__calculate_temperature(obs_freq, band, weather, elevation):

    obs_freq = obs_freq * u.GHz

    atmosphere_params = AtmosphereParams(obs_freq, weather, elevation)
    temp = atmosphere_params._calculate_temperature()

    # Check that the temperature has been correctly assigned to the T_atm
    # property
    assert temp == atmosphere_params.T_atm

    # Check that the atmospheric temperature is "cold" for transparent
    # frequencies
    if band == "opaque":
        assert temp > 250 * u.K
    else:
        assert temp < 150 * u.K
