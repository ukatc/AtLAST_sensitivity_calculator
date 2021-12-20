import astropy.units as u
import numpy as np
from pathlib import Path
import pytest

STATIC_DATA_PATH = Path(__file__).resolve().parents[1] / "static"

WEATHER_PWV = np.array([5, 10, 20])
T_ATM_PATH = STATIC_DATA_PATH / "lookups" / "T_atm_SKA_test.txt"
TAU_ATM_PATH = STATIC_DATA_PATH / "lookups" / "tau_atm_SKA_test.txt"

def test_init():
    from src.functions.atmosphere_params import AtmosphereParams
    obs_freq = 40 * u.GHz
    pwv = 0.5
    elevation = 20 * u.deg
    atm = AtmosphereParams(obs_freq, pwv, elevation)
    assert atm.tau_atm_table[0,0] == 2.50
    assert atm.T_atm_table[0,0] == 2.50

def test_tau_atm():
    from src.functions.atmosphere_params import AtmosphereParams
    obs_freq = 41 * u.GHz
    pwv = 0.5
    elevation = 20 * u.deg
    atm = AtmosphereParams(obs_freq, pwv, elevation)
    zenith = 90.0 * u.deg - elevation

    assert (atm.tau_atm().value < 6e-3/np.cos(zenith)) and (atm.tau_atm().value > 5e-3/np.cos(zenith))


def test_T_atm():
    from src.functions.atmosphere_params import AtmosphereParams
    obs_freq = 41 * u.GHz
    pwv = 0.5
    elevation = 20 * u.deg
    atm = AtmosphereParams(obs_freq, pwv, elevation)

    assert (atm.T_atm().value > 1.40) and (atm.T_atm().value < 1.43)
